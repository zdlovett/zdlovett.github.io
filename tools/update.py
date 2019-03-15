"""
Script to update and re-generate plots.
The script is runs once a day (hour?) and updates the plots on the website.

The general process for this is:

1) git pull
2) pull the data from the overwatch api
3) update the relevent json files
4) git commit with auto generated message
5) git push to deploy it
"""

import pexpect
import requests

from IPython import embed


output = pexpect.run(command="git pull")
print(output)

output = pexpect.run(command="git status")
print(output.decode())

output = pexpect.run(command='git commit -a -m "auto commit"')
print(output.decode())

output = pexpect.run(command="git push")
print(output.decode())

