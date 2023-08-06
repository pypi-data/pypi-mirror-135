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

_version = "0.1.3"

setup(
    name="navabilitysdk",
    version=_version,
    license="Apache-2.0",
    author="NavAbility",
    author_email="info@navability.io",
    package_dir={"": "src"},
    include_package_data=True,
    packages=find_packages("src", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    # entry_points={"console_scripts": ["navability = navability.main:cli"]},
    python_requires=">=3.8",
    download_url=f"https://github.com/NavAbility/NavAbilitySDK.py/archive/refs/tags/v{_version}.tar.gz",  # noqa: E501, B950
    long_description="""NavAbility SDK: Access NavAbility Cloud factor graph features from Python.
Note that this SDK and the related API are still in development. Please let us know if you have any issues at info@navability.io.""",
    install_requires=[
        "click>=8.0.0,<9",
        "gql[all]==3.0.0a6",
        "marshmallow==3.14.0",
        "numpy>=1.21",
        # Dev/test dependencies
        "black==21.9b0",
        "flake8==4.0.1",
        "pytest==6.2.5",
    ],
)
