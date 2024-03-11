rem (**R**os **E**nvironment **M**anager) is a tool based on Docker, which allows you to easily manage multiple versions of ROS environments and brings you the same coding experience as on your local machine.

# feature
- Utilizes the same user and password as the host machine, and does not require local building of Docker images.
- Supports NVIDIA GPU acceleration for tools like Gazebo (requires the installation of `NVIDIA drivers` and `Docker NVIDIA Container Toolkit`).
- Supports from ROS1 Kinetic to the latest ROS2 Rolling, with Zsh and Bash.
- Since the home directory is mounted, shell configurations, Git configurations, Anaconda environments, and all other software installed in the home directory can be used normally.
- Integrates with VSCode's Dev Container feature, allowing the use of the local development environment inside the container.
- By building images locally, you can also easily define various dependencies for a project by modifying configurations, supporting automatic installation of dependencies for apt, ROS, Python, and npm.

# Usage

rem only depends on Python and Docker and can be installed via pip.
```shell
pip install -r requirements.txt
pip install -e .
rem init
```

The syntax of rem is similar to Docker's, but differs in its usage: `rem <action> <ros_distro_name>` instead of `docker <action> <image/container name>`.

For example, you can create a ROS Noetic environment with `rem build noetic`, enter this virtual environment with `rem exec/attach noetic`, and similarly use commands like `start`, `stop`, `rm`, `ps`, etc.

To integrate with VSCode, you need to install the DevContainer plugin and redefine a terminal in VSCode.
```json
"terminal.integrated.defaultProfile.linux": "zsh_rem",
"terminal.integrated.profiles.linux": {
    "zsh_rem": {
        "path": "/entrypoint.sh"
    }
}
```

## Known limitations

- Does not support AMD GPU acceleration
- Due to the difference in Ubuntu's password encryption algorithm, it is necessary to manually enter the user password on Kinetic and Melodic
- If there is a significant discrepancy between the host machine's operating system and the ROS environment's operating system, there may be some configurations is not universally applicable.
