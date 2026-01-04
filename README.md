# pass-cli

## Table of Contents
1. [Architecture](#architecture)
    - 1.1. [Cryptography](#cryptography)
2. [How to run](#how-to-run)
    - 2.1. [Arguments](#arguments)

## Architecture

### Cryptography

## How to run
Run the following command at the repository root:
```bash
python3 -m src.main [-h] [--add] [--remove] [--update] [--get]
```

### Arguments
This application expects the following arguments:

+ `-h` or `--help`: Displays help
+ `-a` or `--add`: Adds an entry to your vault
+ `-r` or `--remove`: Removes an entry from your vault
+ `u` or `--update`: Updates an entry
+ `-g` or `--get`: Copies a password to your clipboard for 10 seconds, then removes it from the clipboard
