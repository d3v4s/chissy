#!/bin/env python3

from chissy.core.chissy import Chissy

import sys
import json

command = sys.argv[1]

with open('conf/server.json') as file:
    confServer = json.load(file)

with open('conf/log.json') as file:
    confLog = json.load(file)

chissy = Chissy(command, confServer, confLog)
chissy.execute()
