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
# This script will create the mysql tables for daocitemdb.  All existing data
# will be lost.
#
#-------------------------------------------------------------------------------

use strict;
use warnings;
use DBI;

my $dbh = DBI->connect('DBI:mysql:mysql_read_default_file=./my.conf',undef,undef)
	or die "Failed to connect: " . $DBI::errstr;

# if DBI->connect fails, it will return undef
if(defined $dbh)
{
	print "DBI->connect success!\n";

	# first drop the tables if they exist
	print "dropping item table\n";
	my $sql  = "DROP TABLE IF EXISTS item;";
	$dbh->do($sql);

	print "dropping bonus table\n";
	$sql  = "DROP TABLE IF EXISTS bonus;";
	$dbh->do($sql);

	print "dropping item_bonuses table\n";
	$sql  = "DROP TABLE IF EXISTS item_bonuses;";
	$dbh->do($sql);

	# create the item table
	print "creating item table\n";
	$sql = "CREATE TABLE item (" .
		"item_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY," .
		"ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP," .
		"name VARCHAR(100)," .
		"realm VARCHAR(10)," .
		"slot VARCHAR(10)," .
		"level TINYINT UNSIGNED" .
#		"bonus1_effect VARCHAR(25)," .
#		"bonus1_amount TINYINT,".
#		"bonus2_effect VARCHAR(25)," .
#		"bonus2_amount TINYINT,".
#		"bonus3_effect VARCHAR(25)," .
#		"bonus3_amount TINYINT,".
#		"bonus4_effect VARCHAR(25)," .
#		"bonus4_amount TINYINT,".
#		"bonus5_effect VARCHAR(25)," .
#		"bonus5_amount TINYINT,".
#		"bonus6_effect VARCHAR(25)," .
#		"bonus6_amount TINYINT,".
#		"bonus7_effect VARCHAR(25)," .
#		"bonus7_amount TINYINT,".
#		"bonus8_effect VARCHAR(25)," .
#		"bonus8_amount TINYINT,".
#		"bonus9_effect VARCHAR(25)," .
#		"bonus9_amount TINYINT," .
#		"bonus10_effect VARCHAR(25)," .
#		"bonus10_amount TINYINT" .
		");";
	$dbh->do($sql);

	# create the bonus table
	print "creating bonus table\n";
	$sql = "CREATE TABLE bonus (" .
		"bonus_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY," .
		"name VARCHAR(100)" .
		");";
	$dbh->do($sql);

	# create the item_bonuses table
	print "creating item_bonuses table\n";
	$sql = "CREATE TABLE item_bonuses (" .
		"item_id INT NOT NULL," .
		"bonus_id INT NOT NULL," .
		"amount TINYINT UNSIGNED" .
		");";
	$dbh->do($sql);

	print "done!\n";
}
