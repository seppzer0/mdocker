from abc import ABC, abstractmethod
from subprocess import CompletedProcess


class IImageBuilder(ABC):
    """An interface for building Docker images."""

    @abstractmethod
    def _builder_instance_clear(self) -> list[CompletedProcess]:
        """Clear the builder instance from the host machine."""
        raise NotImplementedError()

    @abstractmethod
    def _builder_instance_create(self) -> CompletedProcess:
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
