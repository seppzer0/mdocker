import os
import argparse

import mdocker.tools.messages as msg
from mdocker.tools.commands import ccmd
from mdocker.models.builder import ImageBuilder


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("name",
                        help="select a name for the image")
    parser.add_argument("--context",
                        default=".",
                        help="define path to build context")
    parser.add_argument("--file",
                        help="define path to Dockerfile")
    parser.add_argument("--platform",
                        help="select platforms to build Docker image for (e.g., --platform linux/amd64,linux/arm64)")
    parser.add_argument("--push",
                        action="store_true",
                        help="push image to remote registry")
    parser.add_argument("--clean",
                        action="store_true",
                        help="clean cache after the build")
    return parser.parse_args()


def validate() -> None:
    """Check and validate build environment."""
    # try calling "buildx" directly
    try:
        ccmd.launch("docker buildx version", quiet=True, dont_exit=True)
    except Exception:
        # attempt to enable buildx via environment variable
        msg.note("Attempting to enable buildx via environment variable..")
        os.environ["DOCKER_BUILDKIT=1"]
        ccmd.launch("docker buildx version", quiet=True)
        print("[ + ] Done!")


def main(args: argparse.Namespace) -> None:
    os.environ["PYTHONUNBUFFERED"] = "1"
    parse_args()
    validate()
    # create a config with arguments and run
    config = vars(args)
    ImageBuilder(config).run()


if __name__ == "__main__":
    main(parse_args())
