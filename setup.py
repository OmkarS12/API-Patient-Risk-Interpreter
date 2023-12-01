from setuptools import find_packages, setup

setup(
    name='CMS-HCC',
    version='0.0.1',
    author='Omkar',
    author_email='sadekar.o@northeastern.edu',
    packages=find_packages(),
    install_requires=['numpy'],
    include_package_data=True,
    package_dirc={"": "hccpy"},
    package_data={"data": ["*.TXT", "*.csv", "*.json"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ])
