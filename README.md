# gh-token

`gh-token` opens a KeePass file that contains GitHub fine-grained tokens and
then uses the user-selected token to add or delete the `github.com` internet
password from a MacOS Keychain file.

It provides a `fzf` style menu to assist in selecting the token from the KeePass file.

If the `github.com` internet password already exists, the `add` operation
will overwrite this entry with the newly selected token password.


**NOTE:** Decryption of the KeePass file can be very slow, especially if using a `KEY_FILE`.

## Install
```shell
git clone https://github.com/jftuga/gh-token
cd gh-token
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python gh-token.py tokens.kdbx your-github-username add
```

## Usage

```
Usage:
gh-token.py <KeePass file> <GitHub username> [add|rm]

If you want to use a keychain file, then use:
KEY_FILE=My-KeePass-KeyFile gh-token.py <KeePass file> <GitHub username> [add|rm]
```

## Acknowledgements

**Modules used:**

* pykeepass - https://github.com/libkeepass/pykeepass
* pzp - https://github.com/andreax79/pzp

## Disclaimer Notification

This program is my own original idea and was completely developed on my own personal time,
for my own personal benefit, and on my personally owned equipment.
