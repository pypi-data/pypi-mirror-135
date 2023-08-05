import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aoc-lib", # Replace with your own username
    version="1.1.3",
    author="Seppo",
    author_email="aoc@possner.de",
    description="Some helper functions for advent of code puzzles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spossner/aoc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)