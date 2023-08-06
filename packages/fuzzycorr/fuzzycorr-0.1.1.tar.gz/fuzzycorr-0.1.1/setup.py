import pathlib
from setuptools import setup, find_packages

setup(
    name="fuzzycorr",
    version="0.1.1",
    author="Tomáš Mikula",
    author_email="mail@tomasmikula.cz",
    description="A numpy implementation of Robust Rank Correlation Coefficients.",
    keywords="fuzzycorr correlation fuzzy",
    license="MIT license",
    url="https://github.com/mikulatomas/fuzzycorr",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "numpy",
    ],
    extras_require={
        "test": ["pytest", "pytest-cov"],
    },
    long_description=pathlib.Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
