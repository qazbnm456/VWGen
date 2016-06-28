<?php
	// Configuration
	$dbhost = 'Mongo';
	$dbname = 'my_mongodb';
	 
	// Connect to mongo database
	$mongoClient = new MongoClient('mongodb://' . $dbhost);

	// Connect to our database
	$db = $mongoClient->$dbname;

	// Get the flags collection
	$cFlags = $db->flags;

	// Check if document(s) created
	$doc = $cFlags->findOne(array('flag' => 'VWGen{m0d_n05ql1_fl46}'));

	if(empty($doc)) {
        // Insert first object
		$flag = array(
		    'flag' => 'VWGen{m0d_n05ql1_fl46}'
		);
		 
		// Insert this new document into the users collection
		$cFlags->save($flag);
    }
	 
	// Get the users collection
	$cUsers = $db->users;

	// Check if document(s) created
	$doc = $cUsers->findOne(array('last_name' => 'Boik'));
	
	if(empty($doc)) {
        // Insert first object
		$user = array(
		    'first_name' => 'Su',
		    'last_name' => 'Boik'
		);
		 
		// Insert this new document into the users collection
		$cUsers->save($user);

		// Insert second object
		$user = array(
		    'first_name' => 'Ad',
		    'last_name' => 'Admin'
		);
		 
		// Insert this new document into the users collection
		$cUsers->save($user);
    }
?>
