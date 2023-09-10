
with open('requirements.txt') as f:
    required = f.read().splitlines()


from setuptools import setup, find_packages

setup(
    install_requires=required,
    name="nmi-checker",
    version="1.6.1",
    packages=find_packages(),
    package_data={
        'nmi_checker': ['separated_data.json']
    },
    # other metadata...
)
