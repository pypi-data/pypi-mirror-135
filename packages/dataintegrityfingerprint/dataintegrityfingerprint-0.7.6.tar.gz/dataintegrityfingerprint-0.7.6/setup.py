import os
import setuptools


PACKAGE_NAME = "dataintegrityfingerprint"


def get_version():
    """Get version number."""

    with open(os.path.join("src", PACKAGE_NAME, "__init__.py")) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("'")[1]
    return "None"

def get_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


setuptools.setup(
    name = PACKAGE_NAME,
    version=get_version(),
    author='Oliver Lindemann, Florian Krause',
    author_email='oliver@expyriment.org, florian@expyriment.org',
    description='Data Integrity Fingerprint (DIF) - ' \
    'A reference implementation in Python',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    url="https://github.com/expyriment/dataintegrityfingerprint-python",
    classifiers=[
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [f'{PACKAGE_NAME}={PACKAGE_NAME}.cli:cli'],
        'gui_scripts': [f'{PACKAGE_NAME}-gui={PACKAGE_NAME}.gui:start_gui']
    }
)
