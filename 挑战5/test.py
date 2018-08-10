#!/usr/bin/env python3

from configparser import ConfigParser

cf = ConfigParser.read("configfile")

sesions = cf.sections()

print()