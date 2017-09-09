#!/usr/bin/env python
#title           :gcode_recover.py
#description     :Based on last filament output, it will create a new GCode file to resume an interrupted print
#author          :Alexis Lothore
#date            :20170909
#version         :0.1
#usage           :python gcode_recover.py EXXXXXXX
#notes           :
#python_version  :2.7.13
#==============================================================================
import os
import sys
import re

class RecoverException(Exception):
    pass

class RecoverClass:
    def __init__ (self, current_filament, g_file):
        if not os.path.isfile(g_file):
            raise RecoverException
        if self.arg_is_consumed_filament(current_filament) == False:
            raise RecoverException
        self.filepath = os.path.abspath(g_file)
        self.filament = current_filament

    def arg_is_consumed_filament(self, value):
        result = re.match(r"^E[0-9]+(\.[0-9]+)?$", value)
        if(result is None):
            return False
        else:
            return True

def help_usage():
    print "Usage : python {} EXXXX FILE".format(sys.argv[0])
    print "> EXXXX : current filament, example : E187.52"
    print "> FILE  : the original and complete GCode file"

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        help_usage()
        exit(1)

    try:
        recover = RecoverClass(sys.argv[1], sys.argv[2])
    except RecoverException as e:
        print("Cannot start GCode recovering process : wrong arguments")
        help_usage()
        exit(1)
    print("Starting recovering Gcode at interrupted step")
