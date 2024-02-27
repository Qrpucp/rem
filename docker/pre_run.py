import subprocess

# subprocess.run(['echo', 'test'])
subprocess.run(['apt-get', 'install', '-y', 'x11-apps'], check=True)
