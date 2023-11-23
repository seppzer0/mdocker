import mdocker.tools.messages as msg
import mdocker.tools.commands as ccmd


class ImageBuilder:
    """Image builder."""

    _instance = "multi_instance"

    def __init__(self, config: dict) -> None:
        self._name = config.get("name")
        self._file = config.get("file", "Dockerfile")
        self._context = config.get("context", ".")
        self._clean = config.get("clean", False)
        self._push = config.get("push", False)
        self._platforms_string = config.get("platform", None)

    def _clear_builder_instance(self) -> None:
        """Create a temporary Buildx instance."""
        # remove the instance from the machine, just in case
        ccmd.launch(f"docker buildx stop {self._instance}", quiet=True, dont_exit=True)
        ccmd.launch(f"docker buildx rm {self._instance}", quiet=True, dont_exit=True)

    @property
    def _platforms(self) -> list[str]:
        """Form a collection of target platforms.

        For the terms of Docker Buildx, "x86_64" is replaced with "amd64".
        """
        platforms = []
        if self._platforms_string:
            platforms = self._platforms_string.replace("x86_64", "amd64").split(",")
        else:
            # get host arch as target, with "linux" being default OS
            msg.note("Using host arch as default target..")
            os_ = "linux"
            arch_ = ccmd.launch("uname -m", get_output=True).replace("x86_64", "amd64")
            platforms = [f"{os_}/{arch_}"]
        return platforms

    def _gen_docker_cmds(self) -> list[str]:
        """Generate a list of Docker Buildx commands."""
        for platform in self._platforms:
            # only <arch> value is used in tag extension
            tag = f'{self._name}:{platform.split("/")[1]}'
            commands = [
                "docker buildx create --use --name {} --platform {} --driver-opt network=host"\
                    .format(self._instance, platform),
                "docker buildx build --no-cache --platform {} --load -f {} {} -t {}"\
                    .format(platform, self._file, self._context, tag),
                "docker buildx stop {}"\
                    .format(self._instance),
                "docker buildx rm {}"\
                    .format(self._instance),
                "docker buildx prune --force"
            ]
            # optionally push image to registry
            if self._push:
                commands.append(f"docker push {tag}")
            return commands

    def run(self) -> None:
        """Run the image building process."""
        msg.note("Launching multiplatform Docker image build..")
        self._clear_builder_instance()
        for cmd in self._gen_docker_cmds():
            ccmd.launch(cmd)
        msg.done("Multiarch Docker image build finished!")
