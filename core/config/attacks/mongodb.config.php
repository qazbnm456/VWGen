<?php
	// Configuration
	$dbhost = 'Mongodb';
	$dbname = 'my_mongodb';
	 
	// Connect to mongo database
	$mongoClient = new MongoClient('mongodb://' . $dbhost);
	$db = $mongoClient->$dbname;
	 
	// Get the users collection
	$cUsers = $db->users;
	 
	// Insert object
	$user = array(
	    'first_name' => 'Su',
	    'last_name' => 'Lobsiinvok',
	    'roles' => array('developer','bugmaker')
	);
	 
	// Insert this new document into the users collection
	$cUsers->save($user);
?>