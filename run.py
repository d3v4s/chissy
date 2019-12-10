#!/bin/env python3

from chiss.core.chiss import Chiss

import sys
import json

command = sys.argv[1]

with open('conf/server.json') as file:
    confServer = json.load(file)

with open('conf/log.json') as file:
    confLog = json.load(file)

chiss = Chiss(command, confServer, confLog)
chiss.execute()
