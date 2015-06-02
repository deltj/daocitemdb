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
# This file includes view definitions for daocitemdb
#
#-------------------------------------------------------------------------------
from django.shortcuts import render

from .models import Item, Slot, Bonus, ItemBonus
from django.http import HttpResponse
from django.core import serializers
import logging

# set up the logger
log = logging.getLogger(__name__)

#
# This view lists all the items in the database
#
def index(request):
    #log.debug("index being requested!")
    
    item_list = Item.objects.all()
    
    # render output
    context = {'item_list' : item_list}
    return render(request, 'index.html', context)

#
# This view shows the details for a specified item
#
def showitem(request):
    #log.info("showitem being requested!")

    # get the item id   
    iid = request.GET["id"];
    #log.info(id)
    
    # get a list of Items with the specified id (there can only be one)
    item = Item.objects.get(pk=iid)
    
    # get the bonus list for this item
    bonus_list = ItemBonus.objects.filter(item_id=iid)
    
    # render output
    context = {"item" : item, "bonus_list" : bonus_list}
    return render(request, "showitem.html", context)
    
#
# This view renders the search form
#
def searchform(request):
    #log.debug("searchform being requested!")
    
    # get a list of Slots
    slot_list = Slot.objects.all()

    # get a list of Bonuses
    bonus_list = Bonus.objects.all()

    # set up context
    context = {"slot_list" : slot_list, "bonus_list" : bonus_list}

    # render output
    return render(request, "searchform.html", context)

#
# This view accepts query parameters from the search form, performs the query,
# and returns the JSON'd result to the searchform to be displayed to the user
#
def search(request):
    #log.info("search being requested!")
    
    # get the specified item name
    item_name = request.GET.get("itemname", None)
    log.debug("item_name: " + item_name)
    
    # get the specified slot
    slot_id = request.GET.get("slot", None)
    log.debug("slot_id : " + slot_id)

    # get the first specified bonus
    bonus1_id = request.GET.get("bonus1", None)
    log.debug("bonus1_id: " + bonus1_id)
    
    # start with the entire list, and we'll filter it down based on the 
    # search criteria
    #item_list = Item.objects.all()
    item_bonus_list = ItemBonus.objects.all()

    # filter by name
    if item_name and item_name != "":
        item_bonus_list = item_bonus_list.filter(item__name__startswith=item_name)

    # filter by slot
    if slot_id:
        the_slot = Slot.objects.get(pk=slot_id)
        if the_slot:
            item_bonus_list = item_bonus_list.filter(item__slot__id=slot_id)

    # filter by first bonus
    if bonus1_id:
        bonus1 = Bonus.objects.get(pk=bonus1_id)
        if(bonus1):
            item_bonus_list = item_bonus_list.filter(bonus=bonus1)

    # chop the list down to distinct items (currently it contains a row for
    # each bonus in each matching item)
    #item_list.distinct("item__name")

    # it seems that distinct() does not work with the sqlite backend.  As a 
    # workaround, we'll copy the distinct items to a new list.
    item_list = []
    seen_item_ids = []
    for bonus in item_bonus_list:
        if(bonus.item.id not in seen_item_ids):
            seen_item_ids.append(bonus.item.id)
            item_list.append(bonus.item)

    json_result = ""

    # we need to serialize the QuerySet to JSON
    json_result = serializers.serialize("json", item_list)
    #log.debug("item_list: " + item_list.__str__())
    #log.debug("some_json: " + json_result)
    
    # return the search result
    #return JsonResponse({'foo':'bar'})
    return HttpResponse(json_result)
