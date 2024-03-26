# rem

rem (**R**os **E**nvironment **M**anager) is a tool based on Docker, which allows you to easily manage multiple versions of ROS environments and **brings you the same coding experience as on your local machine.**

## feature
- Xorg image forwarding and GPU acceleration.
- Same configuration and softwares between host machine and the virtual ROS environment. **No need to rebuild the image locally.**
- Easily integrates with VSCode [DevContainer](https://code.visualstudio.com/docs/devcontainers/containers).
- Easily configure project dependencies in the environment.


## Installation

rem depends on Python and Docker. You can install rem via pip with the following command:

```shell
pip install -r requirements.txt
pip install -e .
```

Configure the terminal to automatically source the ROS environment, supports both bash and zsh.
```shell
rem init
```

## Usage

rem's syntax is similar to Docker's but with some encapsulation. You can view all commands by running `rem -h`.

For instance, if you want to obtain a ROS Noetic environment, you first need to pull a remote image with `rem pull noetic`, or build a local image with `rem build noetic`.

Next, create and start the container by `running rem run noetic`.

Finally, enter the container for development by using `rem attach noetic` or `rem exec noetic`.

You can replace "noetic" with any other supported ROS version of your choice. And by adding your project configuration in [config.json](config/config.json), dependencies will be automatically installed when building the image locally.

To integrate with VSCode, you need to install the DevContainer plugin and configure in VSCode.

```json
"terminal.integrated.defaultProfile.linux": "zsh_rem",
"terminal.integrated.profiles.linux": {
    "zsh_rem": {
        "path": "/exec.sh"
    }
}
```

## Known limitations

- Currently does not support AMD GPU acceleration
- Due to the difference in Ubuntu's password encryption algorithm, it is necessary to manually enter the user password on Kinetic and Melodic
- If there is a significant discrepancy between the host machine's operating system and the ROS environment's operating system, there may be some configurations is not universally applicable.
- Ubuntu-16.04 lacks the libglvnd package, which results in the inability to use software requiring OpenGL, such as Gazebo and Rviz, when using nvidia-docker2. For more detailed information, please refer to [ros wiki](http://wiki.ros.org/docker/Tutorials/Hardware%20Acceleration#nvidia-docker2). You can manually resolve this issue by following the [instructions](https://github.com/NVIDIA/nvidia-docker/issues/534#issuecomment-436054364).
