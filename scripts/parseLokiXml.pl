#!/usr/bin/perl
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
# This script will extract and display some relevant fields from a Loki item 
# XML file.  It is meant to be used for testing only.
#
#-------------------------------------------------------------------------------

use strict;
use warnings;
use XML::DOM;

#-------------------------------------------------------------------------------
# getElementValue
#
# This subroutine uses XML::DOM to search for and extract the value of a
# XML::DOM::Text element with the specified name, living under the specified
# XML::DOM::Node
#
# The first parameter to this subroutine is an XML::DOM::Node.  It is expected 
# that the specified element name lives under this node.
#
# The second parameter to this subroutine is the name of the element to search 
# for
#
# The subroutine will return the text value of the first element under the 
# specified node matching the specified name, or an empty string if the 
# element name wasn't found.
#-------------------------------------------------------------------------------
sub getElementValue
{
	# the first parameter should be a XML::DOM::Node under which the element to 
	# search for lives
	my $nodeToSearch = $_[0];

	# the second parameter should be the name of the element to search for
	my $elementName = $_[1];

	# get a list of nodes matching the element name
	my $nodeList = $nodeToSearch->getElementsByTagName($elementName);

	# hopefully there is at least one result
	if($nodeList->getLength >= 1)
	{
		# we're only going to look at the first mathing element
		my $node = $nodeList->item(0);

		# make sure $node is a real thing
		if(defined $node)
		{
			# grab the first child of $node (that's where the text value is)
			my $child = $node->getFirstChild;

			# make sure $child is a real thing
			if(defined $child)
			{
				# grab the text value and return it
				my $nodeText = $child->getNodeValue;
				return $nodeText;
			}
		}
	}

	# didn't find what we were looking for, return an empty string
	return "";
}

my $parser = new XML::DOM::Parser;
my $doc = $parser->parsefile("/var/itemdb/uploads/Mystic\ Ivybound\ Sleeves_50.xml");

# get a NodeList of descendent elements with the name "SCItem"
# (this should be the root node in a Loki item XML document)
my $nodes = $doc->getElementsByTagName("SCItem");
my $n = $nodes->getLength;

for (my $i = 0; $i < $n; $i++)
{
	# get the item at position i out of the NodeList
	my $node = $nodes->item($i);

	my $name = getElementValue($node, "ItemName");
	print "ItemName: $name\n";

	my $realm = getElementValue($node, "Realm");
	print "Realm: $realm\n";

	my $level = getElementValue($node, "Level");
	print "Level: $level\n";

	my $location = getElementValue($node, "Location");
	print "Location: $location\n";

	# get all of the bonus values
	my $dropItemNodeList = $node->getElementsByTagName("DROPITEM");
	if($dropItemNodeList->getLength == 1)
	{
		my $slotNodeList = $dropItemNodeList->item(0)->getElementsByTagName("SLOT");
		my $m = $slotNodeList->getLength;
		
		for (my $j = 0; $j < $m; $j++)
		{
			my $slotNode = $slotNodeList->item($j);
			my $effect = getElementValue($slotNode, "Effect");
			my $value = getElementValue($slotNode, "Amount");

			#if($effect != "")
			{
				print "Bonus $j: $value $effect\n";
			}
		}
	}
}

$doc->dispose;
