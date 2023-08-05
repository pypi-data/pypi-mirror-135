import os
import setuptools

_VERSION = "1.1.0-10"

DEPENDENCY_LINKS = [

]
# with open('../../requirements.txt') as f:
#     REQUIRED_PACKAGES = f.read().splitlines()

REQUIRED_PACKAGES = [
    "innocuous-api>=1.1.1-4"
]

setuptools.setup(
    name="innocuous-sdk",
    version=_VERSION,
    description="Innocuous Book SDK",
    install_requires=REQUIRED_PACKAGES,
    dependency_links=DEPENDENCY_LINKS,
    packages = ["innocuous_sdk"],
    zip_safe = False,
    author="Noam Rosenberg",
    author_email="noamsrosenberg@gmail.com",
    url="",
    keywords=["innocuousbook"]
)
