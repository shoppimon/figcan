from setuptools import find_packages, setup

with open('VERSION') as f:
    version = f.read()

with open('README.md') as f:
    long_desc = f.read()

setup(
    name='figcan',
    version=version,
    description='Figcan - minimalistic configuration handling library for Python',
    author='Shahar Evron',
    author_email='shahar@shoppimon.com',
    url='https://github.com/shoppimon/figcan',
    packages=find_packages(),
    long_description=long_desc,
    long_description_content_type='text/markdown',
    install_requires=[],
    test_require=[
        'pytest',
        'pytest-flake8',
        'pytest-mypy',
        'pytest-isort'
    ],
)
