#!/usr/bin/env python
#title           :gcode_recover.py
#description     :Based on last filament output, it will create a new G-code file to resume an interrupted print
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
        result = re.search(r"E[0-9]+(\.[0-9]+)?", value)
        if(result is None):
            return False
        else:
            return True

    def getInterruptedLine(self):
        pattern = re.compile(r'{}'.format(re.escape(self.filament)))
        with open(self.filepath) as complete_gcode:
            nb_line = 0
            found = False
            for line in complete_gcode:
                if(pattern.search(line)):
                    found = True
                    self.x_interrupted = re.search(r"X-?[0-9]+(\.[0-9]+)?", line).group()
                    self.y_interrupted = re.search(r"Y-?[0-9]+(\.[0-9]+)?", line).group()
                    break
                else:
                    nb_line = nb_line+1
        if(found == True):
            self.interrupted_line = nb_line
        else:
            self.interrupted_line = -1

    def getHeightAtInterruption(self):
        pattern = re.compile(r'Z[0-9]+(\.[0-9]+)?$')
        with open(self.filepath) as complete_gcode:
            nb_line = 0
            current_height = "0.200"
            for line in complete_gcode:
                res = pattern.search(line)
                if(res):
                    current_height = res.group()
                else:
                    nb_line = nb_line+1
                if nb_line >= self.interrupted_line:
                    break
        self.interrupted_height =  current_height

    def writeRecoverFile(self, path):
        complete_gcode = open(self.filepath, "r")
        recovery_gcode = open(path, "w")

        height_before_print = float(self.interrupted_height[1:])+5
        recovery_gcode.write("G0 F9000 Z{}\n".format(height_before_print))
        recovery_gcode.write("G92 {}\n".format(self.filament))
        recovery_gcode.write("G0 F9000 {} {} {}\n".format(self.x_interrupted, self.y_interrupted, self.interrupted_height))
        nb_line = 0
        for line in complete_gcode:
            if nb_line > self.interrupted_line :
                recovery_gcode.write(line)
            nb_line = nb_line +1

        recovery_gcode.close()
        complete_gcode.close()

    def createRecoverFile(self):
        self.getInterruptedLine()
        if(self.interrupted_line >= 0):
            print "Interruption occurred at line {}".format(self.interrupted_line)
            print ">> X : ", self.x_interrupted
            print ">> Y : ", self.y_interrupted
        else:
            print "Interruption line not found, abort"
            return
        self.getHeightAtInterruption()
        if(self.interrupted_height >=0):
            print ">> Z : ", self.interrupted_height
        else:
            print "Interruption height not found, abort"
            return

        recovery_path = "recovery.gcode"
        self.writeRecoverFile("recovery.gcode")
        print "New G-code file available at {}".format(os.path.abspath(recovery_path))

def help_usage():
    print "Usage : python {} EXXXX FILE".format(sys.argv[0])
    print "> EXXXX : current filament, example : E187.52"
    print "> FILE  : the original and complete G-code file"

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        help_usage()
        exit(1)

    try:
        recover = RecoverClass(sys.argv[1], sys.argv[2])
    except RecoverException as e:
        print("Cannot start G-code recovering process : wrong arguments")
        help_usage()
        exit(1)

    print("Starting G-code recovering")
    recover.createRecoverFile()
