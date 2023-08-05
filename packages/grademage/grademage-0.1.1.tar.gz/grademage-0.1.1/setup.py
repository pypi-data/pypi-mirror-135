from setuptools import find_packages, setup

setup(
    name="grademage",
    version="0.1.1",
    description="Module to grade online quiz.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Samuel Zhang",
    author_email="qisamuelzhang@hotmail.com",
    url="https://github.com/yiyitech/grademage",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    setup_requires=[],
    install_requires=["requests"],
)
