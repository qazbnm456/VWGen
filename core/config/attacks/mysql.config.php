<?php
    // Configuration
    $dbhost = 'Mysql';
    $dbuser = 'root';
    $dbpass = 'root_password';
    $dbname = 'root_mysql';
    $flag_db = 'flag_db';

    // Connect to mysql database
    $conn = mysql_connect($dbhost, $dbuser, $dbpass) or die('Error with MySQL connection');
    mysql_query("SET NAMES 'utf8'");
    
    mysql_select_db($flag_db);

    // Check if flags table created
    $sql = "SELECT flag from flag_db";
    $result = mysql_query($sql);

    // Create a new flags table if empty
    if(empty($result)) {
        $sql = "CREATE TABLE flags ( id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, flag VARCHAR(30) NOT NULL )";
        mysql_query($sql) or die('MySQL query error');

        // Insert a flag to flags
        $sql = "INSERT INTO flags (flag) VALUES ('VWGen{m0d_5ql1_fl46}')";
        mysql_query($sql) or die('MySQL INSERT query error');
    }

    mysql_select_db($dbname);

    // Check if users table created
    $sql = "SELECT last_name from users";
    $result = mysql_query($sql);

    // Create a new users table if empty
    if(empty($result)) {
        $sql = "CREATE TABLE users ( id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(30) NOT NULL, last_name VARCHAR(30) )";
        mysql_query($sql) or die('MySQL query error');

        // Insert datas to users
        $sql = "INSERT INTO users (first_name, last_name) VALUES ('Su', 'Lobsiinvok')";
        mysql_query($sql) or die('MySQL INSERT query error');

        $sql = "INSERT INTO users (first_name, last_name) VALUES ('Ad', 'Admin')";
        mysql_query($sql) or die('MySQL INSERT query error');
    }
?>
