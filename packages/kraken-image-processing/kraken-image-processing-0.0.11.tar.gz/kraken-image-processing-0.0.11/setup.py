import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kraken-image-processing",
    version="0.0.11",
    description="Kraken Image Processing",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tactik8/kraken_image_processing",
    author="Tactik8",
    author_email="info@tactik8.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['opencv-python', 'fer', 'nudepy', 'aiohttp', 'pyimgbox', 'kraken-class-entity', 'werkzeug', 'flask', 'pytesseract'],
    
)