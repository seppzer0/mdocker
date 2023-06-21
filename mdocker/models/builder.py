import os

import mdocker.tools.messages as msg
import mdocker.tools.commands as ccmd


class ImageBuilder:
    """An Docker image builder."""

    def __init__(self, config: dict) -> None:
        self._name = config.get("name")
        self._platforms = config.get("platform", None)
        self._file = config.get("file", "Dockerfile")
        self._context = config.get("context", None)
        self._clean = config.get("clean", None)
        self._push = config.get("push", None)

    @staticmethod
    def _prepare_x_instance() -> None:
        """Create a temporary Buildx instance."""
        instance = "mdocker_instance"
        # remove the instance from the machine, just in case
        ccmd.launch(f"docker buildx stop {instance}", quiet=True, dont_exit=True)
        ccmd.launch(f"docker buildx rm {instance}", quiet=True, dont_exit=True)

    def run(self):
        """Run the image building process."""
        msg.note("Launching multiplatform Docker image build..")
        self._prepare_x_instance()
         # form platform list (including default value) and launch the build
        platforms = []
        if self._platforms:
            platforms = self._platforms.split(",")
        else:
            # get host arch as target, with "linux" being default os
            print("\n")
            msg.note("Using host arch as default target..")
            os_ = "linux"
            arch_ = ccmd.launch("uname -m", get_output=True)
            platforms = [os_ + "/" + arch_]
        for platform in platforms:
            # substitude x86_64 with amd64
            if "x86_64" in platform:
                msg.note("Substituding x86_64 with amd64")
                platform = platform.replace("x86_64", "amd64")
            print("\n")
            msg.note("Building for platform: {}".format(platform))
            tag = self._name + ":" + platform.split("/")[1]
            commands = [
                "docker buildx create --use --name multi --platform", platform, "--driver-opt", "network=host",
                "docker buildx build --no-cache --platform", platform, "--load", "-f", self._file, self._context, "-t", tag,
                "docker buildx stop multi",
                "docker buildx rm multi",
                "docker buildx prune --force"
            ]
            for cmd in commands:
                ccmd.launch(cmd)
            # [optional] push image to registry
            if self._push:
                ccmd.launch("docker push", tag)
        # [optional] clean Docker cache
        if self._clean:
            images = ["moby/buildkit:buildx-stable-1"]
            # add built images to cleanup list
            for platform in platforms:
                images.append(self._name + ":" + platform.split("/")[1].replace("x86_64", "amd64"))
            # cleanup, including dangling images
            for img in images:
                ccmd.launch("docker rmi", img)
            ccmd.launch('docker rmi $(docker images -f dangling="true" -aq)', dont_exit=True)
        print("\n")
        msg.done("Multiarch Docker image build finished!")
        print("\n")