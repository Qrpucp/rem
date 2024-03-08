from setuptools import setup

setup(
    name="rem",
    version="1.0",
    author="qrpucp",
    author_email="qrpucp@qq.com",
    description="",
    packages=["rem"],
    entry_points={
        "console_scripts": [
            "rem=rem.rem:main",
        ],
    },
)
