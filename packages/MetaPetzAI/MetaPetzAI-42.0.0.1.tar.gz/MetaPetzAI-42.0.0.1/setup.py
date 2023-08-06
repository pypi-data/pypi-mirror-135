from distutils.core import setup
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    
    name="MetaPetzAI",                     # This is the name of the package
    version="42 0.0.1",                        # The initial release version
    author="Jordan Sweetman",                     # Full name of the author
    description="talk to your MetaPet",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["MetaPetzAI"],             # Name of the python package
    install_requires=["tensorflow", "keras"]                     # Install other dependencies if any
)