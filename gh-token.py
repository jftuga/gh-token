#!/usr/bin/env python3
r"""
gh-token.py
-John Taylor
2024-07-16

`gh-token` opens a KeePass file that contains GitHub fine-grained tokens and
then uses the user-selected token to add or delete the `github.com` internet
password from a MacOS Keychain file.

It provides a `fzf` style menu to assist in selecting the token from the KeePass file.

If the `github.com` internet password already exists, the `add` operation
will overwrite this entry with the newly selected token password.

**NOTE:** Decryption of the KeePass file can be very slow, especially if using a `KEY_FILE`.
"""

import getpass
import os
import os.path
import subprocess
import sys
import urllib.request
from pykeepass import PyKeePass
from pzp import pzp

PGM_NAME = "gh-token"
PGM_VERSION = "1.0.0"
PGM_URL = "https://github.com/jftuga/gh-token"

SERVICE = "github.com"
KEYCHAIN_FILE = "login.keychain"


def version():
    print(f"{PGM_NAME} v{PGM_VERSION}")
    print(PGM_URL)


def usage():
    usage_msg = "gh-token.py <KeePass file> <GitHub username> [add|rm]"
    print()
    print("Usage:")
    print(usage_msg)
    print()
    print("If you want to use a keychain file, then use:")
    print(f"KEY_FILE=My-KeePass-KeyFile {usage_msg}")
    print()


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "-v":
        version()
        return

    if len(sys.argv) != 4:
        usage()
        sys.exit(1)
    db_fname = sys.argv[1]
    github_user = sys.argv[2]
    db_operation = sys.argv[3]

    # verify db_fname exists
    if not os.path.isfile(db_fname):
        print(f"file not found: {db_fname}")
        sys.exit(1)

    # verify github_user exists
    github_user_url = f"https://github.com/{github_user}"
    try:
        with urllib.request.urlopen(github_user_url):
            pass
    except Exception as e:
        print(f"GitHub user not found here: {github_user_url}  Error: {e}")
        sys.exit(1)

    # verify db_operation is either add|rm
    if db_operation not in ["add", "rm"]:
        print(f"Unknown operation: {db_operation}")
        sys.exit(1)

    # add a token
    if db_operation == "add":
        operation = "add-internet-password"
        password = getpass.getpass(f"[{db_fname}] password: ")
        key_file = os.getenv("KEY_FILE", None)
        if key_file:
            print(f"Using key file: {key_file}")
        try:
            kp = PyKeePass(db_fname, password=password, keyfile=key_file)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        all_entries = {}
        for entry in kp.entries:
            if entry.group.name.startswith("Recycle Bin"):
                continue
            pos = entry.title.find(" (")
            if pos == -1:
                pos = len(entry.title)
            title = entry.title[:pos]
            all_entries[title] = entry

        selection_list = sorted(all_entries.keys(), key=str.lower, reverse=True)
        selection = pzp(selection_list)
        if not selection:
            sys.exit(1)
        selected_entry = all_entries[selection]
        github_token = selected_entry.password

        # -r htps is specifically needed when creating a GitHub token
        security_args = (
            "security", operation, "-a",
            github_user, "-s", SERVICE,
            "-w", github_token, "-U",
            "-r", "htps", KEYCHAIN_FILE,
        )
    # delete a token
    elif db_operation == "rm":
        operation = "delete-internet-password"
        security_args = (
            "security", operation, "-a",
            github_user, "-s", SERVICE,
            KEYCHAIN_FILE,
        )
    else:
        print(f"Unknown operation: {db_operation}")
        sys.exit(1)

    # run the MacOS 'security' command-line program with the appropriate options
    result = subprocess.run(security_args, capture_output=True)
    if result.returncode == 0:
        print(f"SUCCESS: {operation}")
        return
    print("Error (this may not emit any output):")
    if len(result.stdout):
        print(result.stdout.decode("utf-8"))
    if len(result.stderr):
        print(result.stderr.decode("utf-8"))
    sys.exit(result.returncode)


if __name__ == "__main__":
    sys.exit(main())
