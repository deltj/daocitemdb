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
			while($row = $result->fetch_row()) {
				print "<tr>";
				printf("<td>%d</td>", $row[0]);
				printf("<td>%s</td>", $row[1]);
				printf("<td>%s</td>", $row[2]);
				printf("<td>%s</td>", $row[3]);
				printf("<td>%d</td>", $row[4]);
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
