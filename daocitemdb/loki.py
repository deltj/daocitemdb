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
#from _elementtree import SubElement
try:
    # first try to use the faster c-implementation of ElementTree
    import xml.etree.cElementTree as ET
except ImportError:
    # if that's not available, fall back to the python implementation
    import xml.etree.ElementTree as ET
from xml.dom import minidom    
from daocitemdb.models import Item, Slot, Bonus, ItemBonus
from django.core.exceptions import ObjectDoesNotExist

import logging

# set up the logger
log = logging.getLogger(__name__)

def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# This function accepts a string that describes a Slot, and then either returns
# the Slot in the database that the string represents, or adds a new Slot to the
# database if one doesn't yet exist.
def get_slot(slot_name):
    
    # search the database for a Slot having the specified name
    try:
        slot = Slot.objects.get(name=slot_name)
        log.info("slot (" + slot_name +") found ")
        
    except ObjectDoesNotExist:
        log.info("slot (" + slot_name +") not found, creating a new one")
        
        # if one wasn't found, create it
        slot = Slot.objects.create(name=slot_name)
        slot.save()
    
    # by now slot should be a real thing, one way or another
    return slot

# This function accepts a string that describes a Bonus, and then either returns
# the Bonus in the database that the string represents, or adds a new Bonus
# to the database if one doens't yet exist.
def get_bonus(bonus_name):

    # search the database for a Bonus having the specified name
    try:
        bonus = Bonus.objects.get(name=bonus_name)
        log.info("bonus (" + bonus_name +") found")
        
    except ObjectDoesNotExist:
        log.info("bonus (" + bonus_name +") not found, creating a new one")
        
        # if one wasn't found, create it
        bonus = Bonus.objects.create(name=bonus_name)
        bonus.save()
    
    # by now bonus should be a real thing, one way or another
    return bonus
    
#
# This function processes a Loki XML file, which is passed to this function as
# a string, and adds the item described in the XML to the database.
#
def import_item_from_xml(xml_string):
    
    #log.info(xml_string)
    
    # a new Item that we'll construct
    this_item = Item();
    
    # TODO: implement countermeasures against billion laughs and quadratic 
    # blowup attacks
    
    # parse the XML string
    root = ET.fromstring(xml_string)
    
    # locate the ItemName element to get this Item's name
    item_name_element = root.find(".//ItemName")
    this_item.name = item_name_element.text
    
    log.info("processing item (" + this_item.name + ")")

    # locate the Realm element to get this Item's realm
    realm_element = root.find(".//Realm")
    this_item.realm = realm_element.text
    
    # locate the Level element to get this Item's level
    level_element = root.find(".//Level")
    this_item.level = level_element.text
    
    # locate the Location element to get this Item's slot
    location_element = root.find(".//Location")
    this_item.slot = get_slot(location_element.text)
    
    # save the item
    this_item.save()
    
    # locate the DROPITEM element
    dropitem_element = root.find(".//DROPITEM")
    
    # inspect all of the SLOT elements to get this Item's bonuses
    slot_elements = dropitem_element.findall(".//SLOT")
    for slot in slot_elements:

        # locate the Effect element to get the name of this bonus
        bonus_element = slot.find(".//Effect")
        bonus_name = bonus_element.text
        
        # locate the Type element to get the type of bonus (e.g. stat, 
        # resist, stat cap, etc)
        type_element = slot.find(".//Type")
        bonus_type = type_element.text
        
        # normalize type "Cap Increase" to "Cap" for consistency with the 
        # colloquial phrasing (e.g. "Strength Cap")
        if(bonus_type == "Cap Increase"):
            bonus_name = bonus_name + " Cap"
        
        # locate the Amount element to get the amount of this bonus
        amount_element = slot.find(".//Amount")
        bonus_amount = amount_element.text
        
        # ignore empty bonuses
        if(bonus_amount and bonus_name):
            # get a real Bonus for this bonus_name
            this_bonus = get_bonus(bonus_name)
            
            # add this bonus to the item
            item_bonus = ItemBonus(item=this_item,
                                   bonus=this_bonus,
                                   amount=bonus_amount)
            item_bonus.save()
            
    # get this item's hash
    #log.info(this_item.get_bonus_csv())
    #log.info(this_item.get_bonus_hash())
    the_hash = this_item.get_bonus_hash()
    log.info("hash: " + the_hash)

	# look for duplicates by searching for items with the same hash value
    duplicate_list = Item.objects.filter(hash=the_hash)
    if(duplicate_list.count() > 0):
        # If I've done this right... it shouldn't be possible or multiple items
        # to have the same hash.

        item_already_in_db = duplicate_list[0]

        # increment confidence for the first item in the list
        item_already_in_db.confidence += 1
        item_already_in_db.save()

        # delete this_item, since it's a dup
        this_item.delete()

        log.info("duplice found, updating confidence")
    else:
        this_item.hash = the_hash
        this_item.save()

        log.info("unique item found, adding to database")





#
# This function returns a string containing XML compatible suitable to be 
# imported into Loki
#
'''
def write_item_to_xml(item):
    
    scitem = ET.Element('SCItem')
    
    activity_state = SubElement(scitem, "ActiveState")
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
    
    dbsource = SubElement(scitem, "DBSOURCE")
    dbsource.text = "LOKI"
    
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
    equip_slot = SubElement(equiplist, "SLOT", {"NAME":"Right Hand"})
    equip_slot.text = "true"
    
    dropitem = SubElement(scitem, "DROPITEM")
        
    for slot_num in range(10):
        slot = SubElement(dropitem, "SLOT", {"Number":str(slot_num)})
    
        remakes = SubElement(slot, "Remakes")
        remakes.text = "0"
        
        effect = SubElement(slot, "Effect")
        effect.text = "Dexterity"
        
        quality = SubElement(slot, "Qua")
        quality.text = "99"
        
        amount = SubElement(slot, "Amount")
        amount.text = "3"
        
        done = SubElement(slot, "Done")
        done.text = "0"
        
        time = SubElement(slot, "Time")
        time.text = "0"
        
        type = SubElement(slot, "Type")
        type.text = "Stat" 
    
    # return a nicely formatted XML string
    return prettify(scitem)
'''
