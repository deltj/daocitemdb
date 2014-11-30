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
use Bonus;
use Digest::MD5 qw(md5 md5_hex);

#-------------------------------------------------------------------------------
#
# constructor for Item
#
#-------------------------------------------------------------------------------
sub new {
	my $class = shift;
	my @bonuses = ();

	# anonymous hash for Item properties
	my $self = {
		_name => undef,
		_realm => undef,
		_slot => undef,
		_level => undef,
		_bonuses => []
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

sub getRealm {
	my ($self) = @_;
	return $self->{_realm};
}

sub setRealm {
	my ($self, $realm) = @_;
	$self->{_realm} = $realm if defined($realm);
	return $self->{_realm};
}

sub getSlot {
	my ($self) = @_;
	return $self->{_slot};
}

sub setSlot {
	my ($self, $slot) = @_;
	$self->{_slot} = $slot if defined($slot);
	return $self->{_slot};
}

sub getLevel {
	my ($self) = @_;
	return $self->{_level};
}

sub setLevel {
	my ($self, $level) = @_;
	$self->{_level} = $level if defined($level);
	return $self->{_level};
}

sub addBonus {
	my ($self, $bonusName, $bonusValue) = @_;

	my $bonus = new Bonus;
	$bonus->setName($bonusName);
	$bonus->setValue($bonusValue);
	push @{ $self->{_bonuses} }, $bonus;

	return;
}

sub getHash {
	my ($self) = @_;

	# get a condensed string representation of the class (this will basically
	# be a CSV of all of this Item's attributes)
	my $itemString;
	
	$itemString .= $self->getName() . ",";
	$itemString .= $self->getRealm() . ",";
	$itemString .= $self->getSlot() . ",";
	$itemString .= $self->getLevel() . ",";

	foreach (@{ $self->{_bonuses} }) {
		$itemString .= $_->getName() . ",";
		$itemString .= $_->getValue() . ",";
	}

	# ok now we have a CSV, hash it
	my $datHash = md5_hex($itemString);
}

#-------------------------------------------------------------------------------
#
# Print out a human-readable description of this item
#
#-------------------------------------------------------------------------------
sub print
{
	my ($self) = @_;

	# display basic item attributes
	print "Item Object:\n";
	printf "Name:\t%s\n", $self->getName();
	printf "Realm:\t%s\n", $self->getRealm();
	printf "Slot:\t%s\n", $self->getSlot();
	printf "Level:\t%s\n", $self->getLevel();

	# display item bonus list
	foreach (@{ $self->{_bonuses} }) {
		printf "Bonus:\t%s: %s\n", $_->getName(), $_->getValue();
	}

	printf "Hash:\t%s\n", $self->getHash();
}

1;
