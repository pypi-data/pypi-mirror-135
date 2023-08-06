from typing import Iterable, Union

from .core import Shell


def cd(path: str = '',
       short_args: Union[str, Iterable[str]] = [],
       test: bool = False) -> Union[Shell, str]: ...


def cp(source_path: Union[str, Iterable[str]],
       destination_path: str,
       short_args: Union[str, Iterable[str]] = [],
       long_args: Iterable[str] = [],
       batch: bool = False,
       sudo: bool = False,
       test: bool = False) -> Union[Shell, str]: ...


def ln(source_path: Union[str, Iterable[str]],
       destination_path: str,
       short_args: Union[str, Iterable[str]] = [],
       long_args: Iterable[str] = [],
       batch: bool = False,
       sudo: bool = False,
       test: bool = False) -> Union[Shell, str]: ...


def ls(path: Union[str, Iterable[str]] = '',
       short_args: Union[str, Iterable[str]] = [],
       long_args: Iterable[str] = [],
       batch: bool = False,
       sudo: bool = False,
       test: bool = False) -> Union[Shell, str]: ...


def mv(source_path: Union[str, Iterable[str]],
       destination_path: str,
       short_args: Union[str, Iterable[str]] = [],
       long_args: Iterable[str] = [],
       batch: bool = False,
       sudo: bool = False,
       test: bool = False) -> Union[Shell, str]: ...


def pwd(short_args: Union[str, Iterable[str]] = [],
        test: bool = False) -> Union[str, Shell]: ...


def rm(path: Union[str, Iterable[str]],
       short_args: Union[str, Iterable[str]] = [],
       long_args: Iterable[str] = [],
       batch: bool = False,
       sudo: bool = False,
       test: bool = False) -> Union[Shell, str]: ...
