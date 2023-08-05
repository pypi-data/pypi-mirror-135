import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="gs-dbs-client",
    version="0.2.5-35",
    description="python wrapper for the Glass Sphere DBS",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://glass-sphere-ai.de",
    author="Glass Sphere Software",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["gsdbs"],
    include_package_data=True,
    install_requires=["gql==3.0.0a5", "pandas","PyYAML","requests","aiohttp"],
    entry_points={
        "console_scripts": [
            "realpython=gsdbs.__main__:main",
        ]
    },
)
