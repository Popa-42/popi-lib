from setuptools import setup, find_packages

with open('app/README.md', 'r') as file:
    long_description = file.read()

setup(
    name='popi_lib',
    version='0.0.3',
    description="A package with various helpful utilities.",
    package_dir={'': 'app'},
    packages=find_packages(where='app'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Popa-42/popi-lib',
    author="Popa",
    author_email="prover09_reagent@icloud.com",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'colorama~=0.4.6'
    ],
    extras_require={
        'dev': ['pytest>=7.0', 'twine>=4.0.2']
    },
    python_requires='>=3.7',
)
