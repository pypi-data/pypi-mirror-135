import os
from setuptools import setup, find_packages


def readme(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as file:
        return file.read()


setup(
    name="ua_email_client",
    version="0.1.7",
    packages=find_packages(),
    author="Ryan Johannes-Bland",
    author_email="rjjohannesbland@email.arizona.edu",
    description=(
        "Provides easy interface for sending emails through Amazons Simple "
        "Email Service."
    ),
    long_description=readme("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/UACoreFacilitiesIT/UA-Email-Client",
    license="MIT",
    install_requires=["boto3", "jinja2", "datetime"],
)
