"""Setup for read env"""
from setuptools import setup

requirements = [
    'fastapi>=0.70.0',
]

setup(
    name='py-handling-response',
    version='0.1.2',
    license='MIT',
    description='py handing response for fast api responses from functions and classes',
    author='liuspatt',
    author_email='liuspatt@handlingresponse.com',
    url='https://github.com/liuspatt/py-handling-response',
    keywords=['env', 'python', 'windows'],
    install_requires=requirements,
    python_requires=">=3.5",
    packages=['handlingresponse'],
    package_dir={'': 'src'},
    package_data={
        'handlingresponse': ['py.typed'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Environment :: Web Environment',
    ],
)
