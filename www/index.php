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

$sql = "SELECT * FROM item;";

?>
<table border=1>
<tr>
<td>item_id</td>
<td>name</td>
<td>realm</td>
<td>slot</td>
<td>level</td>
</tr>
<?php
if($mysqli->multi_query($sql)) {
	do {
		if($result = $mysqli->use_result()) {
			while($row = $result->fetch_assoc()) {
				print "<tr>";
				printf("<td>%d</td>", $row["item_id"]);
				printf("<td><a href=\"showitem.php?id=%d\">%s</a></td>",
						$row["item_id"], $row["name"]);
				printf("<td>%s</td>", $row["realm"]);
				printf("<td>%s</td>", $row["slot"]);
				printf("<td>%d</td>", $row["level"]);
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
