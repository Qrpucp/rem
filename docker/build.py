import json
import os
import subprocess

# open config file in docker
with open("./config.json", "r") as file:
    config = json.load(file)

install_commands = [
    "apt-get", "install", "-y"
]

project_num = len(config["project"])
project_name = []
project_deps = []
for i in range(project_num):
    project_name.append(next(iter(config["project"][i])))
    project_deps.append(config["project"][i][project_name[i]])
    for j in range(len(project_deps[i])):
        install_commands.append(project_deps[i][j])

subprocess.run(install_commands, check=True)
