<!doctype HTML>
<html>
<head>
</head>
<body>
<?php
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

$item_id = $_GET["id"];
$sql = "SELECT item.*, bonus.name as bonusname, item_bonuses.amount as amount " .
	"FROM item " .
	"INNER JOIN item_bonuses ON item.item_id = item_bonuses.item_id " .
	"INNER JOIN bonus ON bonus.bonus_id = item_bonuses.bonus_id " .
	"WHERE item.item_id=$item_id;";
?>
<table border=1>
<?php
if($result = $mysqli->query($sql)) {
	$row = $result->fetch_assoc();

	print "<tr>";
	print "<td>item_id</td>";
	printf("<td>%d</td>", $row["item_id"]);
	print "</tr>";

	print "<tr>";
	print "<td>name</td>";
	printf("<td>%s</td>", $row["name"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>realm</td>";
	printf("<td>%s</td>", $row["realm"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>slot</td>";
	printf("<td>%s</td>", $row["slot"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>level</td>";
	printf("<td>%d</td>", $row["level"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>bonus 1</td>";
	printf("<td>%d %s</td>",
			$row["amount"],
			$row["bonusname"]);
	print "</tr>";
	
	$bonus = 2;
	while($row = $result->fetch_assoc()) {
		print "<tr>";
		print "<td>bonus $bonus</td>";
		printf("<td>%d %s</td>",
			$row["amount"],
			$row["bonusname"]);
		print "</tr>";
		$bonus++;
	}	
	
	$result->close();
} else {
	print_r($mysqli->error_list);
}

$mysqli->close();
?>
</table>
</body>
</html>
