from setuptools import setup

setup(
    name='pycalendar',
    version='0.1.0',
    description='Python alternative to Unix cal',
    py_modules=['pycal'],
    install_requires=['arrow', 'click', 'termcolor', 'requests'],
    entry_points='''
        [console_scripts]
        pycal=pycal:main
        pycal_fetch=pycal:fetch_holidays
    ''',
)