from setuptools import setup, find_packages


VERSION = '0.0.4'
DESCRIPTION = ''
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="bapi-fw",
    version=VERSION,
    author="Christophe Kafrouni",
    author_email="<chris.kafrouni@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pydantic'],
    keywords=['python', 'api', 'framework', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
