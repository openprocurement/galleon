import setuptools

REQUIRES = [
    'jsonschema',
    'jsonmapping',
    'pyjq',
    'jmespath'
]
TEST = REQUIRES + ['pytest', 'pytest-cov', 'pytest-benchmark', 'pyyaml']
DEV = TEST + ['ipdb']
EXTRA = {
    'test': TEST,
    'dev': DEV
}

setuptools.setup(
    name="galleon",
    version="0.1.2",
    url="-",

    author="yshalenyk",
    author_email="yshalenyk@quintagroup.com",
    license='Apache License 2.0',

    description="Openprocurement Galleon",
    long_description=open('README.rst').read(),
    zip_safe=False,
    include_package_data=True,

    packages=setuptools.find_packages(),
    tests_require=TEST,
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
