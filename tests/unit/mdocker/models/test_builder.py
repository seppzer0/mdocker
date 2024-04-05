import pytest

from mdocker.models import ImageBuilder


@pytest.mark.parametrize(
    "config, res_expected",
    (
        (
            {
                "name": "mdocker-test",
                "dfile": "Dockerfile",
                "bcontext": ".",
                "push": False,
                "clean": False,
                "platforms": ["linux/amd64"]
            },
            [
                "docker buildx build --no-cache --platform linux/amd64 --load -f Dockerfile . -t mdocker-test:amd64",
                "docker buildx stop multi_instance",
                "docker buildx rm multi_instance",
                "docker buildx prune --force"
            ],
        ),
        (
            {
                "name": "mdocker-test",
                "dfile": "Dockerfile.test",
                "bcontext": "..",
                "push": True,
                "clean": False,
                "platforms": ["linux/amd64", "macos/arm64"]
            },
            [
                "docker buildx build --no-cache --platform linux/amd64 --load -f Dockerfile.test .. -t mdocker-test:amd64",
                "docker buildx stop multi_instance",
                "docker buildx rm multi_instance",
                "docker buildx prune --force",
                "docker push mdocker-test:amd64",
                "docker buildx build --no-cache --platform macos/arm64 --load -f Dockerfile.test .. -t mdocker-test:arm64",
                "docker buildx stop multi_instance",
                "docker buildx rm multi_instance",
                "docker buildx prune --force",
                "docker push mdocker-test:arm64"
            ]
        )
    )
)
def test__gen_build_cmds__check(config: dict[str, any], res_expected: list[str]) -> None:
    """Check the list of returned "docker buildx" commands."""
    instance = ImageBuilder(**config)
    res_actual = instance._gen_build_cmds()
    assert res_expected == res_actual
