# InterMine API Examples (Python)

GitHub: https://github.com/intermine/intermine-ws-python

## Installation

Install the intermine python module (requires pandas and requests as
dependencies):

```
$ pip install intermine
$ pip install requests
$ pip install pandas
```

Additionally, these example scripts use the Python-dotenv package to 
manage API keys:

```
pip install python-dotenv
```

Then download the example scripts:

```
$ git clone https://github.com/elsiklab/intermine-api-python-examples.git
```


## Running the example scripts

Due to relative paths, each example script must be run from the 
directory where it's located:

```
$ cd <mine_dir>
$ ./script_name.py
```

Example:

```
$ cd aquamine
$ ./aquamine_region_search_example.py
```
