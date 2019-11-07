from os.path import dirname, abspath, join, exists
from setuptools import setup

long_description = None
if exists('README.md'):
    with open('README.md') as file:
        long_description = file.read()

install_reqs = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setup(
    name='iprange-python',
    author='Lucas Costa',
    author_email='lucasrodcosta@gmail.com',
    version='0.0.8',
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    install_requires=install_reqs,
    packages=['iprange'],
    url='https://github.com/lucasrodcosta/iprange-python',
    description='Redis as a storage for IP range',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
