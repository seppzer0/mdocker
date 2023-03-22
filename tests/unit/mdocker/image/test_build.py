import os
import subprocess


def test_build():
    """Run a test build."""
    image_name = "mdockertest"
    #subprocess.run("python3 -m pip install pip --upgrade", shell=True, check=True)
    #subprocess.run("python3 -m pip install -e ../../mdocker", shell=True, check=True)
    # various arguments for various cases
    cases = [
        "",
        " --platform linux/arm64",
        " --platform linux/amd64,linux/arm64"
    ]
    for counter, case in enumerate(cases, 1):
        print("\n=== RUNNING CASE {} ===".format(counter))
        cmd = "python3 -m mdocker {} --clean{}".format(image_name, case)
        print("[SCENARIO] {}\n".format(cmd))
        subprocess.run(cmd, shell=True, check=True)


# launch
test_build()
