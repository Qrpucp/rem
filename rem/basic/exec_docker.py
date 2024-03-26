import subprocess
import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout, colorize=True, format="<level>{level}:</level> <level>{message}</level>"
)

logger.info("exec container...")

uid = subprocess.getoutput("id -u")
group = subprocess.getoutput("id -g -n")
gid = subprocess.getoutput("id -g")

# Enable local connections from the root user to the X server
subprocess.run("xhost +local:root", shell=True, check=True, stdout=subprocess.DEVNULL)

# Execute a command inside a running Docker container
try:
    subprocess.run(f"docker exec -it {sys.argv[1]} /exec.sh", shell=True)
finally:
    # Disable local root connections to the X server, ensuring this runs even if the previous command fails
    subprocess.run(
        "xhost -local:root", shell=True, check=True, stdout=subprocess.DEVNULL
    )
