import sys
import argparse
import subprocess


def parse_args():
    """Parse arguments."""
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",
                        help="enable pip module tests")
    parser.add_argument("--upload",
                        help="enable pip module upload")
    parser.add_argument("-u", "--username",
                        dest="username",
                        help="specify PyPI username")
    parser.add_argument("-p", "--password",
                        dest="password",
                        help="specify PyPI password/token")
    args = parser.parse_args()



def validate_args():
    """Validate specified arguments."""
    if (args.upload and args.upload.lower() == "true") and not (args.username and args.password):
        print("[ ! ] Upload enabled but no credentials passed.")
        sys.exit(1)


def ccmd(cmd):
    """Custom cmd wrapper."""
    print(f"[cmd] {cmd}")
    rc = subprocess.run(cmd, shell=True).returncode
    if rc != 0:
        print([f"[ ! ] Could not launch command: {cmd}"])
        sys.exit(1)


def build():
    """Build the pip module."""
    ccmd("python3 -m poetry build")


def test():
    """Test the pip module."""
    ccmd("python3 -m pytest tests")


def upload(usr, pswd):
    """Upload the pip module."""
    ccmd(f"python3 -m twine upload -u {usr} -p {pswd} -r pypi --repository-url https://upload.pypi.org/legacy/ dist/*")


# launch the pipeline
parse_args()
validate_args()
build()
if args.test and args.test.lower() == "true":
    test()
if args.upload and args.upload.lower() == "true":
    upload(args.username, args.password)
