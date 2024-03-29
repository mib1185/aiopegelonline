"""Setup module for aiopegelonline."""
from pathlib import Path

from setuptools import setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = "0.0.9"


setup(
    name="aiopegelonline",
    version=VERSION,
    license="Apache License 2.0",
    url="https://github.com/mib1185/aiopegelonline",
    author="mib1185",
    description="Asynchronous library to retrieve data from PEGELONLINE.",
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=["aiopegelonline"],
    python_requires=">=3.9",
    package_data={"aiopegelonline": ["py.typed"]},
    zip_safe=True,
    platforms="any",
    install_requires=["aiohttp"],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
