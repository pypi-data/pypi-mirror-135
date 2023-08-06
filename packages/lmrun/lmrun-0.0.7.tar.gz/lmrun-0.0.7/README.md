# lmrun

A CLI to run Groovy or PowerShell scripts on a LogicMonitor collector for debugging purposes.

## Installation

From PyPi:

`pip install lmrun`

From source:

`python setup.py`

## Usage

### Sign In

First use the `login` command to log into LogicMonitor by specifying your API ID and Key

```
C:\> lmrun login
Please enter your LogicMonitor company name:
Please enter the API access id:
Please enter the API access key:
```

or via cli parameters

```
lmrun login --company company_name --access_id abc123 --access_key def456
```

This will create a config.json file in the `~\.lmrun` directory.

### Run a script

Then use the `execute` or `exe` command by passing a .groovy or .ps1 file, and the name of the monitored device to run the script against.

```
lmrun execute test.groovy SRV-01
```

```
lmrun exe test.ps1 SRV-01
```

```
lmrun exe test.groovy SRV-01
```

### Logout

If you wish to delete the saved credentials located in `~\.lmrun\config.json` simply run:

```
lmrun logout
```
