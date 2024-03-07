import subprocess
import re
from packaging import version
from loguru import logger
from pathlib import Path


class SudoChecker:
    """
    https://unix.stackexchange.com/questions/244064/why-are-the-include-and-includedir-directives-in-sudo-prefixed-with-the-pound
    """

    def __init__(self, config_path, use_cache) -> None:
        self.use_cache = use_cache
        self.config_path = config_path
        Path(self.config_path).mkdir(exist_ok=True)

    def getSudoVersion(self) -> str:
        raw_text = subprocess.getoutput("sudo --version")
        pattern = r"\b(\d+\.\d+\.\d+)(?:p\d+)?"
        matches = re.findall(pattern, raw_text)
        if matches:
            self.version = max(matches, key=version.parse)

    def copyAndModifySudoers(self) -> None:
        subprocess.run("sudo cp /etc/sudoers " + self.config_path, shell=True)
        subprocess.run(f"sudo chmod 644 " + self.config_path + "/sudoers", shell=True)
        subprocess.run(
            f"sudo sed -i 's/@include/#include/g' '" + self.config_path + "/sudoers'",
            shell=True,
        )
        subprocess.run(f"sudo chmod 440 " + self.config_path + "/sudoers", shell=True)

    def run(self) -> bool:
        sudoers_path = self.config_path + "/sudoers"
        if self.use_cache and Path(sudoers_path).exists():
            return 1

        self.getSudoVersion()
        if version.parse(self.version) >= version.parse("1.9.1"):
            logger.warning(
                f"""\nYour sudo version is {self.version}, which is greater than 1.9.1. \nThere might be incompatibilities in syntax. \nTherefore, permissions are required to read the sudoers file to copy it. \nNote that this will not damage any content."""
            )
            try:
                self.copyAndModifySudoers()
            except:
                logger.error("\nFailed to obtain permission")
                exit()
            return 1
        else:
            return 0
