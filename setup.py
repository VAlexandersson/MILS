# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="text-splitter",
    version="0.1.0",
    description="A tool for splitting markdown files into chunks",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/text-splitter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "text-splitter=text_splitter.main:main",
        ],
    },
)