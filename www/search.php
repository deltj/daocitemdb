<?php
$serializedData = $_POST['data'];
$unserializedData = array();

parse_str($serializedData,$unserializedData);

$name = $unserializedData["itemname"];
//print_r($name);

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

$sql = "SELECT item_id,name FROM item WHERE name LIKE '%$name%';";

if($result = $mysqli->query($sql)) {
	$rows = array();
	while($r = $result->fetch_assoc()) {
		$rows[] = $r;
	}
	print json_encode($rows);
}

$mysqli->close();
?>
