import os
import shutil
import sys

from loguru import logger
from passlib.hash import sha512_crypt


def checkNvidiaGpu() -> bool:
    if shutil.which("nvidia-smi") is None:
        return False
    return True


def getDefaultShell() -> str:
    shell = os.getenv("SHELL")
    if shell is None:
        return ""
    else:
        return shell.split("/")[-1]


def initLogger() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<level>{level}:</level> <level>{message}</level>",
    )


def generateSha512Passwd(passwd: str) -> str:
    return sha512_crypt.hash(passwd)
