from setuptools import setup
setup(
    name='skypebot',
    author='InterCozmic',
    description='A module made for coding text command bots for Skype, with Python.',
    version='0.1.1',
    packages=['skypebot'],
    install_requires=[
        'beautifulsoup4>=4.10.0',
        'certifi>=2021.5.30',
        'charset-normalizer>=2.0.6',
        'idna>=3.2',
        'requests>=2.26.0',
        'SkPy>=0.10.4',
        'soupsieve>=2.2.1',
        'urllib3>=1.26.7',
        'wincertstore>=0.2',
    ]
)
