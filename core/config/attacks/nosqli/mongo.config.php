<?php
	require 'vendor/autoload.php';

	// Configuration
	$dbhost = 'mongo';
	$dbname = 'my_mongodb';
	 
	// Connect to mongo database
	$mongoClient = new MongoDB\Client('mongodb://' . $dbhost);

	// Connect to our database
	$db = $mongoClient->$dbname;

	// Get the flags collection
	$cFlags = $db->flags;

	// Check if document(s) created
	$doc = $cFlags->findOne(['flag' => 'VWGen{m0d_n05ql1_fl46}']);

	if(empty($doc)) {
        // Insert this new document into the flags collection
		$cFlags->insertOne(['flag' => 'VWGen{m0d_n05ql1_fl46}']);
    }
	 
	// Get the users collection
	$cUsers = $db->users;

	// Check if document(s) created
	$doc = $cUsers->findOne(['last_name' => 'Boik']);
	
	if(empty($doc)) {
        // Insert these documents into the users collection
		$cUsers->insertMany([
			['first_name' => 'Su', 'last_name' => 'Boik'],
			['first_name' => 'Ad', 'last_name' => 'Admin']
		]);
    }
?>
