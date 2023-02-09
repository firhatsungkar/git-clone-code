from setuptools import find_packages, setup

setup(
    name="clc",
    version='1.0.0',
    description="CLI for automatically clone git repo in the custom dir structures.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
    [console_scripts]
    clc=clc:main
    '''
)
