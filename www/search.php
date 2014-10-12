<?php
$serializedData = $_POST['data'];
$unserializedData = array();

parse_str($serializedData,$unserializedData);

$name = $unserializedData["itemname"];
$bonus1id = $unserializedData["bonus1"];
$slot = $unserializedData["slot"];

require('creds.php');

$mysqli = new mysqli($dbhost,
	$dbuser, 
	$dbpass,
	$dbname,
	$dbport);

// check for connection error
if (mysqli_connect_errno()) {
	echo "connect error!";
}

$sql = "";
/*
$sql = "SELECT item.*, bonus.name as bonusname, item_bonuses.amount as amount " .
	"FROM item " .
	"INNER JOIN item_bonuses ON item.item_id = item_bonuses.item_id " .
	"INNER JOIN bonus ON bonus.bonus_id = item_bonuses.bonus_id " .
	"WHERE item.item_id=$item_id;";
*/

if(strlen($name) > 0) {
	// item name is valid
	if($bonus1id > 0) {
		// item name and bonus id are valid
		if(strlen($slot) > 0) {
			// item name, bonus, and slot are valid
		} else {
			// item name and bonus are valid
		}
	} else {
		// item name is valid
		if(strlen($slot) > 0) {
			// item name and slot are valid
		} else {
			// item name is valid
			$sql = "SELECT item_id, name " .
				"FROM item " .
				"WHERE name LIKE '%$name%';";
		}
	}
} else {
	// item name is not valid
	if($bonus1id > 0) {
		// bonus id is valid
		if(strlen($slot) > 0) {
			// bonus id and slot are valid
			$sql = "SELECT item.item_id, item.name " .
				"FROM item_bonuses ".
				"INNER JOIN item ON item_bonuses.item_id = item.item_id " .
				"WHERE item_bonuses.bonus_id = $bonus1id AND item.slot = '$slot';";
		} else {
			// bonus id is valid
			$sql = "SELECT item.item_id, item.name " .
				"FROM item_bonuses " .
				"INNER JOIN item ON item_bonuses.item_id = item.item_id " .
				"WHERE item_bonuses.bonus_id = $bonus1id;";
		}
	} else {
		// item name and bonus are not valid
		if(strlen($slot) > 0) {
			// slot is valid
			$sql = "SELECT item_id, name " .
				"FROM item " .
				"WHERE slot = '$slot';";
		} else {
			// nothing is valid
		}
	}
}


if(strlen($sql) > 0) {
	if($result = $mysqli->query($sql)) {
		$rows = array();
		while($r = $result->fetch_assoc()) {
			$rows[] = $r;
		}
		print json_encode($rows);
	}
}

$mysqli->close();
?>
