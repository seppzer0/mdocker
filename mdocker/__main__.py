import io
import os
import sys
import argparse
import subprocess
import mdocker.tools.commands
import mdocker.tools.messages as msg


def parse_args():
    """
    Parse arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("name",
                        help="select a name for the image")
    parser.add_argument("--context",
                        default=".",
                        help="define path to build context")
    parser.add_argument("--file",
                        default=".{}Dockerfile".format(os.sep),
                        help="define path to Dockerfile")
    parser.add_argument("--platform",
                        help="select platforms to build Docker image for (e.g., --platform linux/amd64,linux/arm64)")
    parser.add_argument("--push",
                        action="store_true",
                        help="push image to remote registry")
    parser.add_argument("--clean",
                        action="store_true",
                        help="clean cache after the build")
    global args
    args = parser.parse_args()


def validate():
    """
    Check and validate build environment.
    """
    # try calling "buildx" directly
    try:
        cmdd(["docker", "buildx", "version"], quiet=True, dont_exit=True)
    except Exception as e:
        # attempt to enable buildx via environment variable
        msg.note("Attempting to enable buildx via environment variable..")
        os.environ["DOCKER_BUILDKIT=1"]
        cmdd("docker buildx version", quiet=True)
        print("[ + ] Done!")


# prepare environment
parse_args()
sys.stdout = io.TextIOWrapper(open(sys.stdout.fileno(), 'wb', 0), write_through=True)
validate()
# just in case, remove potentially existing "multi" builder
cmdd(["docker", "buildx", "stop", "multi"], quiet=True, dont_exit=True)
cmdd(["docker", "buildx", "rm", "multi"], quiet=True, dont_exit=True)
msg.note("Launching multiarch Docker image build..")
# form platform list (including default value) and launch the build
platforms = []
if args.platform:
    platforms = args.platform.split(",")
else:
    # get host arch as target, with "linux" being default os
    print("\n")
    msg.note("Using host arch as default target..")
    os = "linux"
    arch = subprocess.check_output(["uname", "-m"]).decode("utf-8").splitlines()[0].lower()
    platforms = [os + "/" + arch]
for platform in platforms:
    # substitude x86_64 with amd64
    if "x86_64" in platform:
        msg.note("Substituding x86_64 with amd64")
        platform = platform.replace("x86_64", "amd64")
    print("\n")
    msg.note("Building for platform: {}".format(platform))
    tag = args.name + ":" + platform.split("/")[1]
    commands = [
        ["docker", "buildx", "create", "--use", "--name", "multi", "--platform", platform, "--driver-opt", "network=host"],
        ["docker", "buildx", "build", "--no-cache", "--platform", platform, "--load", "-f", args.file, args.context, "-t", tag],
        ["docker", "buildx", "stop", "multi"],
        ["docker", "buildx", "rm", "multi"],
        ["docker", "buildx", "prune", "--force"]
    ]
    for cmd in commands:
        cmdd(cmd)
    # [optional] push image to registry
    if args.push:
        cmdd(["docker", "push", tag])
# [optional] clean Docker cache
if args.clean:
    images = ["moby/buildkit:buildx-stable-1"]
    # add built images to cleanup list
    for platform in platforms:
        images.append(args.name + ":" + platform.split("/")[1].replace("x86_64", "amd64"))
    # cleanup, including dangling images
    for img in images:
        cmdd(["docker", "rmi", img])
    cmdd(['docker', 'rmi', '$(docker', 'images', '-f', 'dangling="true"', '-aq'], dont_exit=True)
print("\n")
msg.done("Multiarch Docker image build finished!")
print("\n")
