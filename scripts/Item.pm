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
# A perl class to describe a DAoC item.  Item is the base class for specific
# item types.
#
#-------------------------------------------------------------------------------

package Item;

use strict;
use warnings;

#-------------------------------------------------------------------------------
#
# constructor for Item
#
#-------------------------------------------------------------------------------
sub new {
	my $class = shift;
	my $self = {
		_name => undef,
		_realm => undef,
		_slot => undef,
		_level => undef
	};
	
	return bless $self, $class;
}

sub getName {
	my ($self, $name) = @_;
	$self->{_name} = $name if defined($name);
	return $self->{_name};
}

sub setName {
	my $self = shift;
	my $name = shift;
	$self->{_name} = $name;
}

sub getRealm {
	my ($self, $realm) = @_;
	$self->{_realm} = $realm if defined($realm);
	return $self->{_realm};
}

sub setRealm {
	my $self = shift;
	my $realm = shift;
	$self->{_realm} = $realm;
}

sub getSlot {
	my ($self, $slot) = @_;
	$self->{_slot} = $slot if defined($slot);
	return $self->{_slot};
}

sub setSlot {
	my $self = shift;
	my $slot= shift;
	$self->{_slot} = $slot;
}

sub getLevel {
	my ($self, $level) = @_;
	$self->{_level} = $level if defined($level);
	return $self->{_level};
}

sub setLevel {
	my $self = shift;
	my $level = shift;
	$self->{_level} = $level;
}

#-------------------------------------------------------------------------------
#
# Print out a string representation of this item
#
#-------------------------------------------------------------------------------
#sub print
#{
#	my ($self) = @_;
#
#	print "Name: $self->Name\n";
#}

1;
