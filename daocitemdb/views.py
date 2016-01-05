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
from daocitemdb import loki

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
    
    # get the Item with the specified id
    item = Item.objects.get(pk=iid)
    
    # render output
    context = {"item" : item}
    return render(request, "showitem.html", context)

#
# This view emits Loki XML for the specified item id
#
def lokixml(request):
    #log.info("Loki XML being requested!")

    # get the item id
    iid = request.GET["id"];

    # get the Item with the specified id
    item = Item.objects.get(pk=iid)

    # get Loki XML for this item
    response = HttpResponse(content_type="application/xml")
    response.write(loki.write_item_to_xml(item));
    return response;

    
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
    
    # get the second specified bonus
    bonus2_id = request.GET.get("bonus2", None)
    log.debug("bonus2_id: " + bonus2_id)
    
    # start with the entire list, and we'll filter it down based on the 
    # search criteria
    #item_list = Item.objects.all()
    item_list = Item.objects.all()

    # filter by name
    if item_name and item_name != "":
        item_list = item_list.filter(name__startswith=item_name)

    # filter by slot
    if slot_id:
        the_slot = Slot.objects.get(pk=slot_id)
        if the_slot:
            item_list = item_list.filter(slot=the_slot)

    # filter by first bonus
    if bonus1_id:
        bonus1 = Bonus.objects.get(pk=bonus1_id)
        if(bonus1):
            item_list = item_list.filter(bonuses=bonus1)

    # filter by second bonus
    if bonus2_id:
        bonus2 = Bonus.objects.get(pk=bonus2_id)
        if(bonus2):
            item_list = item_list.filter(bonuses=bonus2)

    # chop the list down to distinct items (currently it contains a row for
    # each bonus in each matching item)
    #item_list.distinct("item__name")

    # it seems that distinct() does not work with the sqlite backend.  As a 
    # workaround, we'll copy the distinct items to a new list.
    #item_list = []
    #seen_item_ids = []
    #for item_bonus in combined_item_bonus_list:
    #    if(item_bonus.item.id not in seen_item_ids):
    #        seen_item_ids.append(item_bonus.item.id)
    #        item_list.append(item_bonus.item)

    json_result = ""

    # we need to serialize the QuerySet to JSON
    json_result = serializers.serialize("json", item_list)
    #log.debug("item_list: " + item_list.__str__())
    #log.debug("some_json: " + json_result)
    
    # return the search result
    #return JsonResponse({'foo':'bar'})
    return HttpResponse(json_result)
