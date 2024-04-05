from abc import ABC, abstractmethod
from subprocess import CompletedProcess


class IImageBuilder(ABC):
    """An interface for Docker image builder."""

    @abstractmethod
    def _builder_instance_clear(self) -> list[CompletedProcess | str]:
        """Clear the builder instance from the host machine."""
        raise NotImplementedError()

    @abstractmethod
    def _builder_instance_create(self) -> CompletedProcess | str | None:
        """Create new builder instance."""
        raise NotImplementedError()

    @abstractmethod
    def _gen_build_cmds(self) -> list[str]:
        """Generate a list of Docker Buildx commands."""
        raise NotImplementedError()

    @abstractmethod
    def run(self) -> None:
        """Run the logic."""
        raise NotImplementedError()
