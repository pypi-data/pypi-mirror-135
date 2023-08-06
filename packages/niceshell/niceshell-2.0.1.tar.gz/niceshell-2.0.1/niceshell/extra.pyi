from typing import List, Tuple, Union

from .extra import *


def force_sudo_password_promt() -> None: ...
def get_root_privileges() -> bool: ...
def get_root_privileges_or_exit(exit_code: int) -> None: ...
def has_root_privileges() -> bool: ...


def list_dirs(
    path: str = '.',
    hidden: bool = True,
    non_hidden: bool = True,
    with_errors: bool = False) -> Union[List[str], Tuple[List[str], str]]: ...


def list_files(
    path: str = '.',
    hidden: bool = True,
    non_hidden: bool = True,
    with_errors: bool = False) -> Union[List[str], Tuple[List[str], str]]: ...
