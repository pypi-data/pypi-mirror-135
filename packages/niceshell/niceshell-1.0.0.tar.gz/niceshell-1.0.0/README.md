# niceshell - Python 3 module for better shell coding

## Requirements

* Python 3.6+ (tested on 3.6.0)

## Installation

### Automatic installation

```bash
python3 -m pip install niceshell
```

### Manual installation

```bash
cd /tmp/
version=1.0.0 # Choose desired version
wget -c "https://github.com/Andrew15-5/niceshell/releases/download/v${version}/niceshell-${version}-py3-none-any.whl"
python3 -m pip -U --user install niceshell-${version}-py3-none-any.whl
```

## Usage

```python
from niceshell import *
ext = "py"

process1 = ls(f"*.{ext}", batch=True)
if process1.exit_code():
    print("No Python scripts here. :(")
    print("stderr:", process1.error_output(), end='')
    exit(1)

process2 = ls(f"*.{ext}", True).shell("head -n 5")
print("stdout:", process2.output(), end='')
files = process2.get_lines()

ln(files, "/tmp/").wait()
```

## Important note

Due to different preferences among coders some things like:

* raised error instead of silencly returned error code or None
* type of raised error and its message;
* behavior of edge cases (the way parameter's data is handled);
* parameter names and their ordinal position
* behavior of command with provided input text (with sudo)

can be inconvenient to some extent for someone and be perfect for others.
Therefore, I encourage everyone to test result of each function, method,
variable, constant, etc. to be 100% sure of how your
script/program/app will handle every situation.

There are some tests in "tests" directory (./niceshell/tests/) to get you
started. And of course you can see implementation of whatever the module
provides for better understanding of what you are looking for.

## Complete list of modules and their functions/classes

>Note: list can be exteneded in future updates.

* \_\_init__
  * GID   ($USER's group ID)
  * GROUP ($USER's group name)
  * HOME  ($USERS's home dir aka '~')
  * UID   ($USER's ID)
  * USER  ($USER)
* core
  * expose_tilde()
  * normalize_short_and_long_args()
  * quotes_wrapper()
  * shell()
  * Shell
  * ShortArgsOption
* extra
  * force_sudo_password_promt()
  * get_root_privileges()
  * get_root_privileges_or_exit()
  * has_root_privileges()
* gnu_coreutils
  * cd()
  * cp()
  * ln()
  * ls()
  * mv()
  * rm()

## TODO list

* [x] Add ability to install module via pip
* [x] Add ability to get command's output and pipe it to another command
* [x] Add function that check if sudo can be used without password
* [x] Add ability to provide input to command in core.Shell
* [x] Add cd
* [x] Add mv
* [x] Add rm
* [x] Add cp
* [x] Add shell() function for chain to start from small 's'
* [x] Add remaining Popen methods/properties to Shell class
