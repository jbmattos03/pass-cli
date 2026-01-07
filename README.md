# pass-cli

## Table of Contents
1. [Architecture](#architecture)
    - 1.1. [Entry structure](#entry-structure)
    - 1.2. [Cryptography](#cryptography)
2. [How to run](#how-to-run)
    - 2.1. [Environment variables](#environment-variables)
    - 2.2. [Running the project](#running-the-project)
    - 2.3. [Arguments](#arguments)
    - 2.4. [Tip: Alias](#tip-alias)

## Architecture
### Requirements

+ Python 3.10+
+ A CLI clipboard manager (see [Not Implemented Error](#not-implemented-error))

#### Not Implemented Error
This application uses [Pyperclip](https://pyperclip.readthedocs.io/en/latest/#) for clipboard related functionalities. Pyperclip requires a copy/paste mechanism, such as xclip, xsel, etc. to have access to your system's clipboard (see [Pyperclip's official documentation](https://pyperclip.readthedocs.io/en/latest/#not-implemented-error)).

**NOTE:** If you use Wayland, I recommend wl-clipboard (it's what I personally use).
### Entry structure
```python
entry_name = {
    "password": password,
    "additional_info": {
        "field_1": field_1,
        ...
    }
}
```

### Cryptography
TBD

## How to run
### Environment variables
Create a `.env` file at the repository root with the following command:
```bash
touch .env
```

Then, you can refer to [`.env.example`](.env.example) for guidance on how to fill your `.env` file.

**OBS.:** Do note that `VAR_DIR` and `VAULT_DIR` should be **directory** paths, not file paths.

### Running the project
To run this project, run the following command at the repository root:
```bash
python3 src/main.py [-h] [--add] [--remove] [--update] [--get] [--show]
```

### Arguments
This application expects the following arguments:

+ `-h` or `--help`: Displays help
+ `-a` or `--add`: Adds an entry to your vault
+ `-r` or `--remove`: Removes an entry from your vault
+ `u` or `--update`: Updates an entry
+ `-g` or `--get`: Copies a password to your clipboard for 10 seconds, then removes it from the clipboard
+ `-s` or `--show`: Shows all attributes of an entry. Will prompt the user to confirm if they want the password to be displayed.

### Tip: Alias
To make it more convenient to run this project, you can set up an alias for the command above:
```bash
set -Ux PASS_CLI_REPO_PATH {path_to_repo}
alias -s passcli='bash {path_to_repo}/pass-cli'
```