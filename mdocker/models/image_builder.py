from pathlib import Path
from pydantic import BaseModel
from subprocess import CompletedProcess

from mdocker.tools import commands as ccmd, messages as msg
from mdocker.interfaces import IImageBuilder


class ImageBuilder(BaseModel, IImageBuilder):
    """A class for building Docker images.

    :param name: Docker image name.
    :param file: Path to Dockerfile.
    :param context: Path to build context.
    :param platforms: List of target platforms.
    :param push: Flag to push built Docker images to registry.
    """

    _instance: str = "multi-target"

    name: str
    dfile: Path
    bcontext: Path
    push: bool
    platforms: list[str]


    def _builder_instance_clear(self) -> list[CompletedProcess | str | None]:
        return [
            ccmd.launch(f"docker buildx stop {self._instance}", quiet=True, dont_exit=True),
            ccmd.launch(f"docker buildx rm {self._instance}", quiet=True, dont_exit=True)
        ]

    def _builder_instance_create(self, platform: str) -> CompletedProcess | str | None:
        return ccmd.launch(
            "docker buildx create --use --name {} --platform {} --driver-opt network=host"\
            .format(self._instance, ",".join(self.platforms))
        )

    def _gen_build_cmds(self, platform: str) -> list[str]:
        # only <arch> value is used in tag extension
        tag = f'{self.name}:{platform.split("/")[1]}'
        # define build commands
        b_cmds = [
            "docker buildx build --no-cache --platform {} --load -f {} {} -t {}"\
            .format(platform, self.dfile, self.bcontext, tag),
            "docker buildx stop {}"\
            .format(self._instance),
            "docker buildx rm {}"\
            .format(self._instance),
            "docker buildx prune --force"
        ]
        # optionally push image to registry
        if self.push:
            b_cmds.append(f"docker push {tag}")
        return b_cmds

    def run(self) -> None:
        msg.note("Launching multi-platform Docker image build..")
        for platform in self.platforms:
            self._builder_instance_clear()
            self._builder_instance_create(platform)
            [ccmd.launch(cmd) for cmd in self._gen_build_cmds(platform)]
            self._builder_instance_clear()
        msg.done("Multiarch Docker image build finished!")
