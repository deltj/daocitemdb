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
# This file contains unit tests for daocitemdb.
#
#-------------------------------------------------------------------------------
from django.test import TestCase
from daocitemdb import loki

# Here is an example Loki XML file for a real Item
test_xml_string = """\
<?xml version="1.0" encoding="UTF-8"?>
<SCItem>
    <ActiveState>drop</ActiveState>
    <Location>Right Hand</Location>
    <Realm>All</Realm>
    <ItemName>Astral Mephitic Fang</ItemName>
    <AFDPS>16.5</AFDPS>
    <Bonus>0</Bonus>
    <ItemQuality>100</ItemQuality>
    <Equipped>1</Equipped>
    <Level>51</Level>
    <OFFHAND>no</OFFHAND>
    <SOURCE>drop</SOURCE>
    <TYPE>Unspecified</TYPE>
    <DAMAGETYPE>Thrust</DAMAGETYPE>
    <Speed>4.0</Speed>
    <DBSOURCE>LOKI</DBSOURCE>
    <CLASSRESTRICTIONS>
        <CLASS>All</CLASS>
    </CLASSRESTRICTIONS>
    <ISUNIQUE>0</ISUNIQUE>
    <ORACLE_IGNORE>0</ORACLE_IGNORE>
    <USER_VALUE>0</USER_VALUE>
    <VARIANT></VARIANT>
    <ASSOCIATE IsParent="0"></ASSOCIATE>
    <EQUIPLIST>
        <SLOT NAME="Right Hand">true</SLOT>
    </EQUIPLIST>
    <DROPITEM>
        <SLOT Number="0">
            <Remakes>0</Remakes>
            <Effect>All Melee Skill Bonus</Effect>
            <Qua>99</Qua>
            <Amount>3</Amount>
            <Done>0</Done>
            <Time>0</Time>
            <Type>Skill</Type>
        </SLOT>
        <SLOT Number="1">
            <Remakes>0</Remakes>
            <Effect>Fatigue</Effect>
            <Qua>99</Qua>
            <Amount>10</Amount>
            <Done>0</Done>
            <Time>0</Time>
            <Type>Other Bonus</Type>
        </SLOT>
        <SLOT Number="2">
            <Remakes>0</Remakes>
            <Effect>Dexterity</Effect>
            <Qua>99</Qua>
            <Amount>5</Amount>
            <Done>0</Done>
            <Time>0</Time>
            <Type>Cap Increase</Type>
        </SLOT>
        <SLOT Number="3">
            <Remakes>0</Remakes>
            <Effect>AF Bonus</Effect>
            <Qua>99</Qua>
            <Amount>15</Amount>
            <Done>0</Done>
            <Time>0</Time>
            <Type>Other Bonus</Type>
        </SLOT>
        <SLOT Number="4">
            <Remakes>0</Remakes>
            <Effect>Strength</Effect>
            <Qua>99</Qua>
            <Amount>5</Amount>
            <Done>0</Done>
            <Time>0</Time>
            <Type>Cap Increase</Type>
        </SLOT>
        <SLOT Number="5">
            <Remakes>0</Remakes>
            <Effect>Style Damage Bonus</Effect>
            <Qua>99</Qua>
            <Amount>4</Amount>
            <Done>0</Done>
            <Time>0</Time>
            <Type>Other Bonus</Type>
        </SLOT>
        <SLOT Number="6">
            <Remakes>0</Remakes>
            <Effect>Melee Damage Bonus</Effect>
            <Qua>99</Qua>
            <Amount>4</Amount>
            <Done>0</Done>
            <Time>0</Time>
            <Type>Other Bonus</Type>
        </SLOT>
        <SLOT Number="7">
            <Remakes>0</Remakes>
            <Effect></Effect>
            <Qua>99</Qua>
            <Amount>0</Amount>
            <Done>0</Done>
            <Time>0</Time>
            <Type>Unused</Type>
        </SLOT>
        <SLOT Number="8">
            <Remakes>0</Remakes>
            <Effect></Effect>
            <Qua>99</Qua>
            <Amount>0</Amount>
            <Done>0</Done>
            <Time>0</Time>
            <Type>Unused</Type>
        </SLOT>
        <SLOT Number="9">
            <Remakes>0</Remakes>
            <Effect></Effect>
            <Qua>99</Qua>
            <Amount>0</Amount>
            <Done>0</Done>
            <Time>0</Time>
            <Type>Unused</Type>
        </SLOT>
    </DROPITEM>
</SCItem>
"""

# This test will attempt to import the example XML string shown above
class LokiXMLImportTest(TestCase):
    
    def test_loki_xml_import(self):
        loki.import_item_from_xml(test_xml_string)
        loki.import_item_from_xml(test_xml_string)