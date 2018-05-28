from setuptools import setup

setup(
    name="takahe",
    version="0.1.0",
    packages=['takahe'],
    install_requires=["networkx", "pygraphviz"],
    include_package_data=True)
