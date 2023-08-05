#Copright (c) 2021 LightningV1p3r

from setuptools import setup

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='console-engine',
    version='0.1.2',
    author='LightningV1p3r',
    author_email='LightningV1p3r@protonmail.com',
    url='https://github.com/LightningV1p3r/console-engine',
    description='Custom, easy to integrate shell',
    license='LICENSE.txt',
    packages=["console_engine"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "colorama==0.4.4"
        ]
)