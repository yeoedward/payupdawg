<?php
/* 
 * @author kku
 * @comment 
 *  server database initialization script for messaging server
 */
?>
<?php
include("sql.php");
?>
<html>
<head>
</head>
<body>
<?php	
	if(isset($_POST['id']) && isset($_POST['pw'])){
		dbInit();
		echo("Server initialization complete!");
	}
	else{
		echo "
			Please enter MySQL root credentials: <br/>
			<form method='POST' action='init.php'>
				Root username: <input type='text' name='id' size='30'><br/><br/>
				Root password: <input type='password' name='pw' size='30'><br/>
				<input type='submit' name='upload' value='Login to Initialize'>
			</form>
		";
	}
	
	function dbInit(){
		require_once("../db/db_config.php");
	
		$db_name = DB_NAME;
		$db_host = DB_HOST;
		
		//create database 
		$link = mysql_connect($db_host, "".$_POST['id'], "".$_POST['pw']);
		$query = "CREATE DATABASE IF NOT EXISTS {$db_name} CHARACTER SET utf8 COLLATE utf8_general_ci";
		$result = mysql_query($query , $link);
		if($result == ""){
			basic_redirect("Unable to create database. Please try again.", "init.php");
		}
		
		//create database user account
		try{
			$db = sql_connect_db($db_host, "".$_POST['id'], "".$_POST['pw'], "{$db_name}");
		}catch(Exception $e){
			basic_redirect("Unable to connect to database {$db_name}. Please try again", "init.php");
		}
		
		$admin_account = DB_USER;
		$admin_pw = DB_PASSWORD;
		
		$query = "CREATE USER '{$admin_account}'@'{$db_host}' IDENTIFIED BY  '{$admin_pw}'";
		if(!$db->query($query)){
			echo $db->error;
			basic_redirect("Unable to create {$admin_account} database account. Please try again.", "init.php");
		}
		
		$query = "GRANT ALL ON {$db_name}.* TO '{$admin_account}'@'{$db_host}' IDENTIFIED BY  '{$admin_pw}' 
			WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0";
		if(!$db->query($query)){
			echo $db->error;
			basic_redirect("Unable to grant {$admin_account} database privilege. Please try again.", "init.php");
		}	
		
		$query = "GRANT FILE ON * . * TO  '{$admin_account}'@'{$db_host}'";
		if(!$db->query($query)){
			echo $db->error;
			basic_redirect("Unable to grant {$admin_account} FILE privilege. Please try again.", "init.php");
		}
		
		//create tables
		//user table
		$query = "CREATE TABLE IF NOT EXISTS user(
			user_id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
			user_first_name VARCHAR(255) NOT NULL, 
			user_last_name VARCHAR(255) NOT NULL, 
			user_password VARCHAR(255) NOT NULL, 
			user_email VARCHAR(255) NOT NULL,
			user_join_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (user_id)
			)";
		if(!$db->query($query)){
			echo $db->error;
			basic_redirect("Unable to create table user. Please try again.", "init.php");
		}
		
		//room table
		$query = "CREATE TABLE IF NOT EXISTS room(
			room_id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT, 
			room_name VARCHAR(255) NOT NULL, 
			room_active TINYINT UNSIGNED NOT NULL DEFAULT 1,
			room_create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (room_id)
		)";
		if(!$db->query($query)){
			echo $db->error;
			basic_redirect("Unable to create room table. Please try again.", "init.php");
		}
		
		//room_member table
		//records members of a group
		$query = "CREATE TABLE IF NOT EXISTS room_member(
			room_id INT(11) UNSIGNED NOT NULL,
			user_id INT(11) UNSIGNED NOT NULL,
			room_member_type TINYINT UNSIGNED NOT NULL,
			PRIMARY KEY (room_id, user_id)
		)";
		if(!$db->query($query)){
			echo $db->error;
			basic_redirect("Unable to create room_member table. Please try again.", "init.php");
		}
		
		//android device id table (reg id of user's devices)
		//gcm_reg_id_hash = sha256(gcm_reg_id) (used to ensure no duplicate device is added)
		$query = "CREATE TABLE IF NOT EXISTS android_device(
			device_id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT, 
			user_id INT(11) NOT NULL, 
			gcm_reg_id TEXT NOT NULL,
			gcm_reg_id_hash VARCHAR(64) NOT NULL,
			PRIMARY KEY (device_id),
			UNIQUE (gcm_reg_id_hash)
		)";
		if(!$db->query($query)){
			echo $db->error;
			basic_redirect("Unable to create android_device table. Please try again.", "init.php");
		}
		
		sql_close($db);
	}
	
	function basic_redirect($msg, $target){
		echo "<script>";
		if(isset($msg))
			echo "alert('{$msg}');";				
		if(isset($target))
			echo "location.replace('{$target}');";
		echo"</script>";
		exit(0);
	}
	
	function encrypt_password($salt, $pw){
		return sha1($salt.$pw);
	}
?>
</body>
</html>
