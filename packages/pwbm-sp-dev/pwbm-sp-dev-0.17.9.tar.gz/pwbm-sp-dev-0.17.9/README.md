# PWBM Local Development Tools

## Requirements
Tool implemented for Python version 3.9


## Installation instruction:

### Virtual environment manager

`pipenv` documentation:
- [pipenv](https://pypi.org/project/pipenv/)

#### First the manager itself should be installed:
```shell
python3.9 -m pip install pipenv
```

#### Creating virtual environment  

In terms of pipenv, virtual environment is just a folder. That means, that all you have to do is to create a folder and run 
following command:
  ```shell
pipenv install --python 3.9
```
A virtual environment will for Python version 3.9 will be created.

#### Virtual environment usage

There are two ways to work with virtual environment:  

1. It can be activated by following command:
```shell
pipenv shell
```
After activating the environment command may be run as `pwbm <command>`

2. Running command without activating environment:
```shell
pipenv run pwmb-sp <command>
```

Note: Both this option assume that current folder is the folder with virtual environment

### Install Python package:
After creating virtual environment, execute following command:
```shell
pipenv install --python 3.9 pwbm-sp-dev
```
This will install the latest package version

### Verify installation
```shell
pipenv run pwbm-sp
```
If everything was installed correctly, help message will be printed

### Installing legacy versions

Toolset supports installation of legacy versions. 

Installation of particular version: 
```shell
pipenv install --python 3.9 pwbm-sp-dev==0.0.0
```
Where `0.0.0` is replaced with package version


NOTE: It's NOT possible to have multiple version of the package within same virtual environment.
If you want to use multiple versions - install them in separate environments.


## Features

PWBM local development tools has following feature:

* Create boilerplate
```shell
pwbm-sp boilerplate /path/to/file.py
```
This command will create a Python file in specified location

* Run scraper script
```shell
pwbm-sp run /path/to/store/file.py
```
This command will run file from specified location. If custom scraper needs parameters, they can be provided in a following way:
```shell
pwbm-sp run /path/to/input/file.py -p param1=value1 param2=value2
```

* Wrap scraper script into pipeline configuration
```shell
pwbm-sp wrap --input /path/to/input/file.py --output /path/to/output/file.json
```
Omitting `--output` parameter will result printing pipeline configuration into console.

If custom scraper needs parameters, they can be provided in a following way:
```shell
pwbm-sp wrap --input /path/to/input/file.py -p param1=value1 param2=value2
```