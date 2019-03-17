"handful of useful functions"

import json
import pexpect

def load(path):
    "load json data from path"
    with open(path, "r") as fp:
        data = json.load(fp)
    return data

def dump(data, path):
    "dump json data to a path"
    with open(path, "w") as fp:
        json.dump(data, fp, indent=4)

def pull():
    output = pexpect.run(command="git pull")
    print(output)

    output = pexpect.run(command="git status")
    print(output.decode())


def push():
    output = pexpect.run(command='git commit -a -m "auto commit"')
    print(output.decode())

    output = pexpect.run(command="git push")
    print(output.decode())