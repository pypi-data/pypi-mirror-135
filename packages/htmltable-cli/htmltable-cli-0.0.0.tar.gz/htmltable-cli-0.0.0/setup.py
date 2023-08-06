# type: ignore

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    rqeuirements = fh.readlines()

setuptools.setup(
    name="htmltable-cli",
    description="command line tool to generate html tables with embedded audios and images",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    scripts=["htmltable.py"],
    install_requires=rqeuirements)
