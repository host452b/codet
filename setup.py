from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codet",
    version="0.2.0",
    author="clemente0620",
    author_email="clemente0620@gmail.com",
    description="一个跨平台的命令行文件处理工具",
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
        "click>=8.0.0",
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