import json
import os
import subprocess
import sys

from loguru import logger

from rem.utils.docker_wrapper import DockerWrapper
from rem.utils.user_handler import UserHandler
from rem.utils.utils import checkNvidiaGpu, initLogger

config = {}
config_path = display = local_host = user = uid = group = gid = ""


def getConfig() -> None:
    global config_path, config
    config_path = os.path.abspath(__file__ + "/../../../config")
    with open(config_path + "/config.json", "r", encoding="utf8") as file:
        config = json.load(file)


def getEnv() -> None:
    global display, local_host, user, uid, group, gid
    display = os.getenv("DISPLAY", ":1")
    local_host = os.uname()[1]
    user = os.getenv("USER")
    uid = subprocess.getoutput("id -u")
    group = subprocess.getoutput("id -g -n")
    gid = subprocess.getoutput("id -g")


def getDockerImage(distro_name: str) -> str:
    docker_wrapper_local = DockerWrapper(f"local/rem:{distro_name}", "")
    docker_wrapper_remote = DockerWrapper(f"qrpucp/rem:{distro_name}", "")
    if docker_wrapper_local.checkImage():
        return f"local/rem:{distro_name}"
    elif docker_wrapper_remote.checkImage():
        return f"qrpucp/rem:{distro_name}"
    else:
        logger.error(
            "Docker image not found, you should first pull or build the image."
        )
        sys.exit()


if __name__ == "__main__":

    initLogger()
    getConfig()
    getEnv()

    distro_name = container_name = sys.argv[1]
    image_name = getDockerImage(distro_name)

    docker_wrapper = DockerWrapper(image_name, container_name)

    if config["auto_remove"]:
        docker_wrapper.stopContainer()
        docker_wrapper.removeContainer()
    else:
        if docker_wrapper.checkContainer():
            logger.warning("Please remove the existed container first.")
            sys.exit()

    logger.info("create and start container...")

    # Start docker container
    # fmt: off
    docker_run_command = [
        "docker", "run", "-it", "-d",
        "--privileged=true",
        "--name", container_name,
        # apollo x11
        "-e", f"DISPLAY={display}",
        "-e", "REM_CONTAINER=1",
        # "-e", f"DOCKER_USER={user}",
        "-e", f"USER={user}",
        # "-e", f"DOCKER_USER_ID={uid}",
        # "-e", f"DOCKER_GRP={group}",
        # "-e", f"DOCKER_GRP_ID={gid}",
        "-e", f"XDG_RUNTIME_DIR={os.getenv('XDG_RUNTIME_DIR')}",
        "-v", f"{os.getenv('XDG_RUNTIME_DIR')}:{os.getenv('XDG_RUNTIME_DIR')}",
        "-v", "/dev/input:/dev/input",
        "--network", "host",
        # ref: https://answers.ros.org/question/336963/rosout-high-memory-usage/
        # "--ulimit", "nofile=1024:524288"
        "--ulimit", "nofile=524288:524288"
    ]
    # fmt: on

    if checkNvidiaGpu():
        # fmt: off
        nvidia_gpu_command = [
            "--gpus", "all",
            "-e", "NVIDIA_DRIVER_CAPABILITIES=all",
        ]
        # fmt: on
        docker_run_command.extend(nvidia_gpu_command)

    user_handler = UserHandler(config_path, True, distro_name)
    user_handler.run()
    # fmt: off
    user_config_command = [
        "-u", f"{uid}:{gid}",
        "-v", f"{config_path}/host/group:/etc/group:ro",
        "-v", f"{config_path}/host/passwd:/etc/passwd:ro",
        "-v", f"{config_path}/host/sudoers:/etc/sudoers:ro",
        "-v", f"/home/{user}:/home/{user}",
        "-v",
    ]
    if distro_name in ("melodic", "kinetic"):
        user_config_command.append(f"{config_path}/host/shadow_sha512:/etc/shadow:ro")
    else:
        user_config_command.append(f"{config_path}/host/shadow_yescrypt:/etc/shadow:ro")
    # fmt: on
    docker_run_command.extend(user_config_command)

    # if config["auto_config_user"]:
    #     if distro.id() == "arch":
    #         sudo_checker = SudoChecker(config_path, True)
    #         sudo_check_flag = sudo_checker.run()
    #         user_config_command = [
    #             "-u", f"{uid}:{gid}",
    #             # "-v", "/etc/group:/etc/group:ro",
    #             # "-v", f"{config_path}/group:/etc/group:ro",
    #             "-v", "/etc/passwd:/etc/passwd:ro",
    #             "-v", "/etc/shadow:/etc/shadow:ro",
    #             # "-v", "/etc/sudoers.d:/etc/sudoers.d:ro",
    #             "-v", f"/home/{user}:/home/{user}",
    #         ]
    #         # if sudo_check_flag:
    #         #     user_config_command.append("-v")
    #         #     user_config_command.append(
    #         #         f"{config_path}/sudoers:/etc/sudoers")
    #         # else:
    #         #     user_config_command.append("-v")
    #         #     user_config_command.append("/etc/sudoers:/etc/sudoers:ro")
    #         docker_run_command.extend(user_config_command)
    #     else:
    #         logger.warning(
    #             "Only Ubuntu systems support automatic configuration of local users. For other systems wishing to use local users, please recompile the Docker image.")

    mount_dir_num = len(config["mount_dir"])
    for i in range(mount_dir_num):
        docker_run_command.append("-v")
        docker_run_command.append(
            config["mount_dir"][i] + ":/root/" + config["mount_dir"][i].split("/")[-1]
        )

    if config["memory_limit"] != 0:
        docker_run_command.append("-m")
        docker_run_command.append(str(config["memory_limit"]) + "g")

    docker_run_command.append(image_name)

    subprocess.run(docker_run_command, check=True, stdout=subprocess.DEVNULL)
