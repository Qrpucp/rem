import subprocess
import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout, colorize=True, format="<level>{level}:</level> <level>{message}</level>"
)

logger.info("attach container...")

subprocess.run("xhost +local:root", shell=True, check=True, stdout=subprocess.DEVNULL)

try:
    subprocess.run(f"docker attach {sys.argv[1]}", shell=True)
finally:
    subprocess.run(
        "xhost -local:root", shell=True, check=True, stdout=subprocess.DEVNULL
    )
