import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 0):
    sys.exit(
        """
######################################
# Python 3 is needed #
######################################
"""
    )

setup(
    name="navabilitysdk",
    version="0.0.1",
    license="Apache",
    author="NavAbility",
    package_dir={"": "src"},
    include_package_data=True,
    packages=find_packages("src", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    # entry_points={"console_scripts": ["navability = navability.main:cli"]},
    python_requires=">=3.5",
    download_url="https://github.com/NavAbility/NavAbilitySDK.py/archive/refs/tags/v0.0.1.tar.gz",
    long_description="NavAbility SDK",
    install_requires=[
        "click>=8.0.0,<9",
        "gql[all]==3.0.0a6",
        "marshmallow==3.14.0",
        "numpy==1.21.4",
        # Dev/test dependencies
        "black==21.9b0",
        "flake8==4.0.1",
        "pytest==6.2.5",
    ],
)
