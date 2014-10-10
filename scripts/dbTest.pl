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
# Test script for connecting the mysql database
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
}
