from setuptools import setup

setup(
    name='strongpy',
    version='0.0.1',
    author='-',
    author_email='-',
    packages=['strongpy', 'strongpy.utils'],
    scripts=[],
    url='-',
    license='LICENSE.txt',
    description='An awesome package that does something',
    long_description=open('README.md').read(),
    install_requires=[
       "pytest",
    ],
)