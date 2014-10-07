#!/usr/bin/perl
#-------------------------------------------------------------------------------
# Parser for Loki XML files.
#
# Copyright Ted DeLoggio
#-------------------------------------------------------------------------------

use strict;
use warnings;
use XML::DOM;

sub getElementValue
{
	# the first parameter should be a XML::DOM::Node under which the element to 
	# search for lives
	my $nodeToSearch = $_[0];

	# the second parameter should be the name of the element to search for
	my $elementName = $_[1];

	my $nodeList = $nodeToSearch->getElementsByTagName($elementName);
	if($nodeList->getLength == 1)
	{
		my $node = $nodeList->item(0);
		if(defined $node)
		{
			my $child = $node->getFirstChild;
			if(defined $child)
			{
				my $nodeText = $child->getNodeValue;
				return $nodeText;
			}
		}
	}

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
