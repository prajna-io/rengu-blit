"""Setup for blit"""

from os import path

from setuptools import find_packages, setup

PROJECT_ROOT = path.abspath(path.dirname(__file__))

with open(path.join(PROJECT_ROOT, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

requires_extra = {
    "dev": ["GitPython", "pylint", "black"],
    "optional": [
        "Jinja2",
    ],
}
requires_extra["all"] = [m for v in requires_extra.values() for m in v]

setup(
    name="blit",
    version="6.0",
    description="Companion to Rengu used for managing binary objects",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://prajna.io",
    author="Thornton K. Prime",
    author_email="thornton.prime@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    install_requires=["Click", "cmd2"],
    extras_require=requires_extra,
    entry_points={
        "console_scripts": [
            "blit=blit.cli:cli",
        ],
        "blit_cli": [
            "info = blit.cli.info:info",
        ],
        "blit_store": [],
        "blit_metadata": [],
    },
)
