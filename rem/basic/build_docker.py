import subprocess
import sys
import os

image_name = sys.argv[1]

root_path = os.path.abspath(__file__ + "/../../..")
print(root_path)

subprocess.run(
    ["cp", f"{root_path}/config/config.json", f"{root_path}/docker"],
    check=True,
)

subprocess.run(
    ["docker", "build", "-t", f"{image_name}", f"{root_path}/docker"],
    check=True,
)

subprocess.run(
    ["rm", f"{root_path}/docker/config.json"],
    check=True,
)
