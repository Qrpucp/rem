#!python3
import argparse
import os
import subprocess
import sys


def main():
    actions = ["build", "run", "exec", "attach"]
    action_descriptions = [
        "Build docker image using the dockerfile.",
        "Create the container based on the image.",
        "Exec into the container.",
        "Attach to the container.",
    ]
    parser = argparse.ArgumentParser(description="")

    subparsers = parser.add_subparsers(dest="action", help="")

    init_parser = subparsers.add_parser(
        "init",
        help="Configure the terminal to automatically source the ROS environment.",
    )

    ros_distro = ["rolling", "humble", "foxy", "noetic", "melodic", "kinetic"]

    for action, description in zip(actions, action_descriptions):
        action_parser = subparsers.add_parser(action, help=description)
        action_parser.add_argument(
            "distro", help="Ros distro name.", choices=ros_distro
        )

    if len(sys.argv) == 1:
        parser.print_usage(sys.stderr)
        sys.exit()

    args = parser.parse_args()

    basic_func_path = os.path.abspath(__file__ + "/../basic")

    if args.action == "init":
        # fmt: off
        subprocess.run("echo -e '\n# Automatically generated by rem\nif [[ \"$REM_CONTAINER\" == \"1\" ]]; then\n    source /opt/ros/$ROS_DISTRO/setup.zsh\nfi' >> ~/.zshrc", shell=True, check=True)
        # fmt: on
    elif args.action == "build":
        subprocess.run(
            ["python3", f"{basic_func_path}/build_docker.py", f"{args.distro}"],
            check=True,
        )
    elif args.action == "run":
        subprocess.run(
            ["python3", f"{basic_func_path}/run_docker.py", f"{args.distro}"],
            check=True,
        )
    elif args.action == "exec":
        subprocess.run(
            ["python3", f"{basic_func_path}/exec_docker.py", f"{args.distro}"],
            check=True,
        )
    elif args.action == "attach":
        subprocess.run(
            ["python3", f"{basic_func_path}/attach_docker.py", f"{args.distro}"],
            check=True,
        )


if __name__ == "__main__":
    main()
