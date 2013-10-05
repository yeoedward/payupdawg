<?php
/*
 *  @author kku
 *  @comment database utility functions for server set up 
 */
?>
<?php
	/*	sql_connect_db
		ENSURES:
			returns a mysqli object if successfully connected. NULL otherwise
	*/	
	function sql_connect_db($host, $username, $password, $db_name){
		$mysqli = new mysqli($host, $username, $password, $db_name);
		if ($mysqli->connect_errno) {
			echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
			throw new Exception("SQL: Unable to connect to databse.");
		}
		return $mysqli;
	}
	
	function sql_close($db){
		mysqli_close($db);
	}
	
	function sql_prepare_stmt($db, $query){
		if (!($stmt = $db->prepare($query))) {
			echo "Prepare failed: (" . $db->errno . ") " . $db->error;
			throw new Exception("SQL: Unable to prepare statement.");
		}
		return $stmt;
	}
	
	// $store = true if want to store result in stmt
	function sql_execute_stmt($stmt, $store){
		if (!$stmt->execute()) {
			echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
			return new Exception("SQL: Unable to execute statement");
		}
		if($store)
			$stmt->store_result();
		return $stmt;
	}
	
	function sql_fetch_row($stmt){
		return $stmt->fetch();
	}

	function sql_exec_prepared_query($query, $bind_types, $bind_args, $store){
		$db = NULL;
		$stmt = NULL;
		try{
			$info = sql_get_default_values();
			$db = sql_connect_db($info['db_host'], $info['db_user'], $info['db_pw'], $info['db_name']);
			
			$stmt = sql_prepare_stmt($db, $query);
			
			$tmp = call_user_func_array("mysqli_stmt_bind_param", array_merge(array($stmt, $bind_types), create_ref_array($bind_args)));
			if(!$tmp)
				throw new Exception("SQL: Unable to bind param");
			
			$stmt = sql_execute_stmt($stmt, $store);
			sql_close($db);
			
			return $stmt; 
		}catch(Exception $e){
			//echo $e->getMessage();
			return NULL;
		}
	}
	
	function sql_prepared_stmt_get_result($stmt){
		$meta = $stmt->result_metadata(); 

		while ($field = $meta->fetch_field()) { 
			$params[] = &$row[$field->name]; 
		} 

		$ret = array();
		call_user_func_array(array($stmt, 'bind_result'), $params);    		
		while ($stmt->fetch()) { 
			foreach($row as $key => $val) { 
				$c[$key] = $val; 
			} 
			$ret[] = $c; 
		} 		
		return $ret;
	}
?>
