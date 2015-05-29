#-------------------------------------------------------------------------------
#
# This file is part of daocitemdb.
#
# daocitemdb is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# daocitemdb is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# daocitemdb.  If not, see <http://www.gnu.org/licenses/>.
#
# daocitemdb Copyright (c) 2015 Ted DeLoggio
#
#-------------------------------------------------------------------------------
#
# This script is meant to be used from the command-line to import a number of 
# Loki XML files at once.
#
#-------------------------------------------------------------------------------'
import argparse
import os.path
from daocitemdb import loki

# main function of the script
if __name__ == "__main__":
    
    # parse command-line arguments
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("files", nargs="+")
    arguments = argument_parser.parse_args()
    
    # files should contain a list of all the files passed on the command line
    for filename in arguments.files:
        
        print("trying to import file (" + filename + ")")
        
        # test whether this file actually exists
        if os.path.isfile(filename):
            
            # open the file
            with open(filename, "r") as the_file:
            
                # read the file into a string
                xml_string = the_file.read()
                
                # try to read the XML
                loki.read_item_from_xml(xml_string)
        