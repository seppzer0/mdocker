from abc import ABC, abstractmethod
from subprocess import CompletedProcess


class IImageBuilder(ABC):
    """An interface for Docker image builder."""

    @abstractmethod
    def _builder_instance_clear(self) -> list[CompletedProcess | str | None]:
        """Clear the builder instance."""
        raise NotImplementedError()

    def _builder_instance_create(self, platform: str) -> CompletedProcess | str | None:
        """Create new builder instance."""
        raise NotImplementedError()

    @abstractmethod
    def _gen_build_cmds(self, platform: str) -> list[str]:
        """Generate a list of Docker Buildx commands."""
        raise NotImplementedError()

    @abstractmethod
    def run(self) -> None:
        """Execute the logic."""
        raise NotImplementedError()
