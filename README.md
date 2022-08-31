# Sidekick Agent Python

Sidekick agent python is a Python library that communicate with Sidekick broker to inspect, monitor and debug your application on the fly.

## Installation

For Macos, install [brew](https://brew.sh) to manage installation packages easily.

```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install python 3.6. You can take a glance following [stackover thread](https://stackoverflow.com/questions/51726203/installing-python3-6-alongside-python3-7-on-mac) for macos.


Check your python version on working environment nad make sure its python3.6. 
Then, Install [pipenv](https://pipenv-fork.readthedocs.io/en/latest/) with following command.

```bash
brew install pipenv
```

## Usage

Activate pipenv with following command and install dependecies mentioned in Pipfile.

```
pipenv shell
```
```
pipenv install
```

Build tracepointdebug.
**Note:** For permisson denied error getting whilst running script, use chmod to change permission.

Check "setup.cfg" file created or not

```
./build.sh
```

Check build directory created or not. If not created, run following command to generate source and binary distribution.

```
./build_tools/build_wheels.sh
```

## Entegration with other apps to debugging

To debug Sidekick agent python, just add "build/lib.*/tracepointdebug" by creating soft link in application directory and configure your app according to Sidekick documents. Be sure about your project python version is 
same with sidekick agent python build/lib.*.