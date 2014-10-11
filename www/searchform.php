<!doctype HTML>
<html>
<head>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

<script>
$(document).ready(function() {
	// add a handler to the itemname textbox's keyup event.  this is a 
	// better event to use than change, because it doesn't require 
	// the control to lose focus.
	$('#itemname').keyup(function() {

		// figure out what the user type in for the name
		var itemname = document.getElementById("itemname").value;
		//console.log(itemname);

		// get a handle to the result table
		var table = document.getElementById("resulttable");

		// an empty query will return a result set containing the entire
		// database, which we do not want.
		if(itemname.length == 0) {
			// itemname textbox is empty, clear the table
			for(var j=0; j<table.rows.length; j++) {
				table.deleteRow(j);
			}
		} else {
			// itemname textbox contains some text

			// serialize the search parameters so they can be sent to the 
			// back end search processor
			var searchparams = $("form").serialize();
			//console.log(searchparams);

			// post the search parameters to search.php and deal with the
			// result.  if matching items are found, the result will be
			// an array of JSON objects.
			$.post("search.php", {data:searchparams},
					function(data, status) {
				//console.log(data);

				// parse the JSON result so it can be displayed
				var result = $.parseJSON(data);
				//console.log(obj[0].name);
				//console.log(result.length);

				// loop through the array of objects
				for(var i=0; i<result.length; i++) {
					//console.log(result[i].name);

					// now build some HTML to display the result

					// first delete all rows from the table
					for(var j=0; j<table.rows.length; j++) {
						table.deleteRow(j);
					}

					// append a row to the table
					var row = table.insertRow(-1);

					// add a cell to the row for this item's name
					var cell = row.insertCell(0);
					cell.innerHTML = result[i].name;
				}
			});
		}
	})
});
</script>

</head>
<body>
<form>
Name: <input type="text" name="itemname" id="itemname"><br />
</form>

<!-- this table will store the query result -->
<table id="resulttable">
</table>

</body>
</html>
