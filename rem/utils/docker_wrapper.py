import sys

from loguru import logger

import docker


class DockerWrapper:
    def __init__(self, image_name, container_name) -> None:
        self.client = docker.from_env()
        self.image_name = image_name
        self.container_name = container_name
        if not self.checkImage():
            logger.error("image not found")
            sys.exit()

    def checkImage(self) -> bool:
        try:
            self.client.images.get(self.image_name)
            return True
        except Exception:
            return False

    def checkContainer(self) -> bool:
        try:
            self.client.containers.get(self.container_name)
            return True
        except Exception:
            return False

    def startContainer(self) -> bool:
        try:
            container = self.client.containers.get(self.container_name)
            logger.info("start container...")
            container.start()
            return True
        except Exception:
            return False

    def stopContainer(self) -> bool:
        try:
            container = self.client.containers.get(self.container_name)
            logger.info("stop container...")
            container.stop()
            return True
        except Exception:
            return False

    def removeContainer(self) -> bool:
        try:
            container = self.client.containers.get(self.container_name)
            if container.status == "running":
                self.stopContainer()
            logger.info("remove container...")
            container.remove()
            return True
        except Exception:
            return False

    def CreateContainer(self) -> None:
        pass
