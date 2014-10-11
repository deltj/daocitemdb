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
$sql = "SELECT * FROM item where item_id=$item_id;";

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
			$row["bonus1_amount"],
			$row["bonus1_effect"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>bonus 2</td>";
	printf("<td>%d %s</td>",
			$row["bonus2_amount"],
			$row["bonus2_effect"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>bonus 3</td>";
	printf("<td>%d %s</td>",
			$row["bonus3_amount"],
			$row["bonus3_effect"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>bonus 4</td>";
	printf("<td>%d %s</td>",
			$row["bonus4_amount"],
			$row["bonus4_effect"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>bonus 5</td>";
	printf("<td>%d %s</td>",
			$row["bonus5_amount"],
			$row["bonus5_effect"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>bonus 6</td>";
	printf("<td>%d %s</td>",
			$row["bonus6_amount"],
			$row["bonus6_effect"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>bonus 7</td>";
	printf("<td>%d %s</td>",
			$row["bonus7_amount"],
			$row["bonus7_effect"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>bonus 8</td>";
	printf("<td>%d %s</td>",
			$row["bonus8_amount"],
			$row["bonus8_effect"]);
	print "</tr>";
	
	print "<tr>";
	print "<td>bonus 9</td>";
	printf("<td>%d %s</td>",
			$row["bonus9_amount"],
			$row["bonus9_effect"]);
	print "</tr>";
	
	$result->close();
}

$mysqli->close();
?>
</table>
</body>
</html>
