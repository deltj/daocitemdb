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
# This file includes model definitions for daocitemdb
#
#-------------------------------------------------------------------------------
from django.db import models
import hashlib

# This model represents a Slot.  A Slot is a place on a character where an item
# can be equipped.  For example, an item that is a necklace may be equipped in
# the Necklace slot.
class Slot(models.Model):
    
    # The name of this Slot
    name = models.CharField(max_length=50)
    
    # This override provides a short, human-readable description
    def __str__(self):
        return self.name

# This model represents a Bonus that an Item may have.
class Bonus(models.Model):
    
    # The name of this Bonus
    name = models.CharField(max_length=50)
    
    # This override provides a short, human-readable description
    def __str__(self):
        return self.name

# This model represents a specific bonus that a specific item has.
class ItemBonus(models.Model):
    
    # The Item having the Bonus
    item = models.ForeignKey("daocitemdb.Item")
    
    # The Bonus the Item has 
    bonus = models.ForeignKey("daocitemdb.Bonus")
    
    # The amount of the bonus
    amount = models.SmallIntegerField(default=0)
    
    def bonus_name(self):
        return self.bonus.name

# This model represents an Item.  An Item is an object in DAoC that may be 
# equipped by a character.
class Item(models.Model):
    # This DateTime describes the moment at which this Item was added to the
    # database
    added = models.DateTimeField(auto_now_add=True)
    
    # The name of this item
    name = models.CharField(max_length=200, default="")
    
    # The realm that this item belongs to
    realm = models.CharField(max_length=10, default="")
    
    # Slot in which this Item may be equipped
    slot = models.ForeignKey(Slot, null=True)
    
    # The item's level
    level = models.SmallIntegerField(default=0)
    
    # A hash value that (hopefully) uniquely identifies this item (used to 
    # prevent duplicate items from being added to the database)
    hash = models.CharField(max_length=33, default="")
    
    # An integer that describes the likelihood that this item is a real-actual
    # item from the game, and not some erroneous item that doesn't exist.  The
    # idea behind this field is that each time items are imported (e.g. from 
    # Loki XML), if an item being imported is the same as an item that's already
    # in the database, we'll increase that item's confidence since now we've 
    # seen it N+1 times.  Conceptually this is saying that the more often an 
    # item has been seen, the more likely it is to be a real and correct.
    confidence = models.SmallIntegerField(default=0)
    
    # This override provides a short, human-readable description
    def __str__(self):
        return self.name
    
    # Generate a CSV representation of the bonuses for this item.
    def get_bonus_csv(self):
        
        # get the bonus list for this item
        bonus_list = ItemBonus.objects.filter(item_id=self.id).order_by("bonus__name")
        
        # generate the csv
        csv_string = ""
        for bonus in bonus_list:
            csv_string += bonus.bonus_name() + "," + str(bonus.amount) + ","
            
        return csv_string
    
    # This function determines the hash value for this item by first creating 
    # a comma-separated-variable description of all of the item's bonuses, then
    # computing the MD5 sum for the CSV string.
    def get_bonus_hash(self):
        
        csv_string = self.get_bonus_csv()
        return hashlib.md5(csv_string.encode("utf-8")).hexdigest()
