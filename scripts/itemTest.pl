#!/usr/bin/perl

use strict;
use warnings;
use Item;

my $item = new Item();

$item->setName("dat name");
printf("Name: %s\n", $item->getName);

$item->setRealm("Hibernia");
printf("Realm: %s\n", $item->getRealm);

$item->setSlot("Ring");
printf("Slot: %s\n", $item->getSlot);

$item->setLevel(50);
printf("Level: %d\n", $item->getLevel);

printf "Loki XML: \n %s\n\n", $item->getLokiXml();
