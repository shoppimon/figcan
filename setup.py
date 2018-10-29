# Copyright (c) 2018 Shoppimon LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

with open('VERSION') as f:
    version = f.read()

with open('README.md') as f:
    long_desc = f.read()

setup(
    name='figcan',
    version=version,
    description='Figcan - minimalistic configuration handling library for Python',
    keywords='configuration config management yaml json ini arguments simple',
    author='Shahar Evron',
    author_email='shahar@shoppimon.com',
    license='Apache 2.0',
    url='https://github.com/shoppimon/figcan',
    packages=find_packages(),
    long_description=long_desc,
    long_description_content_type='text/markdown',
    install_requires=[],
    python_requires='>=2.7.12,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
)
