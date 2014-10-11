<!doctype HTML>
<html>
<head>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

<script>
$(document).ready(function() {
	$('#itemname').keyup(function() {
		var searchparams = $("form").serialize();
		//console.log(searchparams);
		$.post("search.php", {data:searchparams}, function(data, status) {
			console.log(data);
			// do things?
		});
	})
});
</script>

</head>
<body>
<form>
Name: <input type="text" name="itemname" id="itemname"><br />
</form>


</body>
</html>
