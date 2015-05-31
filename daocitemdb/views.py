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

    # set up context
    #context = dict()
    context = {"slot_list" : slot_list}

    # render output
    return render(request, "searchform.html", context)

#
# This view accepts query parameters from the search form, performs the query,
# and returns the JSON'd result to the searchform to be displayed to the user
#
def search(request):
    #log.info("search being requested!")
    
    # get the item name
    item_name = request.GET['itemname']
    log.debug("item_name: " + item_name)
    
    json_result = ""
    
    # get a filtered list of Items
    if item_name:
        # this will yield a QuerySet of objects matching the search parameters
        item_list = Item.objects.filter(name__startswith=item_name)
        
        # we need to serialize the QuerySet to JSON
        json_result = serializers.serialize("json", item_list)
        #log.debug("item_list: " + item_list.__str__())
        #log.debug("some_json: " + json_result)
    
    # return the search result
    #return JsonResponse({'foo':'bar'})
    return HttpResponse(json_result)
