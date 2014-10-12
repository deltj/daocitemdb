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

my $parser = new XML::DOM::Parser;

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

		my $dbh = DBI->connect('DBI:mysql:mysql_read_default_file=./my.conf',
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

my $numargs = $#ARGV + 1;
if($numargs < 1) {
	print "specify at least one XML file\n";
	exit;
}

print "$numargs files to import...\n";

foreach my $file (@ARGV) {
	importLokiXmlFile($file);
}

print "done!\n";
