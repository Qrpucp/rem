import subprocess

subprocess.run(["apt-get", "install", "-y", "x11-apps"], check=True)
