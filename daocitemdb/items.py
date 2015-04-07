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
# This file contains Python classes to represent DAoC items and their various
# attributes. 
#
#-------------------------------------------------------------------------------
        
#
# This class represents a DAoC Item
#
class Item(object):
        
    #
    # Item constructor
    #
    def __init__(self):
        self.name = ""
        self.realm = ""
        self.slot = ""
        self.level = 0      

    #
    # returns the name of this item
    #
    def get_name(self):
        return self.__name
    
    #
    # sets the name of this item
    #
    def set_name(self, value):
        self.__name = value

    #
    # returns the realm for this item
    #
    def get_realm(self):
        return self.__realm

    #
    # sets the realm for this item
    #
    def set_realm(self, value):
        self.__realm = value

    #
    # returns this item's slot
    #
    def get_slot(self):
        return self.__slot

    #
    # sets this item's slot
    #
    def set_slot(self, value):
        self.__slot = value

    #
    # returns this items's level
    #
    def get_level(self):
        return self.__level

    #
    # sets this item's level
    #
    def set_level(self, value):
        self.__level = value
    
    #
    # adds the specified bonus to this item's list of bonuses
    #
    def add_bonus(self, bonus):
        self.bonuses.append(bonus)

    #
    # generates a human-readable string representation of this item
    #
    def __str__(self, *args, **kwargs):
        s =  "--------------------\n"
        s += "DAoC Item:\n"
        s += "name: {0}\n".format(self.name)
        s += "realm: {0}\n".format(self.realm)
        s += "level: {0}\n".format(self.level)
        s += "slot: {0}\n".format(self.slot)
        for bonus in self.bonuses:
            s += "{0}: {1}\n".format(bonus.effect, bonus.amount)
        s +=  "--------------------\n"
        return s
    
    #
    # the name of this item
    #
    name = property(get_name, set_name, None, None)
    
    #
    # which realm this item belongs to
    #
    realm = property(get_realm, set_realm, None, None)
    
    #
    # which slot this item may be used in
    #
    slot = property(get_slot, set_slot, None, None)
    
    #
    # the level of this item
    #
    level = property(get_level, set_level, None, None)
    
    #
    # a list of bonuses that this item grants
    #
    bonuses = []

#
# This class represents a single bonus for a DAoC Item.  Items typically have
# more than one bonus.
#
class Bonus(object):

    #
    # get the effect of this bonus
    #
    def get_effect(self):
        return self.__effect

    #
    # set the effect of this bonus
    #
    def set_effect(self, value):
        self.__effect = value
     
    #
    # get the amount of this bonus
    #   
    def get_amount(self):
        return self.__amount

    #
    # set the amount of this bonus
    #
    def set_amount(self, value):
        self.__amount = value
     
    #
    # The effect is basically the name or identifier for this bonus.  For 
    # example, if the bonus is "Strength Cap 5", then "Strength Cap" is the
    # effect.
    effect = property(get_effect, set_effect, None, None)
    
    #
    # The amount of the bonus.  For example, if the bonus is "Strength Cap 5",
    # then "5" is the amount.
    #
    amount = property(get_amount, set_amount, None, None)
    