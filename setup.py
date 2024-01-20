from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='poller-framework',
    version='1.0',
    packages=['util', 'resource', 'messaging', 'poller'],
    url='https://github.com/mchauhan3/poller-framework',
    license='MIT',
    author='mohitc',
    author_email='mhchauhan3@gmail.com',
    description='Lightweight framework for polling a resource at regular intervals and providing notifications on any '
                'updates',
    install_requires=requirements
)
