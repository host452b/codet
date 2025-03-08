from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codet",
    version="0.4.0",
    author="clemente0620",
    author_email="clemente0620@gmail.com",
    description="A cross-platform command-line tool for file processing and Git repository analysis with support for commit history tracking, code hotspot detection, and customizable filtering options",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clemente0731/codet",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorlog>=6.0.0",
        "gitpython>=3.1.0",
        "typing>=3.7.4",
        "prettytable>=3.12.0",
        "tqdm>=4.60.0",
    ],
    entry_points={
        "console_scripts": [
            "codet=codet.cli:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "isort>=5.9.1",
            "flake8>=3.9.2",
            "twine>=3.4.1",
        ],
    },
) 