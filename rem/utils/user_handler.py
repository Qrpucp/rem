import os
import re
import subprocess
import sys
from pathlib import Path

from loguru import logger

from rem.utils.utils import generateSha512Passwd


class UserHandler:
    def __init__(self, external_config_path, external_use_cache, external_distro):
        self.use_cache = external_use_cache
        self.config_path = external_config_path
        self.distro = external_distro

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

    def generateShadowFiles(self) -> None:
        # ref: https://www.cyberciti.biz/faq/understanding-etcshadow-file/
        user = os.getenv("USER")
        if user is None:
            logger.error("Unable to obtain environment variables")
            sys.exit()

        if self.distro in ("melodic", "kinetic"):
            subprocess.run(
                f"cp {self.config_path}/ubuntu/shadow {self.config_path}/host/shadow_sha512",
                shell=True,
                check=True,
            )
            lines_with_user = []
            with open(
                f"{self.config_path}/host/shadow.bak", "r", encoding="utf8"
            ) as file:
                for line in file:
                    if user in line:
                        lines_with_user.append(line.strip())
            logger.warning(
                "Due to the differences in password encryption algorithms in Ubuntu 18.04 and 16.04, you need to enter the plaintext of the password to ensure consistency between the password in the container and the host machine."
            )
            user_input = input("Please input password:\n")
            sha512_crypt_passwd = generateSha512Passwd(user_input)
            for line in lines_with_user:
                new_line = (
                    f"{user}:" + sha512_crypt_passwd + ":" + line.split(":", 2)[2]
                )
                subprocess.run(
                    f"echo '{new_line}' >> {self.config_path}/host/shadow_sha512",
                    shell=True,
                    check=True,
                )
        else:
            subprocess.run(
                f"cp {self.config_path}/ubuntu/shadow {self.config_path}/host/shadow_yescrypt",
                shell=True,
                check=True,
            )
            lines_with_user = []
            with open(
                f"{self.config_path}/host/shadow.bak", "r", encoding="utf8"
            ) as file:
                for line in file:
                    if user in line:
                        lines_with_user.append(line.strip())
            for line in lines_with_user:
                subprocess.run(
                    f"echo '{line}' >> {self.config_path}/host/shadow_yescrypt",
                    shell=True,
                    check=True,
                )

    def generateUserFiles(self) -> None:
        user = os.getenv("USER")
        if user is None:
            logger.error("Unable to obtain environment variables")
            sys.exit()

        # delete files except *.bak
        # subprocess.run(f"find {self.config_path}/host -type f | grep -v '\.bak$' | xargs rm",
        #                shell=True, stderr=subprocess.DEVNULL)

        # group
        subprocess.run(
            f"cp {self.config_path}/ubuntu/group {self.config_path}/host/group",
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
            f"cp {self.config_path}/ubuntu/sudoers {self.config_path}/host/sudoers",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"echo '%rem ALL=(ALL:ALL) ALL' >> {self.config_path}/host/sudoers",
            shell=True,
            check=True,
        )
        # shadow
        self.generateShadowFiles()
        # passwd
        subprocess.run(
            f"cp {self.config_path}/ubuntu/passwd {self.config_path}/host/passwd",
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
        files = ["group", "passwd", "shadow_sha512", "shadow_yescrypt", "sudoers"]
        for file in files:
            if Path(f"{self.config_path}/host/{file}").exists():
                subprocess.run(
                    f"sudo chown root:root {self.config_path}/host/{file}",
                    shell=True,
                    check=True,
                )

    def yescryptShadowFileExist(self) -> bool:
        files = ["/", "/group", "/passwd", "/shadow_yescrypt", "/sudoers"]
        for file in files:
            if not Path(self.config_path + "/host" + file).exists():
                return False
        return True

    def sha512ShadowFileExist(self) -> bool:
        files = ["/", "/group", "/passwd", "/shadow_sha512", "/sudoers"]
        for file in files:
            if not Path(self.config_path + "/host" + file).exists():
                return False
        return True

    def run(self):
        if self.distro in ("melodic", "kinetic"):
            if self.use_cache and self.sha512ShadowFileExist():
                return
            elif self.use_cache and self.yescryptShadowFileExist():
                self.generateShadowFiles()
                return
        else:
            if self.use_cache and self.yescryptShadowFileExist():
                return
            elif self.use_cache and self.sha512ShadowFileExist():
                self.generateShadowFiles()
                return

        self.copyHostUserFiles()
        self.generateUserFiles()


if __name__ == "__main__":
    config_path = os.path.abspath(__file__ + "/../../../config")
    user_handler = UserHandler(config_path, True, "noetic")
    user_handler.run()
