<!doctype HTML>
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
?>
<html>
<head>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

<script>
// this function serializes the search form data and sends it to the back end
// search processor (search.php)
function doSearch() {
	//console.log("in doSearch");

	// figure out what the user typed in for the name
	var itemname = document.getElementById("itemname").value;
	//console.log(itemname);

	// figure out what the user selected for the first bonus
	var bonus1id = document.getElementById("bonus1").selectedIndex;
	//console.log(bonus1id);

	var slot = document.getElementById("slot").value;

	// if the form is empty, clear the result table
	if(slot.length == 0 && bonus1id == 0 && itemname.length == 0) {
		console.log("clearing result table");

		// get a handle to the result table
		var table = document.getElementById("resulttable");

		// form is empty, clear the table
		for(var j=table.rows.length-1; j>=0; j--) {
			table.deleteRow(j);
		}
	}
	
	// form has data, do the search!
	else {
		// serialize the search parameters so they can be sent to the 
		// back end search processor
		var searchparams = $("form").serialize();
		console.log(searchparams);

		// post the search parameters to search.php.  if matching items
	   	// are found, the result will be an array of JSON objects.
		$.post("search.php", {data:searchparams}, searchCallback);
	}
}

// this function will be called by jQuery.post if the request succeeds.  It will
// examine the result from search.php and display the result.
//
// @param data			the response data from search.php
// @param status		the status of the HTTP Post
function searchCallback(data, status) {
	//console.log("in searchCallback");
	//console.log(data);

	// parse the JSON result so it can be displayed
	var result = $.parseJSON(data);
	//console.log(obj[0].name);
	//console.log(result.length);

	// get a handle to the result table
	var table = document.getElementById("resulttable");

	// first delete all rows from the table
	for(var j=table.rows.length-1; j>=0; j--) {
		table.deleteRow(j);
	}

	// loop through the array of objects
	for(var i=0; i<result.length; i++) {
		//console.log(result[i].name);

		// append a row to the table (-1 means insert the new row at the end)
		var row = table.insertRow(-1);

		// add a cell to the row for this item
		var cell = row.insertCell(0);
		cell.innerHTML = "<a href=\"showitem.php?id=" +
			result[i].item_id + "\">" + result[i].name +
			"</a>";
	}
}

// perform some initialization stuff after the document is loaded
$(document).ready(function() {
	// add a handler to the itemname textbox's keyup event.  this is a 
	// better event to use than change, because it doesn't require 
	// the control to lose focus.
	document.getElementById("itemname").onkeyup = function() {doSearch()};

	document.getElementById("bonus1").onchange = function() {doSearch()};
	document.getElementById("slot").onchange = function() {doSearch()};
});
</script>

</head>
<body>
<form>

Slot: <select name="slot" id="slot">
<option value="">-</option>
<?php
$sql = "SELECT DISTINCT(slot) as slot FROM item;";

if($result = $mysqli->query($sql)) {
	while($r = $result->fetch_assoc()) {
		$slot = $r["slot"];
		print "<option value=\"$slot\">" . $r["slot"] . "</option>\n";
	}
}
?>
</select><br />

Bonus: <select name="bonus1" id="bonus1">
<option value="0">-</option>
<?php
$sql = "SELECT * FROM bonus;";

if($result = $mysqli->query($sql)) {
	while($r = $result->fetch_assoc()) {
		$bonusid = $r["bonus_id"];
		print "<option value=\"$bonusid\">" . $r["name"] . "</option>\n";
	}
}
?>
</select><br />

Name: <input type="text" name="itemname" id="itemname"><br />
</form>

<!-- this table will store the query result -->
<table id="resulttable">
</table>

</body>
</html>
<?php
$mysqli->close();
?>
