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

class RecoverClass:
    def __init__(self, current_filament, file):
        self.filament = current_filament
        self.file = file

def help_usage():
    print "Usage : python {} EXXXX FILE".format(sys.argv[0])
    print "> EXXXX : current filament, example : E187.52"
    print "> FILE  : the original and complete GCode file"

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        help_usage()
        exit(1)

    print("Starting recovering Gcode at interrupted step")
    recover = RecoverClass(sys.argv[1], sys.argv[2])
