
from setuptools import setup, find_packages

setup(
    name="nmi-checker",
    version="1.5.0",
    packages=find_packages(),
    package_data={
        'nmi_checker': ['separated_data.json']
    },
    # other metadata...
)
