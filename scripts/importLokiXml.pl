#!/usr/bin/perl -w
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
# This script will import relevant fields from a Loki item XML file into the 
# itembd database.  It is meant to be used for testing only.
#
#-------------------------------------------------------------------------------

use strict;
use warnings;
use XML::DOM;
use DBI;
use Item;

my $parser = new XML::DOM::Parser;

my $dbh = undef;

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

sub importLokiXmlFile {

	my $doc = $parser->parsefile($_[0]);

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

		my $dbh = DBI->connect('DBI:mysql:mysql_read_default_file=/etc/itemdb.conf',
				undef,undef)
			or die "Failed to connect: " . $DBI::errstr;
		#print "DBI->connect success!\n";

		# sql statement to add this item to the item table
		my $sql = "INSERT INTO item (name, realm, slot, level) " .
		   "VALUES (\"$name\", \"$realm\", \"$location\", $level);";
		# print "SQL statement for this item: $sql\n";

		print "adding item to table\n";
		$dbh->do($sql);

		# get item_id for the new item
		$sql = "SELECT item_id FROM item WHERE name = \"$name\";";
		my $qh = $dbh->prepare($sql);
		$qh->execute();
		my @row = $qh->fetchrow();
		my $itemid = $row[0];
		print "using item_id $itemid for item \"$name\"\n";

		# process all of the bonus values
		my $dropItemNodeList = $node->getElementsByTagName("DROPITEM");
		if($dropItemNodeList->getLength == 1)
		{
			my $slotNodeList = $dropItemNodeList->item(0)->getElementsByTagName("SLOT");
			my $m = $slotNodeList->getLength;
		
			for (my $j = 0; $j < $m; $j++)
			{
				my $slotNode = $slotNodeList->item($j);
				my $bonus = getElementValue($slotNode, "Effect");
				my $amount = getElementValue($slotNode, "Amount");

				# what kind of bonus is this?
				my $bonustype = getElementValue($slotNode, "Type");
				
				if($bonustype eq "Cap Increase") {
					$bonus .= " Cap";
				}

				# ignore empty bonuses
				if(length($bonus) > 0) {
					# get the bonus id for this bonus
					$sql = "SELECT bonus_id FROM bonus WHERE name = \"$bonus\";";

					$qh = $dbh->prepare($sql);
					$qh->execute();
					@row = $qh->fetchrow();
					my $rowcount = @row;
				
					my $bonusid = 0;

					# there should be exactly 1 row
					if($rowcount == 1) {
						# this bonus exists, get the id
						$bonusid = $row[0];
						print "using bonus_id $bonusid for bonus \"$bonus\"\n";
					} else {
						# this bonus does not exist, add it
						$dbh->do("INSERT INTO bonus (name) VALUES (\"$bonus\");");
						print "adding new bonus \"$bonus\"\n";

						# re-query for the bonus id
						$dbh->prepare($sql);
						$qh->execute();
						@row = $qh->fetchrow();
						$bonusid = $row[0];
						print "using bonus_id $bonusid for bonus \"$bonus\"\n";
					}

					# update the 3nf table for this item/bonus
					$sql = "INSERT INTO item_bonuses (item_id, bonus_id, amount) " .
						"VALUES ($itemid, $bonusid, $amount);";
					$dbh->do($sql);
					print "adding item ($itemid) bonus ($bonusid) amount ($amount) " .
						"to item_bonuses";

					print "Bonus $j: $amount $bonus\n";
				} else {
					print "ignoring empty bonus in slot $j\n";
				}
			}
		}
	}
}

sub newImportLokiXmlFile {

	my $doc = $parser->parsefile($_[0]);

	# get a NodeList of descendent elements with the name "SCItem"
	# (this should be the root node in a Loki item XML document)
	my $nodes = $doc->getElementsByTagName("SCItem");
	my $n = $nodes->getLength;

	my $item = new Item;

	for (my $i = 0; $i < $n; $i++)
	{
		# get the item at position i out of the NodeList
		my $node = $nodes->item($i);

		my $name = getElementValue($node, "ItemName");
		print "ItemName: $name\n";
		$item->setName($name);

		my $realm = getElementValue($node, "Realm");
		print "Realm: $realm\n";
		$item->setRealm($realm);

		my $level = getElementValue($node, "Level");
		print "Level: $level\n";
		$item->setLevel($level);

		my $location = getElementValue($node, "Location");
		print "Location: $location\n";
		$item->setSlot($location);

		# process all of the bonus values
		my $dropItemNodeList = $node->getElementsByTagName("DROPITEM");
		if($dropItemNodeList->getLength == 1)
		{
			my $slotNodeList = $dropItemNodeList->item(0)->getElementsByTagName("SLOT");
			my $m = $slotNodeList->getLength;
		
			for (my $j = 0; $j < $m; $j++)
			{
				my $slotNode = $slotNodeList->item($j);
				my $bonus = getElementValue($slotNode, "Effect");
				my $amount = getElementValue($slotNode, "Amount");

				# what kind of bonus is this?
				my $bonustype = getElementValue($slotNode, "Type");
				
				if($bonustype eq "Cap Increase") {
					$bonus .= " Cap";
				}

				# ignore empty bonuses
				if(length($bonus) > 0) {
					$item->addBonus($bonus, $amount);

					print "Bonus $j: $amount $bonus\n";
				} else {
					print "ignoring empty bonus in slot $j\n";
				}
			}
		}
	}

	addOrVerifyItem($item);
}

#-------------------------------------------------------------------------------
# getBonusId
#
# This subroutine checks whether the specified Bonus exists in the database.
# If the specified Bonus does not exist in the database it is added.  The 
# bonus_id for the specified Bonus is returned.
#
# The first parameter to this subroutine is the name of a Bonus (the string that
# describes it, e.g. Strength)
#
# This subroutine returns a bonus_id
#-------------------------------------------------------------------------------
sub getBonusId {

	my $bonus= $_[0];

	# get the bonus id for this bonus
	my $sql = "SELECT bonus_id FROM bonus WHERE name = \"$bonus\";";

	my $qh = $dbh->prepare($sql);
	$qh->execute();
	my @row = $qh->fetchrow();
				
	my $bonusid = 0;

	if(@row) {
		# this bonus exists, get the id
		$bonusid = $row[0];
	} else {
		# this bonus does not exist, add it
		$dbh->do("INSERT INTO bonus (name) VALUES (\"$bonus\");");
		print "adding new bonus \"$bonus\"\n";

		# re-query for the bonus id
		$dbh->prepare($sql);
		$qh->execute();
		@row = $qh->fetchrow();
		$bonusid = $row[0];
	}

	return $bonusid;
}

#-------------------------------------------------------------------------------
# addOrVerifyItem
#
# This subroutine considers the specified Item object, adding it to the
# database if it doesn't exist yet, or adds to the Item's verification count
# if it does exist.
#
# The first parameter to this subroutine is an Item object.
#-------------------------------------------------------------------------------
sub addOrVerifyItem {

	my $item = $_[0];

	print "considering the following item:\n";
	$item->print();

	# get item_id for the new item
	my $sql = "SELECT item_id FROM item WHERE hash = \"" . $item->getHash() . "\";";
	my $qh = $dbh->prepare($sql);
	my $rv = $qh->execute();
	#TODO: check return value of execute

	my @row = $qh->fetchrow();
	if(@row) {
		my $itemid = $row[0];
		printf "found a matching item with item_id: %d\n", $itemid;

		$sql = "CALL IncrementConfidence($itemid);";
		$dbh->do($sql);

	} else {
		print "no matching item found, adding a new one\n";

		# sql statement to add this item to the item table
		$sql = "INSERT INTO item (name, realm, slot, level, hash) " .
			"VALUES (" .
			"\"" . $item->getName() . "\"," .
		    "\"" . $item->getRealm() . "\"," .
			"\"" . $item->getSlot() . "\"," .
			$item->getLevel() . "," .
			"\"" . $item->getHash() . "\");";
		# print "SQL statement for this item: $sql\n";

		print "adding item to table\n";
		$dbh->do($sql);

		# get item_id for the new item
		$sql = "SELECT item_id FROM item WHERE hash = \"" . $item->getHash() . "\";";
		my $qh = $dbh->prepare($sql);
		$qh->execute();
		my @row = $qh->fetchrow();
		my $itemid = $row[0];
		print "using item_id $itemid for item \"" . $item->getName() . "\"\n";

		# add each bonus to the item
		foreach (@{ $item->getBonusArrayRef() }) {
			my $bonusName = $_->getName();
			my $bonusValue = $_->getValue();

			my $bonusid = getBonusId($bonusName);
			print "using bonus_id $bonusid for $bonusName\n";

			# update the 3nf table for this Item's bonuses
			$sql = "INSERT INTO item_bonuses (item_id, bonus_id, amount) " .
				"VALUES ($itemid, $bonusid, $bonusValue);";
			$dbh->do($sql);
		}
	}

	# sql statement to add this item to the item table
#	my $sql = "INSERT INTO item (name, realm, slot, level) " .
#	   "VALUES (\"$name\", \"$realm\", \"$location\", $level);";
	# print "SQL statement for this item: $sql\n";

#	print "adding item to table\n";
#	$dbh->do($sql);
}

#==============================================================================
#
# PROGRAM ENTRY POINT 
#
#==============================================================================
my $numargs = $#ARGV + 1;
if($numargs < 1) {
	print "specify at least one XML file\n";
	exit;
}

print "$numargs files to import...\n";

# connect to the database
$dbh = DBI->connect('DBI:mysql:mysql_read_default_file=/etc/itemdb.conf',undef,undef)
	or die "Failed to connect: " . $DBI::errstr;

# process all of the files specified on the command line
foreach my $file (@ARGV) {
	newImportLokiXmlFile($file);
}

print "done!\n";
