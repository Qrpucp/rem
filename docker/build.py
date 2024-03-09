import json
import subprocess

# open config file in docker
with open("./config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

python_install_commands = ["pip", "install"]
apt_install_commands = ["apt-get", "install", "-y"]
npm_install_commands = ["npm", "install", "-g"]

project_num = len(config["project"])
project_name = []
project_ros_deps = []
project_python_deps = []
project_apt_deps = []
project_npm_deps = []

for i in range(project_num):
    project_name.append(next(iter(config["project"][i])))
    project_apt_deps.append(config["project"][i][project_name[i]]["apt_deps"])
    project_ros_deps.append(config["project"][i][project_name[i]]["ros_deps"])
    project_python_deps.append(config["project"][i][project_name[i]]["python_deps"])
    project_npm_deps.append(config["project"][i][project_name[i]]["npm_deps"])
    for j in range(len(project_apt_deps[i])):
        apt_install_commands.append(project_apt_deps[i][j])
    for j in range(len(project_ros_deps[i])):
        # apt_install_commands.append("ros-${ROS_DISTRO}-" + project_ros_deps[i][j])
        apt_install_commands.append("ros-noetic-" + project_ros_deps[i][j])
    for j in range(len(project_python_deps[i])):
        python_install_commands.append(project_python_deps[i][j])
    for j in range(len(project_npm_deps[i])):
        npm_install_commands.append(project_npm_deps[i][j])

subprocess.run(apt_install_commands, check=True)
subprocess.run(python_install_commands, check=True)
subprocess.run(npm_install_commands, check=True)
