#!/usr/bin/env python3
#
# Rattlegram Desktop
# Copyright 2025 
# Stuart MacIntosh ZL3TUX <stuart@macintosh.nz>
#

import os
import sys
import json
import platform
import getpass

DEFAULT_CFO = 1300

username = getpass.getuser()
if len(username) > 13:
    DEFAULT_CALLSIGN = username.encode("ascii", "ignore").decode().upper()[0:13]
elif len(username) > 0 and len(username) < 14:
    DEFAULT_CALLSIGN = username.encode("ascii", "ignore").decode().upper()
else:
    DEFAULT_CALLSIGN = 'ANONYMOUS'

_platform = platform.system().lower()
if _platform == 'windows':
    # unsupported yet
    DEFAULT_ENCODE = 'bin' + os.sep + '%s-%s' % (platform.system().lower(), platform.machine()) + os.sep + 'encode.exe'
    DEFAULT_DECODE = 'bin' + os.sep + '%s-%s' % (platform.system().lower(), platform.machine()) + os.sep + 'decode.exe'
elif _platform == 'darwin':
    # unsupported yet
    DEFAULT_ENCODE = 'bin' + os.sep + '%s-%s' % (platform.system().lower(), platform.machine()) + os.sep + 'encode'
    DEFAULT_DECODE = 'bin' + os.sep + '%s-%s' % (platform.system().lower(), platform.machine()) + os.sep + 'decode'
elif _platform == 'linux':
    DEFAULT_ENCODE = 'bin' + os.sep + '%s-%s' % (platform.system().lower(), platform.machine()) + os.sep + 'encode'
    DEFAULT_DECODE = 'bin' + os.sep + '%s-%s' % (platform.system().lower(), platform.machine()) + os.sep + 'decode'

class RattlegramDesktopConfig():
    def __init__(self):
        self.current_config = self.read_config()

    def read_config(self):
        # if exists, load configuration from file, else create new config file
        config_file = os.path.expanduser('~') + os.sep + '.rattlegram.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as existing_config_file:
                    config = json.load(existing_config_file)
            except FileNotFoundError:
                print("Error: The file '.rattlegram.json' was not opened, but the file exists: check permissions.")
                sys.exit(1)
            except json.JSONDecodeError:
                print("Error: Failed to decode JSON from the file. The file might contain invalid JSON.")
                sys.exit(1)
        else:
            try:
                with open(config_file, 'w') as new_config_file:
                    config = { 
                            'callsign': DEFAULT_CALLSIGN,
                            'CFO': DEFAULT_CFO,
                            'encode': DEFAULT_ENCODE,
                            'decode': DEFAULT_DECODE
                        }
                    json.dump(config, new_config_file)
            except Exception as e:
                print(e)
                sys.exit(1)

        return config

    def write_config(self, config):
        config_file = os.path.expanduser('~') + os.sep + '.rattlegram.json'
        try:
            with open(config_file, 'w') as new_config_file:
                json.dump(config, new_config_file)
        except Exception as e:
            print(e)
            sys.exit(1)

    def get_value(self, key):
        # TODO handle KeyError
        try:
            value = self.read_config()[key]
        except KeyError:
            value = ''
        print('get_value\t%s:%s' % (key, value))
        return value

    def set_value(self, key, value):
        # TODO
        print('set_value\t%s:%s' % (key, value))
        config = self.read_config()
        config[key] = value

        self.write_config(config)

        return True

if __name__=='__main__':
    from IPython import embed
    c = RattlegramDesktopConfig()
    print(c.read_config())
    embed()