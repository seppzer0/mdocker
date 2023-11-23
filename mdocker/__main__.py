import os
import io
import sys
import argparse

import mdocker.tools.messages as msg
import mdocker.tools.commands as ccmd

from mdocker.models.builder import ImageBuilder


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
        help="specify a path to build context"
    )
    parser.add_argument(
        "--file",
        help="specify a path to Dockerfile"
    )
    parser.add_argument(
        "--platform",
        help="specify target platforms (e.g., --platform linux/amd64,linux/arm64)"
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="push image to remote registry"
    )
    return parser.parse_args(args)


def validate() -> None:
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


def main(args: argparse.Namespace) -> None:
    # for logs to always show in order
    sys.stdout = io.TextIOWrapper(open(sys.stdout.fileno(), 'wb', 0), write_through=True)
    # parse arguments and run
    parse_args()
    validate()
    config = vars(args)
    ImageBuilder(config).run()


if __name__ == "__main__":
    main(parse_args())
