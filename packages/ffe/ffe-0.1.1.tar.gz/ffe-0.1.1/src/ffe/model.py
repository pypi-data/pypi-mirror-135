import sys
import importlib.util
from pathlib import Path
from typing import Any, Type, TypedDict, cast
from abc import ABC, abstractmethod

# 采用 ErrMsg 而不是采用 exception, 一来是受到 Go 语言的影响，
# 另一方面，凡是用到 ErrMsg 的地方都是与业务逻辑密切相关并且需要向用户反馈详细错误信息的地方，
# 这些地方用 ErrMsg 更合理。 (以后会改用 pypi.org/project/result)
ErrMsg = str
"""一个描述错误内容的简单字符串，空字符串表示无错误。"""

Result = tuple[list[str], ErrMsg]
"""Result 由两元素组成。当多个任务组合使用时，第一个元素可以作为 names 被下一个任务接收。"""

__input_files_max__ = 99
"""默认文件/文件夹数量上限(不是实际处理数量，而是输入参数个数)"""

MB = 1024 * 1024
"""用于方便计算文件体积"""


class Recipe(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of this recipe.

        应返回一个便于命令行输入的名称，比如中间不要有空格。
        注意：文件名以 'common_' 开头的文件会被忽略，不视为插件。
        """
        pass

    @property
    @abstractmethod
    def help(self) -> str:
        """Help messages.

        方便在命令行查看每个 recipe 的用途。如果不写清楚，使用者（包括一段时间之后的作者自己）
        就需要查看源文件才能知道具体使用方法了。通常用一个带注释的 TOML 文件即可。
        如果依赖第三方库，也可在这里注明。
        """
        pass

    @property
    @abstractmethod
    def default_options(self) -> dict:
        """默认选项，具体项目可根据需要自由决定。"""
        pass

    @abstractmethod
    def validate(self, names: list[str], options: dict) -> ErrMsg:
        """检查参数并进行初始化。

        注意：插件制作者必须保证 validate 是安全的，不可对文件进行任何修改。
             包括文件内容、日期、权限等等任何修改都不允许。
        """
        self.is_validated = True  # 在 dry_run, exec 中确认已检查
        return ""

    @abstractmethod
    def dry_run(self) -> Result:
        """在不修改文件的前提下尝试运行，尽可能多收集信息预测真实运行的结果。

        比如，检查文件是否存在、将被修改的文件名等等。注意，与 validate 方法一样，
        插件制作者必须保证 dry_run 是安全的，不可对文件进行任何修改。
        """
        assert self.is_validated, "在执行 dry_run 之前必须先执行 validate"
        print(f"There's no dry_run for {self.name}.")
        return [], ""

    @abstractmethod
    def exec(self) -> Result:
        """只有这个方法才真正操作文件，其它方法一律不可操作文件。"""
        assert self.is_validated, "在执行 exec 之前必须先执行 validate"
        return [], ""


class Task(TypedDict):
    recipe: str
    names: list[str]
    options: dict


class Plan(TypedDict):
    """一个计划可包含一个或多个任务，可与 TOML 文件互相转换。"""
    tasks: list[Task]


def new_plan(obj: dict[str, Any] = None) -> Plan:
    plan = Plan(tasks=[])
    if not obj:
        return plan

    if "tasks" in obj:
        for i, v in enumerate(obj["tasks"]):
            v = cast(dict, v)
            task = Task(recipe="", names=[], options={})
            task["recipe"] = v.get("recipe", "")
            task["names"] = v.get("names", [])
            task["options"] = v.get("options", {})
            obj["tasks"][i] = task
        plan["tasks"] = obj["tasks"]

    return plan


Recipes = dict[str, Type[Recipe]]
__recipes__: Recipes = {}


def register(recipe: Type[Recipe]):
    r = recipe()
    name = r.name

    # 由于 ABC@abstractmethod 不能确保一个方法是否被设置了 @property,
    # 因此只要手动检查。
    if not isinstance(name, str):
        name = r.name()  # type:ignore

    assert isinstance(r.name, str), f"{name}.name should be a property"
    assert isinstance(r.help, str), f"{name}.help should be a property"
    assert isinstance(
        r.default_options, dict
    ), f"{name}.default_options should be a property"

    assert name not in __recipes__, f"{name} already exists"
    __recipes__[name] = recipe


def init_recipes(folder: str) -> None:
    """注册 folder 里的全部插件。

    注意：文件名以 'common_' 开头的文件会被加载，但不注册为插件。
    """
    recipes_files = Path(folder).glob("*.py")
    for file_path in recipes_files:
        module_name = file_path.stem
        spec = importlib.util.spec_from_file_location(module_name, file_path)

        assert spec is not None
        assert spec.loader is not None

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        if file_path.name.startswith("common_"):
            # 以 'common_' 开头的文件会被加载，但不注册为插件。
            continue

        register(module.__recipe__)


def check_plan(plan: Plan) -> ErrMsg:
    """做一些简单的检查"""
    if not plan["tasks"]:  # 如果 tasks 是空列表
        return "no task"

    for task in plan["tasks"]:
        recipe = task["recipe"]
        if not recipe:
            return "recipe cannot be empty"
        if recipe not in __recipes__:
            return f"not found recipe: {recipe}"
    return ""


def must_exist(names: list[str] | list[Path]) -> ErrMsg:
    """names 是文件/文件夹的路径，全部存在时返回空字符串。"""
    for name in names:
        if isinstance(name, str):
            name = Path(name)
        if not name.exists():
            return f"not found: {name}"
    return ""


def must_folders(names: list[str] | list[Path]) -> ErrMsg:
    """必须全是文件夹"""
    for name in names:
        if isinstance(name, str):
            name = Path(name)
        if not name.is_dir():
            return f"'{name}' should be a directory"
    return ""


def must_files(names: list[str] | list[Path]) -> ErrMsg:
    """必须全是文件"""
    for name in names:
        if isinstance(name, str):
            name = Path(name)
        if not name.is_file():
            return f"'{name}' should be a file"
    return ""


def filter_files(names: list[Path]) -> list[Path]:
    """只要文件，不要文件夹"""
    return [x for x in names if x.is_file()]


def filesize_limit(name: str | Path, limit: int) -> ErrMsg:
    """限制文件体积不可超过 limit (单位:MB)"""
    if isinstance(name, str):
        name = Path(name)
    filesize = name.lstat().st_size / MB
    if filesize > limit:
        return f"{name}\nfile size ({filesize:.2f} MB) exceeds the limit ({limit} MB)\n"
    return ""


def names_limit(
    names: list[str], min: int, max: int = __input_files_max__
) -> tuple[list[str], ErrMsg]:
    """清除 names 里的空字符串，并且限定其上下限。"""

    temp = map(lambda name: name.strip(), names)
    names = list(filter(lambda name: name != "", temp))
    expected = ""
    size = len(names)
    if min == max and size != min:
        expected = f"exactly {min} names"
    elif size < min:
        expected = f"names.length > {min}"
    elif size > max:
        expected = f"names.length <= {max}"

    if expected:
        expected = f"expected: {expected}, got: {names}"
        names = []
    return names, expected


def get_bool(options: dict, key: str) -> tuple[bool, ErrMsg]:
    v = options.get(key, False)
    if not isinstance(v, bool):
        return False, f"Please set {key} to 'true' or 'false'"
    return v, ""
