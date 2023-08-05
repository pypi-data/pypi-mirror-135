from setuptools import setup, find_packages

setup(
   name='gdlib',
   version='0.0.5',
   description='This is an opinionated gamedev library that is developed within the Software- and '
               'Game Development lecture at Stuttgart Media University.',
   author='Kai Eckert, Florian Rupp. Benjamin Schnabel',
   author_email='rupp@hdm-stuttgart.de',
   packages=find_packages(),
   install_requires=['wheel', 'pygame']
)
