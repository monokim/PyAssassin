from setuptools import setup

setup(name="gym_tank",
      version="0.1",
      author="A.I. Noob",
      license="MIT",
      packages=["gym_tank", "gym_tank.envs"],
      install_requires = ["gym", "pygame", "numpy"]
)
