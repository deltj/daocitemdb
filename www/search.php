<?php
$serializedData = $_POST['data'];
$unserializedData = array();

parse_str($serializedData,$unserializedData);

$name = $unserializedData["itemname"];
//print_r($name);

$bonus1id = $unserializedData["bonus1"];

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
	if($bonus1id > 0) {
		// search by name and bonus1id
	} else {
		// search by name only
		$sql = "SELECT item_id,name FROM item WHERE name LIKE '%$name%';";
	}
} else {
	// search bu bonus1id only
	$sql = "SELECT item.item_id, item.name FROM item_bonuses " .
		"INNER JOIN item ON item_bonuses.item_id = item.item_id " .
		"WHERE item_bonuses.bonus_id = $bonus1id";
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
