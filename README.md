Figcan - Minimalistic Configuration Handling Library
==================================================== 
*Figcan* is a minimalistic configuration handling library for Python 3.5 and up. 
It is designed to help you manage runtime configuration coming from different sources, without
making any assumptions about configuration file formats and locations, without requiring any
dependencies beyond what's in the Python standard library, and while staying super simple to use for
common use cases.   

When should I use Figcan?
-------------------------
*Figcan*'s design is based on a few basic assumptions:

* Configuration is important in any but the most simple projects
* Configuration can easily be described as a set of nested key-value pairs where
  values can have a few native scalar types (booleans, strings, numbers) or container
  types (lists, mappings) 
* Python dictionaries are *almost* perfect for holding and passing around configuration
* Configuration "keys" can be known in advance. The structure of your expected configuration is
  almost always known to your project's code and therefore can be described in advance.   
* Configuration can come from multiple sources: in-code defaults, multiple configuration files, 
  environment variables, command line arguments, database-persisted key-value pairs etc.   
* But realistically, these sources are not that different from each other: they can almost always be
  represented as Python object attributes or dictionaries
* There is already a Python module in out there that handles reading values from these sources and converting them
  to some kind of native dictionary or object 

With those in mind, here is what *Figcan* will do:
* Provide a dictionary-like object containing configuration
* This object is created from a dictionary specifying your default configuration
* Additional configuration values (in the form of Python dictionaries or objects) can be "layered" on top of this 
  default configuration to override values
 
And here is what *Figcan* will not do:
* Read and parse files in specific formats (`INI`, `JSON`, `YAML` etc.)
  * Look for configuration files in specific places, based on OS or environment 
* Read values from a specific command line argument parser library (`argparse`, `optparse`, `click` etc.) 
* Manage saving configuration to files or anywhere else
* Provide any API to accessing configuration beyond what the Python `dict` interface provides 
  (which, if you ask us, should be enough for everybody)
 
However, as you will see, doing most of these with *Figcan* can be very straight-forward, 
and we provide some documentation and examples on how to do that. 

You should decide whether to use *Figcan* or any other configuration handling library (and there are many)
based on what it can do for you, but also based on all the things it *does not* do - as less code
and runtime dependencies is always "a good thing"™.

Getting Started
---------------

### Installation
Install via `pip`:

Or if using `pipenv`:

Or directly from `git`: 


### Using in your project
Typically, *Figcan* is used by reading configuration from all sources at the beginning of your program
(e.g. in your `main`), and making the configuraion object available to all other parts of the program as needed. 

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

#### Applying configuration from INI files or other key-value formats:

#### Applying configuration from environment variables:

#### Applying configuration from command line arguments:

## Some Alternatives to Consider
There are many configuration handling libraries for Python. Some may be more suitable 
for you than *Figcan* (some we have tried before deciding to write *Figcan*):

* 
* 
* 

## TODO / Planned Features
* **"Schema" based type coercion and validation of configuration values** - the idea here is that the initial 
  `default_config` dict will also contain some type annotations in some form. These will be used to 
  coerce override values (e.g. when coming as strings from environment variables) and to do some validation
  when configuration is applied. 

## Credits
Figcan was created by the [Shoppimon](https://www.shoppimon.com) team. 

## Legal Stuff
© 2018 Shoppimon LTD, all rights reserved

* License TBD
