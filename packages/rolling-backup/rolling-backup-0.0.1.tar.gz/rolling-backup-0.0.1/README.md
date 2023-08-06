# rolling-backup
create rolling backups of a file

![Tests](https://github.com/RSabet/rolling-backup/actions/workflows/test.yml/badge.svg)
![Issues](https://img.shields.io/github/issues/RSabet/rolling-backup)
![License](https://img.shields.io/github/license/RSabet/rolling-backup)
[![codecov](https://codecov.io/gh/RSabet/rolling-backup/branch/main/graph/badge.svg?token=85XWRBNF9T)](https://codecov.io/gh/RSabet/rolling-backup)
## installation
``` 
$ pip install rolling-backup
```

## Usage

```python

from rolling_backup import backup
backup(filename, num_to_keep=12)

```
returns True on success otherwise False

Creates up to 12 rolling backups of file `filename` by appending zeroes to the filename.

## Example Usage
```python
>>> import os
>>> from rolling_backup import backup
>>> os.listdir(".")
['file.txt']
>>> backup('file.txt', num_to_keep=12)
True
>>> os.listdir(".")
['file.txt', 'file.txt.00']
```