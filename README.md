# mdocker — multiplatform Docker image builder

## Description

**mdocker** is a simple wrapper over Docker Buildx, which can be used for easy image building targeted for various platforms.

## Usage

mdocker takes some of the arguments used standard Docker Buildx argument list.

```help
$ python3 -m mdocker --help
usage: __main__.py [-h] [--context CONTEXT] [--dockerfile DOCKERFILE] [--platform PLATFORM] [--upload] [--clean]
                   name

positional arguments:
  name                  select a name for the image

optional arguments:
  -h, --help            show this help message and exit
  --context CONTEXT     define path to build context
  --dockerfile DOCKERFILE
                        define path to Dockerfile
  --platform PLATFORM   select platforms to build Docker image for (e.g., --platform linux/amd64,linux/arm64)
  --upload              upload image to remote registry
  --clean               clean cache after the build
```

## Local installation from sources

To install and debug mdocker locally, in the root of repository use:

```sh
python3 -m pip install -e .
```
