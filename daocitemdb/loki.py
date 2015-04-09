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
# This file contains functions to handle serializing and de-serializing XML
# files used with the Loki spellcrafting software from Synthetic Realms.
#
#-------------------------------------------------------------------------------
from _elementtree import SubElement
try:
    # first try to use the faster c-implementation of ElementTree
    import xml.etree.cElementTree as ET
except ImportError:
    # if that's not available, fall back to the python implementation
    import xml.etree.ElementTree as ET
from xml.dom import minidom    
from daocitemdb import items

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

def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
#
# This function returns an Item object populated with values from a Loki XML 
# file, which is passed to this function as a string.
#
def read_item_from_xml(xml_string):
    
    # a new Item that we'll construct, and hopefully return to the caller
    item = items.Item();
    
    # TODO: implement countermeasures against billion laughs and quadratic 
    # blowup attacks
    
    # parse the XML string
    root = ET.fromstring(xml_string)
    
    # locate the ItemName element to get this Item's name
    item_name_element = root.find(".//ItemName")
    item.name = item_name_element.text

    # locate the Realm element to get this Item's realm
    realm_element = root.find(".//Realm")
    item.realm = realm_element.text
    
    # locate the Level element to get this Item's level
    level_element = root.find(".//Level")
    item.level = level_element.text
    
    # locate the Location element to get this Item's slot
    location_element = root.find(".//Location")
    item.slot = location_element.text
    
    # locate the DROPITEM element
    dropitem_element = root.find(".//DROPITEM")
    
    # inspect all of the SLOT elements to get this Item's bonuses
    slot_elements = dropitem_element.findall(".//SLOT")
    for slot in slot_elements:

        # make a new Bonus object for this bonus
        bonus = items.Bonus()
        
        # locate the Effect element to get the name of this bonus
        bonus_element = slot.find(".//Effect")
        bonus.effect = bonus_element.text
        
        # locate the Amount element to get the amount of this bonus
        amount_element = slot.find(".//Amount")
        bonus.amount = amount_element.text
        
        # locate the Type element to get the type of bonus (e.g. stat, 
        # resist, stat cap, etc)
        type_element = slot.find(".//Type")
        bonus_type = type_element.text
        
        # normalize type "Cap Increase" to "Cap" for consistency with the 
        # colloquial phrasing (e.g. "Strength Cap")
        if(bonus_type == "Cap Increase"):
            bonus.effect = bonus.effect + " Cap"
        
        # ignore empty bonuses
        if(bonus.effect):
            # add this bonus to the item
            item.add_bonus(bonus)
            
    return item

#
# This function returns a string containing XML compatible suitable to be 
# imported into Loki
#
def write_item_to_xml(item):
    
    scitem = ET.Element('SCItem')
    
    activity_state = SubElement(scitem, "ActivityState")
    activity_state.text = "drop"
    
    location = SubElement(scitem, "Location")
    location.text = item.location
    
    realm = SubElement(scitem, "Realm")
    realm.text = item.realm
    
    item_name = SubElement(scitem, "ItemName")
    item_name.text = item.name
    
    afdps = SubElement(scitem, "AFDPS")
    afdps.text = "16.5"
    
    bonus = SubElement(scitem, "Bonus")
    bonus.text = "0"
    
    item_quality = SubElement(scitem, "ItemQuality")
    item_quality.text = "100"
    
    equipped = SubElement(scitem, "Equipped")
    equipped.text = "1"
    
    level = SubElement(scitem, "Level")
    level.text = "50"
    
    offhand = SubElement(scitem, "OFFHAND")
    offhand.text = "no"
    
    source = SubElement(scitem, "SOURCE")
    source.text = "drop"
    
    type = SubElement(scitem, "TYPE")
    type.text = "Unspecified"
    
    damage_type = SubElement(scitem, "DAMAGETYPE")
    damage_type.text = "Thrust"
    
    speed = SubElement(scitem, "Speed")
    speed.text = "4.0"
    
    class_restrictions = SubElement(scitem, "CLASSRESTRICTIONS")
    class_ = SubElement(class_restrictions, "CLASS")
    class_.text = "All"
    
    is_unique = SubElement(scitem, "ISUNIQUE")
    is_unique.text = "0"
    
    oracle_ignore = SubElement(scitem, "ORACLE_IGNORE")
    oracle_ignore.text = "0"
    
    user_value = SubElement(scitem, "USER_VALUE")
    user_value.text = "0"
    
    variant = SubElement(scitem, "VARIANT")

    associate = SubElement(scitem, "ASSOCIATE", {"IsParent":"0"})
    
    equiplist = SubElement(scitem, "EQUIPLIST")
    #slot = SubElement(equiplist, )
    
    dropitem = SubElement(scitem, "DROPITEM")
    
    for slot_num in range(10):
        slot = SubElement(dropitem, "SLOT", {"Number":str(slot_num)})
    
        remakes = SubElement(slot, "Remakes")
        remakes.text = "0"
        
        effect = SubElement(slot, "Effect")
        effect.text = "some effect"
        
        quality = SubElement(slot, "Qua")
        quality.text = "99"
        
        amount = SubElement(slot, "Amount")
        amount.text = "3"
        
        done = SubElement(slot, "Done")
        done.text = "0"
        
        time = SubElement(slot, "Time")
        time.text = "0"
        
        type = SubElement(slot, "Type")
        type.text = "Skill" 
        
    #print(ET.tostring(scitem))
    print(prettify(scitem))
    return ""
