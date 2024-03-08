#!/bin/python
import argparse
import subprocess
import os


def main():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "action", choices=["init", "build", "run", "exec", "attach"], help=""
    )

    parser.add_argument("name", help="")

    args = parser.parse_args()

    basic_func_path = os.path.abspath(__file__ + "/../basic")

    if args.action == "init":
        pass
    elif args.action == "build":
        subprocess.run(
            ["python", f"{basic_func_path}/build_docker.py", f"{args.name}"], check=True
        )
    elif args.action == "run":
        subprocess.run(
            ["python", f"{basic_func_path}/run_docker.py", f"{args.name}"], check=True
        )
    elif args.action == "exec":
        subprocess.run(
            ["python", f"{basic_func_path}/exec_docker.py", f"{args.name}"], check=True
        )
    elif args.action == "attach":
        subprocess.run(
            ["python", f"{basic_func_path}/attach_docker.py", f"{args.name}"],
            check=True,
        )


if __name__ == "__main__":
    main()
