from setuptools import setup
import textwrap

setup(
    name='simple-salesforce-wrapper',
    version='0.02.0',
    author='Iqbal Talaat',
    author_email='iqbaltalaat@gmail.com',
    maintainer='Iqbal Talaat',
    maintainer_email='iqbaltalaat@gmail.com',
    packages=['simple_salesforce_wrapper'],
    url='https://github.com/afrobeard/simple-salesforce-wrapper',
    license='Apache 2.0',
    description=("Simple Salesforce is a basic Salesforce.com REST API client. "
                 "The goal is to provide a very low-level interface to the API, "
                 "returning an ordered dictionary of the API JSON response."),
    long_description=textwrap.dedent(open('README.rst', 'r').read()),
    install_requires=[
        'simple_salesforce'
    ],
    keywords="python salesforce salesforce.com",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
