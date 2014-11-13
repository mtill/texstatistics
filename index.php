<?php

$approxWordsPerPage = 335;


if (!isset($_REQUEST['project'])) {
 die('invalid call');
}

$project = preg_replace("/[^a-zA-Z0-9]+/", "", $_REQUEST["project"]);

?>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>texstatistics</title>
</head>
<body>
<h3>Words (1 page: approx. <?php echo $approxWordsPerPage; ?> words):</h3>
<p id="progress"></p>
<p><img src="<?php echo $project; ?>.png"></p>
<p><img src="<?php echo $project; ?>_rel.png"></p>
</body>
</html>

