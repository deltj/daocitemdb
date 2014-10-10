<!doctype HTML>
<html>
<head>
</head>
<body>
<?php
//$dbhost = $_SERVER['RDS_HOSTNAME'];
//$dbport = $_SERVER['RDS_PORT'];
//$dbname = $_SERVER['RDS_DB_NAME'];
//$dbuser = $_SERVER['RDS_USERNAME'];
//$dbpass = $_SERVER['RDS_PASSWORD'];

$link = mysqli_connect($dbhost,
	$dbuser, 
	$dbpass,
	$dbname,
	$dbport);

// check for connection error
if ($link->connect_error) {
	echo "connect error!";
}
?>
</body>
</html>
