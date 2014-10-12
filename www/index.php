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

$sql = "SELECT * FROM item;";

?>
<table id="results">
<tr>
<td id="results">Name</td>
<td id="results">Realm</td>
<td id="results">Slot</td>
<td id="results">Level</td>
</tr>
<?php
if($mysqli->multi_query($sql)) {
	do {
		if($result = $mysqli->use_result()) {
			while($row = $result->fetch_assoc()) {
				print "<tr>";
				printf("<td id=\"results\"><a href=\"showitem.php?id=%d\">%s</a></td>",
						$row["item_id"], $row["name"]);
				printf("<td id=\"results\">%s</td>", $row["realm"]);
				printf("<td id=\"results\">%s</td>", $row["slot"]);
				printf("<td id=\"results\">%d</td>", $row["level"]);
				print "</tr>";
			}
			$result->close();
		}
	} while($mysqli->next_result());
}

$mysqli->close();
?>
</table>
</body>
</html>
