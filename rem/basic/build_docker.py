import os
import subprocess
import sys
from pathlib import Path

distro_name = image_name = sys.argv[1]

root_path = os.path.abspath(__file__ + "/../../..")
print(root_path)

subprocess.run(
    ["cp", f"{root_path}/config/config.json", f"{root_path}/docker"],
    check=True,
)

if distro_name == "foxy":
    base_image = "osrf/ros:foxy-desktop"
else:
    base_image = f"osrf/ros:{distro_name}-desktop-full"

if distro_name == "melodic" or distro_name == "kinetic":
    nodejs_version = 16
else:
    nodejs_version = 20

try:
    subprocess.run(
        [
            "docker",
            "build",
            "--build-arg",
            f"base_image={base_image}",
            "--build-arg",
            f"nodejs_version={nodejs_version}",
            "--build-arg",
            f"distro={distro_name}",
            "-t",
            f"local/rem:{image_name}",
            f"{root_path}/docker",
        ],
        check=True,
    )
finally:
    if Path(f"{root_path}/docker/config.json").exists():
        subprocess.run(
            ["rm", f"{root_path}/docker/config.json"],
            check=True,
        )
