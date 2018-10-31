Figcan - Minimalistic Configuration Handling Library
==================================================== 
*Figcan* is a minimalistic configuration handling library for Python.

It is designed to help you manage runtime configuration coming from different 
sources, without making any assumptions about configuration file formats and 
locations, and while staying super simple to use for common use cases.

Figcan has no runtime dependencies other than Python versions 2.7 or 3.4 and 
up. 

[![Build Status](https://travis-ci.org/shoppimon/figcan.svg?branch=master)](https://travis-ci.org/shoppimon/figcan)

Figcan's Philosophy
-------------------
*Figcan*'s design is based on a few basic assumptions:

* Configuration is important in any but the most simple projects
* Configuration can easily be described as a set of nested key-value pairs 
  where values can have a few native scalar types (booleans, strings, numbers) 
  or container types (lists, mappings)
* Python dictionaries are *almost* perfect for configuration. *Almost*.
* Configuration keys can be known in advance. The structure of your expected
  configuration is almost always known to your project's code and thus can be 
  described in advance.   
* Configuration can come from multiple sources: in-code defaults, multiple 
  configuration files, environment variables, command line arguments, 
  database-persisted key-value pairs etc.   
* But realistically, objects read from these sources are not that different 
  from each other: they can almost always be represented as Python object 
  attributes or dictionaries
* There is already a Python module in out there that handles reading values 
  from these sources and converting them to some kind of native dictionary or 
  object 

With those in mind, here is what *Figcan* will do:

* Provide a dictionary-like object containing configuration
* This object is created from a dictionary specifying your default 
  configuration
* Additional configuration values (in the form of Python dictionaries or 
  objects) can be "layered" on top of this default configuration to override 
  values
 
And here is what *Figcan* will not do for you in one line - but supports doing
very easily with just a few lines of custom code you will need to write:

* Read and parse files in specific formats (`INI`, `JSON`, `YAML` etc.)
* Look for configuration files in specific places, based on OS or environment
* Read values from a specific command line argument parsers (`argparse`, 
  `optparse`, `click` etc.) 
* Manage saving configuration to files or anywhere else
* Provide any API to accessing configuration beyond what the Python `dict` 
  interface provides (which, if you ask us, should be enough for everybody)
 
We plan to provide some documentation and examples on how to get these done
with *Figcan*. 

Getting Started
---------------

### Installation
It is recommended to add *Figcan* to your project using `pip`:

    pip install figcan

You should also be able to install directly from the source tree pulled from 
git:

    `TBD`

### Using in your project
Typically, *Figcan* is used by reading configuration from all sources at the 
beginning of your program (e.g. in your `main`), and making the configuration 
object available to all other parts of the program as needed. 

Here is a very basic (but not unrealistic) usage example:

```python
import os
from figcan import Configuration
from my_project.config import default_config  # A dictionary defining default configuration values

def main():
    config = Configuration(default_config)
    
    # Apply configuration overrides from environment variables
    config.apply_flat(os.environ, prefix='MYPROJECT')

    # Do something with the configuration:
    db_engine = sqlalchemy.create_engine(config['db']['url'])
```

#### Applying configuration from YAML or JSON files:
If your configuration is saved in a file format that can be parsed into a 
Python `dict`, you can easily get *Figcan* to work with it. For example: 

```python
import yaml
from figcan import Configuration
from my_project.config import default_config  # A dictionary defining default configuration values

def main(config_file_path):
    config = Configuration(default_config)
    
    with open(config_file_path) as f:
        config.apply(yaml.safe_load(f))
        
    # Do something with the configuration:
    db_engine = sqlalchemy.create_engine(config['db']['url'])
```

Note that `Configuration.apply` will raise an exception if it encounters a
configuration key that is not present in your `default_config`. This can be
changed like so:

```python
config.apply(yaml.safe_load(f), raise_on_unknown_key=False)
```

If you want to allow merging new configuration keys into a configuration 
section, you will need to define that section as `Extensible` in the base
configuration:

```python
from figcan import Configuration, Extensible

default_config = dict({  # Base configuration keys are known ahead and static 
    'bind_port': 5656,
    'db': {  # Database settings keys are known ahead and static
        'hostname': 'db.local',
        'username': 'foobar',
        'password': 'blahblah'
    } ,
    'logging': Extensible({  # But logging settings are flexible, and new handlers / loggers can be defined
        'handlers': {
            'handler_1': '...'
        }
    })
})

config = Configuration(default_config)

# This will not raise an exception and 'handler_2' config will be available in `config`:
config.apply({"logging": {"handlers": {"handler_2": "... more config ..."}}})
```

#### Applying configuration from environment variables:

#### Applying configuration from command line arguments:

## Some Alternatives to Consider
There are many configuration handling libraries for Python. Some may be more 
suitable for you than *Figcan* (some we have tried before deciding to write 
*Figcan*):

* 
* 
* 

## TODO / Planned Features

### Schema based type coercion and validation of configuration values
the idea here is that the initial `default_config` dict will also contain some
type annotations in some form. These will be used to coerce override values 
(e.g. when coming as strings from environment variables) and to do some 
validation when configuration is applied. 

### Allow defining "flexible" vs "non-flexible" configuration mapping
For example, a `logging` section used for `logging.config.dictConfig` typically
needs to have a flexible structure. However, making everything flexible can 
lead to typos etc. not being detected.

## Credits
Figcan was created by the [Shoppimon](https://www.shoppimon.com) team and is in
use by Shoppimon in highly used, critical production code. 

## License
© 2018 Shoppimon LTD, all rights reserved

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
