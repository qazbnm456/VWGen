<?php
	// Configuration
	$dbhost = 'Mongodb';
	$dbname = 'my_mongodb';
	 
	// Connect to mongo database
	$mongoClient = new MongoClient('mongodb://' . $dbhost);
	$db = $mongoClient->$dbname;
	 
	// Get the users collection
	$cUsers = $db->users;
	 
	// Insert first object
	$user = array(
	    'first_name' => 'Su',
	    'last_name' => 'Lobsiinvok',
	    'roles' => array('developer','bugmaker')
	);
	 
	// Insert this new document into the users collection
	$cUsers->save($user);

	// Insert second object
	$user = array(
	    'first_name' => 'Ad',
	    'last_name' => 'Admin',
	    'roles' => array('administrator', 'developer')
	);
	 
	// Insert this new document into the users collection
	$cUsers->save($user);
?>