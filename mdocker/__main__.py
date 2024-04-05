import os
import io
import sys
import argparse
from pathlib import Path

from mdocker.tools import commands as ccmd, messages as msg
from mdocker.models import ImageBuilder


def parse_args() -> argparse.Namespace:
    """Parse arguments."""
    args = None if sys.argv[1:] else ["-h"]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "name",
        help="specify a name for the image"
    )
    parser.add_argument(
        "--context",
        dest="bcontext",
        help="specify a path to build context"
    )
    parser.add_argument(
        "--file",
        dest="dfile",
        default=Path("Dockerfile"),
        help="specify a path to Dockerfile"
    )
    parser.add_argument(
        "--platforms",
        default=[
            f"linux/{ccmd.launch('uname -m', get_output=True, quiet=True).replace('x86_64', 'amd64')}"
        ],
        help="specify target platforms (e.g., --platforms linux/amd64,linux/arm64)"
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="push image to remote registry"
    )
    return parser.parse_args(args)


def validate_env() -> None:
    """Check and validate build environment."""
    # try calling "buildx" directly
    try:
        ccmd.launch("docker buildx version", quiet=True, dont_exit=True)
    except Exception:
        # attempt to enable buildx via environment variable
        msg.note("Attempting to enable buildx via environment variable..")
        os.environ["DOCKER_BUILDKIT"] = "1"
        ccmd.launch("docker buildx version", quiet=True)
        print("[ + ] Done!")


def process_platforms(platforms: str | list[str]) -> list[str]:
    """Process target platform list."""
    if not isinstance(platforms, list):
        return platforms.replace("x86_64", "amd64").split(",")
    else:
        return platforms


def main(args: argparse.Namespace) -> None:
    # for logs to show in order in various CI/CD / Build systems
    sys.stdout = io.TextIOWrapper(open(sys.stdout.fileno(), "wb", 0), write_through=True)
    validate_env()
    ImageBuilder(
        name=args.name,
        bcontext=args.bcontext,
        dfile=args.dfile,
        platforms=process_platforms(args.platforms),
        push=args.push
    ).run()


if __name__ == "__main__":
    main(parse_args())
