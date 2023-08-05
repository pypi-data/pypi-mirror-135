import setuptools
from pathlib import Path

setuptools.setup(
    name='gym_kuka',
    version='0.0.1',
    description="A OpenAI Gym Env for Kuka iiwa robot arm",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="gym_kuka*"),
    install_requires=['gym']  # And any other dependencies foo needs
)
