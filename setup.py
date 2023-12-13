import os

from setuptools import find_packages, setup

import zefir_api


def load_req(r_file: str) -> list[str]:
    with open(os.path.join(os.getcwd(), r_file)) as f:
        return [
            r for r in (line.split("#", 1)[0].strip() for line in f.readlines()) if r
        ]


setup(
    name="zefir_api",
    packages=find_packages(".", exclude=["*tests*"]),
    version=zefir_api.__version__,
    install_requires=load_req("requirements.txt"),
    setup_requires="",
    python_requires=">=3.11",
    author="IDEA",
    author_email="office@idea.edu.pl",
    url="idea.edu.pl",
)
