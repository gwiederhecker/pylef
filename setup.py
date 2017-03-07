import sys
from setuptools import setup


version = '0.0.2'

setup_requires = ['pytest-runner'] if \
    {'pytest', 'test', 'ptr'}.intersection(sys.argv) else []

setup(
    name='pylef',
    version=version,
    author='Felippe Barbosa',
    author_email='felippebarbosa@gmail.com',
    license='MIT v1.0',
    url='https://github.com/gwiederhecker/pylef',
    description='Python module for controlling isntruments and support IFGW LEF',
    long_description='Sem muito por enquanto',
    keywords='instrument control',
    packages=['pylef'],
    package_dir={'pylef': 'pylef'},
    ext_modules=[],
    provides=['pylef'],
    install_requires=['numpy', 'pyvisa', 'pandas'] + (['future']
                                  if sys.version_info.major < 3 else []),
    setup_requires=setup_requires,
    tests_require=[],
    platforms='OS Independent',
    classifiers=[
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator'
    ],
    zip_safe=False)
