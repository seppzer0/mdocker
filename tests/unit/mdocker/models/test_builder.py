import pytest

from mdocker.models.builder import ImageBuilder


@pytest.mark.parametrize(
    "platforms_string",
    ("linux/amd64", "linux/arm64", "linux/amd64,linux/arm64", "linux/x86_64", "linux/x86_64,linux/arm64")
)
class TestGenPlatforms:

    """A grouping class for testing the _gen_platforms() method."""

    def test__gen_platforms__same_amount(self, platforms_string: str) -> None:
        """Test the amount of generated platforms."""
        instance = ImageBuilder({"name": "mdocker-test", "platform": platforms_string})
        res_expected = len(platforms_string.split(","))
        res_actual = len(instance._platforms)
        assert res_expected == res_actual

    def test__gen_platforms__x86_64_substitution(self, platforms_string: str) -> None:
        """Test the x86_64 -> amd64 substitution."""
        instance = ImageBuilder({"name": "mdocker-test", "platform": platforms_string})
        res_actual = instance._platforms
        assert "x86_64" not in " ".join(res_actual)

@pytest.mark.parametrize(
    "config, res_expected",
    (
        (
            {
                "name": "mdocker-test",
                "push": False,
            },
            [
                "docker buildx create --use --name multi_instance --platform linux/amd64 --driver-opt network=host",
                "docker buildx build --no-cache --platform linux/amd64 --load -f Dockerfile . -t mdocker-test:amd64",
                "docker buildx stop multi_instance",
                "docker buildx rm multi_instance",
                "docker buildx prune --force"
            ],
        ),
        (
            {
                "name": "mdocker-test",
                "file": "Dockerfile.test",
                "context": "..",
                "push": True,
                "platform": "linux/x86_64"
            },
            [
                "docker buildx create --use --name multi_instance --platform linux/amd64 --driver-opt network=host",
                "docker buildx build --no-cache --platform linux/amd64 --load -f Dockerfile.test .. -t mdocker-test:amd64",
                "docker buildx stop multi_instance",
                "docker buildx rm multi_instance",
                "docker buildx prune --force",
                "docker push mdocker-test:amd64"
            ]
        )
    )
)
def test__gen_docker_cmds__check(config: dict[str, any], res_expected: list[str]) -> None:
    """Check the list of returned "docker buildx" commands."""
    instance = ImageBuilder(config)
    res_actual = instance._gen_docker_cmds()
    print(res_actual)
    print("\n")
    print(res_expected)
    assert res_expected == res_actual
