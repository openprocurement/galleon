import setuptools

REQUIRES = [
    'jsonschema',
    'jsonmapping',
    'jq'
]
TEST = REQUIRES + ['pytest', 'pytest-cov']
DEV = TEST + ['ipdb']
EXTRA = {
    'test': TEST,
    'dev': DEV
}

setuptools.setup(
    name="galleon",
    version="0.1.0",
    url="-",

    author="yshalenyk",
    author_email="yshalenyk@quintagroup.com",
    license='Apache License 2.0',

    description="Openprocurement Galleon",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    setup_requires=[
        'pytest-runner',
    ],
    install_requires=REQUIRES,
    extras_require=EXTRA,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
