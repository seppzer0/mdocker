# mdocker

An easy-to-use wrapper for multi-platform Docker image builds.

## Contents

- [mdocker](#mdocker)
  - [Contents](#contents)
  - [Description](#description)
  - [Usage](#usage)
  - [Examples](#examples)
  - [Installation](#installation)
    - [From PyPI (recommended)](#from-pypi-recommended)
    - [Local from source](#local-from-source)
    - [No installation, direct run from source](#no-installation-direct-run-from-source)
  - [License](#license)

## Description

mdocker is a simple wrapper over Docker Buildx, which can be used for convenient image builds targeted for multiple platforms.

This tool was originally designed as a workaround to a [limitation](https://github.com/docker/buildx/issues/59) that Buildx has with the `--load` parameter.

> [!NOTE]
> *There are, however, some [workarounds and progress](https://github.com/docker/roadmap/issues/371) towards this issue.*

The amount of target platforms specified for this wrapper will be equal to the amount of tags generated in local cache.

E.g., if `linux/arm64` and `linux/amd64` were specified as target platforms for a `demo` image, you will get `demo:arm64` and `demo:amd64` built and stored within your local cache.

## Usage

mdocker requires an installation of Python 3.10+.

Below is a help message with the description of arguments.

```help
$ python3 -m mdocker --help
usage: [-h] [--context BCONTEXT] [--file DFILE] [--platforms PLATFORMS] [--push] name

positional arguments:
  name                  specify a name for the image

options:
  -h, --help            show this help message and exit
  --context BCONTEXT    specify a path to build context
  --file DFILE          specify a path to Dockerfile
  --platforms PLATFORMS
                        specify target platforms (e.g., --platforms linux/amd64,linux/arm64)
  --push                push image to remote registry
```

## Examples

You can try building the Dockerfile in this project with mdocker itself!

The command below will build the image for both `amd64` and `arm64` target architectures:

```sh
python3 -m mdocker demo --platforms linux/amd64,linux/arm64
```

Optionally, you can specify paths to the build context and Dockerfile:

```sh
python3 -m mdocker demo --context . --file ./Dockerfile --platforms linux/amd64,linux/arm64
```

## Installation

### From PyPI (recommended)

To install latest mdocker package from PyPI, use:

```sh
python3 -m pip install mdocker
```

### Local from source

To install and debug mdocker locally, in the root of repository use:

```sh
python3 -m pip install -e .
```

### No installation, direct run from source

To run mdocker without any installation into local cache, in the root of repository use:

```sh
export PYTHONPATH=$(pwd)
python3 -m poetry install --no-root
python3 mdocker <arguments>
```

## License

[MIT](#license)
