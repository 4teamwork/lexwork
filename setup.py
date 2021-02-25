import os

from setuptools import find_packages, setup

setup(
    name="lexwork",
    version="1.0.0dev0",
    description="API Client for Lexwork PDF Signer",
    long_description=open("README.rst").read() + "\n" + open("HISTORY.txt").read(),
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="lexwork api client apiclient",
    author="4teamwork AG",
    author_email="mailto:info@4teamwork.ch",
    url="https://github.com/4teamwork/lexwork.apiclient",
    license="GPL2",
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=["requests", "urllib3<2"],
)
