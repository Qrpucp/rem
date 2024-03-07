from loguru import logger
from pathlib import Path
import subprocess
import os


class UserHandler:
    def __init__(self, config_path, use_cache):
        self.use_cache = use_cache
        self.config_path = config_path

    def copyHostUserFiles(self):
        logger.warning(
            f"""\nPermissions are required to read files. \nNote that this will not damage any content.""")

        # delete and create the host directory
        subprocess.run("rm -rf " + self.config_path + "/host", shell=True)
        Path(self.config_path + "/host").mkdir(exist_ok=True)

        subprocess.run(
            f"sudo cp /etc/passwd /etc/shadow {self.config_path}/host", shell=True)
        subprocess.run(
            f"sudo chmod 644 {self.config_path}/host/shadow", shell=True)
        subprocess.run(
            f"mv {self.config_path}/host/shadow {self.config_path}/host/shadow.bak", shell=True)
        subprocess.run(
            f"mv {self.config_path}/host/passwd {self.config_path}/host/passwd.bak", shell=True)

    def generateUserFiles(self):
        user = os.getenv('USER')
        # delete files except *.bak
        # subprocess.run(f"find {self.config_path}/host -type f | grep -v '\.bak$' | xargs rm",
        #                shell=True, stderr=subprocess.DEVNULL)
        # group
        subprocess.run(
            f"cp {self.config_path}/noetic/group {self.config_path}/host/group", shell=True)
        subprocess.run(
            f"echo 'rem:x:123:{user}' >> {self.config_path}/host/group", shell=True)
        subprocess.run(
            f"echo '{user}:x:1000:' >> {self.config_path}/host/group", shell=True)
        # sudoers
        subprocess.run(
            f"cp {self.config_path}/noetic/sudoers {self.config_path}/host/sudoers", shell=True)
        subprocess.run(
            f"echo '%rem ALL=(ALL:ALL) ALL' >> {self.config_path}/host/sudoers", shell=True)
        # shadow
        subprocess.run(
            f"cp {self.config_path}/noetic/shadow {self.config_path}/host/shadow", shell=True)
        lines_with_user = []
        with open(f"{self.config_path}/host/shadow.bak", 'r') as file:
            for line in file:
                if user in line:
                    lines_with_user.append(line.strip())
        for line in lines_with_user:
            subprocess.run(
                f"echo '{line}' >> {self.config_path}/host/shadow", shell=True)
        # passwd
        subprocess.run(
            f"cp {self.config_path}/noetic/passwd {self.config_path}/host/passwd", shell=True)
        lines_with_user = []
        with open(f"{self.config_path}/host/passwd.bak", 'r') as file:
            for line in file:
                if user in line:
                    lines_with_user.append(line.strip())
        for line in lines_with_user:
            subprocess.run(
                f"echo '{line}' >> {self.config_path}/host/passwd", shell=True)
        # chown
        files = ["group", "passwd", "shadow", "sudoers"]
        for file in files:
            subprocess.run(
                f"sudo chown root:root {self.config_path}/host/{file}", shell=True)

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


if __name__ == '__main__':
    config_path = os.path.abspath(__file__ + "/../../../config")
    user_handler = UserHandler(config_path, True)
    user_handler.run()
