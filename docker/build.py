import json
import subprocess
import sys

distro_name = sys.argv[1]

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
custom_commands = []
project_scripts = []
executed_scripts = []


for i in range(project_num):
    project_name.append(next(iter(config["project"][i])))
    project_apt_deps.append(config["project"][i][project_name[i]]["apt_deps"])
    project_ros_deps.append(config["project"][i][project_name[i]]["ros_deps"])
    project_python_deps.append(config["project"][i][project_name[i]]["python_deps"])
    project_npm_deps.append(config["project"][i][project_name[i]]["npm_deps"])
    custom_commands.append(config["project"][i][project_name[i]]["custom_cmds"])
    project_scripts.append(config["project"][i][project_name[i]]["scripts"])

    if config["project"][i][project_name[i]]["distro"] != distro_name:
        continue
    if not config["project"][i][project_name[i]]["install"]:
        continue

    for j in range(len(project_apt_deps[i])):
        apt_install_commands.append(project_apt_deps[i][j])
    for j in range(len(project_ros_deps[i])):
        # to be compatible with python2 in kinetic.
        apt_install_commands.append(
            "ros-{}-".format(distro_name) + project_ros_deps[i][j]
        )
    for j in range(len(project_python_deps[i])):
        python_install_commands.append(project_python_deps[i][j])
    for j in range(len(project_npm_deps[i])):
        npm_install_commands.append(project_npm_deps[i][j])
    for j in range(len(custom_commands[i])):
        if not custom_commands[i][j]:
            continue
        subprocess.run(custom_commands[i][j], shell=True, check=True)
    for j in range(len(project_scripts[i])):
        if not project_scripts[i][j]:
            continue
        if not project_scripts[i][j] in executed_scripts:
            subprocess.run(
                "/usr/bin/bash /root/scripts/" + project_scripts[i][j],
                shell=True,
                check=True,
            )
            executed_scripts.append(project_scripts[i][j])

if len(apt_install_commands) > 3:
    subprocess.run(apt_install_commands, check=True)
if len(python_install_commands) > 2:
    subprocess.run(python_install_commands, check=True)
if len(npm_install_commands) > 3:
    subprocess.run(npm_install_commands, check=True)
