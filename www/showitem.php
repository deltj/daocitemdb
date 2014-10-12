<!doctype HTML>
<html>
<head>
<link rel="stylesheet" href="css.css" type="text/css">
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
<table id="results"> 
<?php
if($result = $mysqli->query($sql)) {
	$row = $result->fetch_assoc();

	print "<tr>";
	print "<td id=\"show\">Name</td>";
	printf("<td>%s</td>", $row["name"]);
	print "</tr>";
	
	print "<tr>";
	print "<td id=\"show\">Realm</td>";
	printf("<td>%s</td>", $row["realm"]);
	print "</tr>";
	
	print "<tr>";
	print "<td id=\"show\">Slot</td>";
	printf("<td>%s</td>", $row["slot"]);
	print "</tr>";
	
	print "<tr>";
	print "<td id=\"show\">Level</td>";
	printf("<td>%d</td>", $row["level"]);
	print "</tr>";
	
	print "<tr>";
	print "<td id=\"show\" style=\"vertical-align:top\">Bonuses</td><td>";
	printf("%d %s<br />\n",
			$row["amount"],
			$row["bonusname"]);
	
	while($row = $result->fetch_assoc()) {
		printf("%d %s<br />\n",
			$row["amount"],
			$row["bonusname"]);
	}	
	print "</td></tr>\n";
	
	$result->close();
} else {
	print_r($mysqli->error_list);
}

$mysqli->close();
?>
</table>
</body>
</html>
