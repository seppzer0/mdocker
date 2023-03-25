import os
import sys
import subprocess


def test_build():
    """Run a test build."""
    image_name = "mdockertest"
    subprocess.run("python3 -m pip install pip --upgrade", shell=True, check=True)
    #subprocess.run("python3 -m pip install -e ../mdocker", shell=True, check=True)
    # various arguments for various cases
    cases = [
        " --file {0}Dockerfile --context {0}".format(path_test_build),
        " --platform linux/arm64 --file {0}Dockerfile --context {0}".format(path_test_build),
        " --platform linux/amd64,linux/arm64 --file {0}Dockerfile --context {0}".format(path_test_build)
    ]
    for counter, case in enumerate(cases, 1):
        print("\n=== RUNNING CASE {} ===".format(counter))
        cmd = "python3 -m mdocker {} --clean{}".format(image_name, case)
        print("[SCENARIO] {}\n".format(cmd))
        subprocess.run(cmd, shell=True, check=True)


# launch
path_test_build = os.path.dirname(os.path.abspath(__file__)) + os.sep
test_build()
