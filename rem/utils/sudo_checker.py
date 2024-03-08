import re
import subprocess
import sys
from pathlib import Path

from loguru import logger
from packaging import version


class SudoChecker:
    """
    https://unix.stackexchange.com/questions/244064/why-are-the-include-and-includedir-directives-in-sudo-prefixed-with-the-pound
    """

    def __init__(self, external_config_path, external_use_cache) -> None:
        self.use_cache = external_use_cache
        self.config_path = external_config_path
        self.version = None
        Path(self.config_path).mkdir(exist_ok=True)

    def getSudoVersion(self) -> None:
        raw_text = subprocess.getoutput("sudo --version")
        pattern = r"\b(\d+\.\d+\.\d+)(?:p\d+)?"
        matches = re.findall(pattern, raw_text)
        if matches:
            self.version = max(matches, key=version.parse)
        else:
            logger.error("Unable to get sudo version")
            sys.exit()

    def copyAndModifySudoers(self) -> None:
        subprocess.run(
            "sudo cp /etc/sudoers " + self.config_path, shell=True, check=True
        )
        subprocess.run(
            "sudo chmod 644 " + self.config_path + "/sudoers", shell=True, check=True
        )
        subprocess.run(
            "sudo sed -i 's/@include/#include/g' '" + self.config_path + "/sudoers'",
            shell=True,
            check=True,
        )
        subprocess.run(
            "sudo chmod 440 " + self.config_path + "/sudoers", shell=True, check=True
        )

    def run(self) -> bool:
        sudoers_path = self.config_path + "/sudoers"
        if self.use_cache and Path(sudoers_path).exists():
            return True

        self.getSudoVersion()
        if self.version is None:
            logger.error("Unable to get sudo version")
            sys.exit()

        if version.parse(self.version) >= version.parse("1.9.1"):
            logger.warning(
                f"\nYour sudo version is {self.version}, which is greater than 1.9.1."
                "\nThere might be incompatibilities in syntax."
                "\nTherefore, permissions are required to read the sudoers file to copy it."
                "\nNote that this will not damage any content."
            )
            try:
                self.copyAndModifySudoers()
            except Exception:
                logger.error("\nFailed to obtain permission")
                sys.exit()
            return True
        return False
