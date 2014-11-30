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
# A perl class to describe a DAoC item bonus.  An Item may have zero or more
# Bonuses, and this class is used to represent a bonus (its name and value).
#
# I could have done some weird stuff with maps or something (perl doesn't have
# multidimensional arrays) to store Bonus names/values in the Item object,
# an array of Bonus objects seemed cleaner
#
#-------------------------------------------------------------------------------

package Bonus;

use strict;
use warnings;

#-------------------------------------------------------------------------------
#
# constructor for Bonus 
#
#-------------------------------------------------------------------------------
sub new {
	my $class = shift;
	my @bonuses = ();

	# anonymous hash for Bonus properties
	my $self = {
		_name => undef,
		_value => undef
	};
	
	return bless $self, $class;
}

sub getName {
	my ($self) = @_;
	return $self->{_name};
}

sub setName {
	my ($self, $name) = @_;
	$self->{_name} = $name if defined($name);
	return $self->{_name};
}

sub getValue {
	my ($self) = @_;
	return $self->{_value};
}

sub setValue {
	my ($self, $value) = @_;
	$self->{_value} = $value if defined($value);
	return $self->{_value};
}

#-------------------------------------------------------------------------------
#
# Print out a human-readable description of this Bonus 
#
#-------------------------------------------------------------------------------
sub print
{
	my ($self) = @_;

	# display bonus infoz
	print "Bonus Object:\n";
	printf "Name:\t%s\n", $self->getName();
	printf "Value:\t%s\n", $self->getValue();
}

1;
