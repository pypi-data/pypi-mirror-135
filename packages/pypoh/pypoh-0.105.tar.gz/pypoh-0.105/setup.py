from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pypoh",
    packages=["pypoh"],
    version="0.105",
    license="MIT",
    description="A Python Wrapper for the Proof of Humanity Rest API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Luciano Bruna",
    author_email="lucianobruna007@gmail.com",
    url="https://github.com/jamesluc007",
    download_url="https://github.com/jamesluc007/pypoh/archive/refs/tags/v_0105.tar.gz",
    keywords=["PROOF", "HUMANITY", "ETHEREUM", "BLOCKCHAIN"],
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
