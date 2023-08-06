import pathlib

from setuptools import setup

long_description = pathlib.Path("README.md").read_text()

# for options, see https://github.com/pypa/sampleproject/blob/main/setup.py
setup(
    name='chatter_py',
    version='1.0.1',
    packages=['chatter_py'],
    url='https://github.com/nickjfenton/chatter',
    license='MIT',
    author='nickjfenton',
    author_email='nickjfenton@yahoo.co.uk',
    description='A lightweight Python framework for building chatbots.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3",
    keywords="chatbot, framework"
)
