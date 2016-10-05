from setuptools import setup, find_packages

setup(
    name='pycalendar',
    version='0.1.0',
    description='Python alternative to Unix cal',
    packages=find_packages(),
    install_requires=['arrow', 'click', 'termcolor', 'requests'],
    entry_points={
        'console_scripts': [
            'pycal = pycalendar.pycal:main',
            'pycal-fetch = pycalendar.pycal:fetch_holidays',
        ],
    },
)