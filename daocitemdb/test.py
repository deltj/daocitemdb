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
# daocitemdb Copyright (c) 2014 Ted DeLoggio
#
#-------------------------------------------------------------------------------
#
# unit tests for daocitemdb
#
#-------------------------------------------------------------------------------
import unittest
from daocitemdb import items
from daocitemdb import loki

class TestItem(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_reading_xml(self):
        print("Testing Loki XML Read")
        
        # read in the sample item XML
        item = loki.read_item_from_xml(loki.test_xml_string)
        print(item)
        pass
    
    def test_writing_xml(self):
        print("Testing Loki XML Write")
        
        # build a sample Item to write out
        item = items.Item()
        item.name = "Foo Item"
        
        loki.write_item_to_xml(item)
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestItem.testName']
    unittest.main()