from setuptools import setup

setup(
    name="clc",
    version='1.0.0',
    description="CLI for automatically clone git repo in the custom dir structures.",
    py_modules=["clc"],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'clc = clc:main',
        ],
    }
)
