from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "1.0.3"
DESCRIPTION = "Simple Package that allows the extraction of player data, this is a REST api and needs to be ran. This is a flask application"
LONG_DESCRIPTION = """Popular Online Gaming Platform allows games like counterstrike and much more to be played on their servers,
                Faceit has created a pretty inrteresting and hard to understand API that can extract player and game data, this package will do all the hard backend stuf for you so you can just simply import the package and query
                a player, game or map.
                """

# Setting up
setup(
    name="pyfaceit",
    version=VERSION,
    author="Milahn Martin",
    author_email="<milahnmartin.develop@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["requests", "flask"],
    keywords=["python", "faceit", "api", "rest api", "get data", "flask","python"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
