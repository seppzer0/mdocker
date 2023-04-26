import os
import sys
import pytest
import subprocess


test_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data"
)
@pytest.mark.parametrize(
    "arguments",
    [
        ["--file", "Dockerfile", "--context", test_path],
        ["--platform", "linux/arm64", "--file", "Dockerfile" "--context", test_path],
        ["--platform", "linux/amd64,linux/arm64", "--file", "Dockerfile" "--context", test_path]
    ]
)
def test__build_image__check(arguments):
    """
    Run a test build.
    """
    test_image_name = "mdockertest"
    cmd = ["python3", "-m", "mdocker", test_image_name, "--clean"] + arguments
    subprocess.run(cmd, check=True)
    subprocess.check_output(["docker", "images"])
    #cmd = "python3 -m mdocker {} --clean{}".format(image_name, case)
    #print("[SCENARIO] {}\n".format(cmd))
    #subprocess.run(cmd, shell=True, check=True)
