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
		"level TINYINT UNSIGNED," .
		"hash VARCHAR(33)," .
		"confidence SMALLINT UNSIGNED DEFAULT 0" .
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

    print "dropping IncrementConfidence stored procedure\n";
	$sql = "DROP PROCEDURE IF EXISTS IncrementConfidence;";
	$dbh->do($sql);

	print "creating the IncrementConfidence stored procedure\n";
	$sql = 
		"CREATE PROCEDURE IncrementConfidence(IN id INT) " .
		"BEGIN " .
		"DECLARE c SMALLINT UNSIGNED; " .
		"SELECT confidence INTO c FROM item WHERE item_id=id; " .
		"SET c = c + 1; " .
		"UPDATE item SET confidence=c WHERE item_id=id; " .
		"END";
	$dbh->do($sql);

	print "done!\n";
}
