from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'My Pypi Module'
LONG_DESCRIPTION = "My Pypi Module"

# Setting up
setup(
    name="nabil",
    version=VERSION,
    author="Nabil Rahman",
    author_email="rjnabilrahman@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests','BeautifulSoup4'],
    keywords=['nabil', 'nabil-official', 'easy syntax', 'python project'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)