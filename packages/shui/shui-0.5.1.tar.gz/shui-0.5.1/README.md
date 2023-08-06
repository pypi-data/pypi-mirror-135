# SHUI
Spark-Hadoop Unix Installer

![OSes](https://img.shields.io/badge/system-macOS%7CLinux%7CFreeBSD-green)
![Architectures](https://img.shields.io/badge/arch-i686%7Cx86__64-yellowgreen)

[![Python](https://img.shields.io/pypi/pyversions/shui.svg?logo=python&logoColor=white)](https://pypi.org/project/shui)
[![PyPI version](https://badge.fury.io/py/shui.svg)](https://badge.fury.io/py/shui)
[![PyPI downloads](https://img.shields.io/pypi/dm/shui)](https://img.shields.io/pypi/dm/shui)
[![Code style](https://github.com/jemrobinson/shui/workflows/check-code-style/badge.svg)](https://github.com/jemrobinson/shui/actions)
[![Functionality](https://github.com/jemrobinson/shui/workflows/test-functionality/badge.svg)](https://github.com/jemrobinson/shui/actions)

This package uses Python to download and unpack a pre-built version of Spark/Hadoop from Apache.
Its primary use-case is simplifying unattended installs where the user wants "the latest available version" of these tools.

## Features

- download Spark/Hadoop release tarball from Apache.
- verify the tarball using the SHA512 sum provided by Apache.
- unpack the tarball to a target directory on your local system.

## Installation

First you'll need to install `shui` using pip: `pip install shui`.

## Usage

### Versions
The `versions` command shows you all available Spark/Hadoop versions.

```
USAGE
  shui versions [--latest]

OPTIONS
  --latest               Show only the latest available version

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question
```

### Install
The `install` command will download, verify and install a particular Spark/Hadoop version.

```
USAGE
  shui install [--latest] [--spark <...>] [--hadoop <...>] [--target <...>]

OPTIONS
  --latest               Use the latest available version
  --spark                Spark version (default: "any")
  --hadoop               Hadoop version (default: "any")
  --target               Directory to install into (default: "cwd")

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question
```
