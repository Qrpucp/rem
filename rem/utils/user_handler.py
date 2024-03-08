import os
import subprocess
import sys
from pathlib import Path

from loguru import logger


class UserHandler:
    def __init__(self, external_config_path, external_use_cache):
        self.use_cache = external_use_cache
        self.config_path = external_config_path

    def copyHostUserFiles(self):
        logger.warning(
            "\nPermissions are required to read files."
            "\nNote that this will not damage any content."
        )

        # delete and create the host directory
        subprocess.run("rm -rf " + self.config_path + "/host", shell=True, check=True)
        Path(self.config_path + "/host").mkdir(exist_ok=True)

        subprocess.run(
            f"sudo cp /etc/passwd /etc/shadow {self.config_path}/host",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"sudo chmod 644 {self.config_path}/host/shadow", shell=True, check=True
        )
        subprocess.run(
            f"mv {self.config_path}/host/shadow {self.config_path}/host/shadow.bak",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"mv {self.config_path}/host/passwd {self.config_path}/host/passwd.bak",
            shell=True,
            check=True,
        )

    def generateUserFiles(self):
        user = os.getenv("USER")
        if user is None:
            logger.error("Unable to obtain environment variables")
            sys.exit()

        # delete files except *.bak
        # subprocess.run(f"find {self.config_path}/host -type f | grep -v '\.bak$' | xargs rm",
        #                shell=True, stderr=subprocess.DEVNULL)

        # group
        subprocess.run(
            f"cp {self.config_path}/noetic/group {self.config_path}/host/group",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"echo 'rem:x:123:{user}' >> {self.config_path}/host/group",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"echo '{user}:x:1000:' >> {self.config_path}/host/group",
            shell=True,
            check=True,
        )
        # sudoers
        subprocess.run(
            f"cp {self.config_path}/noetic/sudoers {self.config_path}/host/sudoers",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"echo '%rem ALL=(ALL:ALL) ALL' >> {self.config_path}/host/sudoers",
            shell=True,
            check=True,
        )
        # shadow
        subprocess.run(
            f"cp {self.config_path}/noetic/shadow {self.config_path}/host/shadow",
            shell=True,
            check=True,
        )
        lines_with_user = []
        with open(f"{self.config_path}/host/shadow.bak", "r", encoding="utf8") as file:
            for line in file:
                if user in line:
                    lines_with_user.append(line.strip())
        for line in lines_with_user:
            subprocess.run(
                f"echo '{line}' >> {self.config_path}/host/shadow",
                shell=True,
                check=True,
            )
        # passwd
        subprocess.run(
            f"cp {self.config_path}/noetic/passwd {self.config_path}/host/passwd",
            shell=True,
            check=True,
        )
        lines_with_user = []
        with open(f"{self.config_path}/host/passwd.bak", "r", encoding="utf8") as file:
            for line in file:
                if user in line:
                    lines_with_user.append(line.strip())
        for line in lines_with_user:
            subprocess.run(
                f"echo '{line}' >> {self.config_path}/host/passwd",
                shell=True,
                check=True,
            )
        # chown
        files = ["group", "passwd", "shadow", "sudoers"]
        for file in files:
            subprocess.run(
                f"sudo chown root:root {self.config_path}/host/{file}",
                shell=True,
                check=True,
            )

    def fileExist(self):
        files = ["/", "/group", "/passwd", "/shadow", "/sudoers"]
        for file in files:
            if not Path(self.config_path + "/host" + file).exists():
                return False
        return True

    def run(self):
        if self.use_cache and self.fileExist():
            pass
        else:
            self.copyHostUserFiles()
            self.generateUserFiles()


if __name__ == "__main__":
    config_path = os.path.abspath(__file__ + "/../../../config")
    user_handler = UserHandler(config_path, True)
    user_handler.run()
