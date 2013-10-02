<?php
/*
 *  @author kku
 *  @comment common database library class for push message server
 */
class DBConnection {
	private $db = NULL;

	function __construct() {
	}
	
	function __destruct() {
		$this->close();
	}
	
	public function connect(){
		require_once './db_config.php';
		
		$this->db = new mysqli(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
		if ($this->db->connect_errno) {
			echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " 
        . $mysqli->connect_error;
			$this->db = NULL;
			return false;
		}
		
		return true;
	}
	
	private function prepareStatement($query){
		$stmt = $this->db->prepare($query);		
		if(!$stmt)
			return NULL;	
		return $stmt;
	}
	
	private function hashPassword($password) {
		//TODO: implement hash
		return $password;
	}
	
	/*
	 * ENSURES: returns NULL if addUser failed, user_id if successful 
	 */
	public function addUser($firstName, $lastName, $pw, $email) {
		$pw = hashPassword($pw);
	
		$query = "INSERT INTO user(
			user_first_name, 
			user_last_name, 
			user_password, 
			user_email, 
			user_join_time) 
			VALUES(?, ?, ?, ?, NOW());
		";
			
		$stmt = prepareStatement($query);
		$bind = $stmt->bind_param("ssss", $firstName, $lastName, $pw, $email);
		if(!$bind)
			return NULL;
		
		$exec = $stmt->execute();
		if(!$exec)
			return NULL;
			
		return $stmt->insert_id;
	}
	
	/*
	 *	ENSURES: returns user_id of the user with the corresponding email,
	 *		NULL if not match was found
	 */
	public function getUID($email){
		$query = "SELECT user_id FROM user WHERE user_email = ?";
		
		$stmt = prepareStatement($query);
		$bind = $stmt->bind_param("s", $email);
		if(!$bind)
			return NULL;
		
		$exec = $stmt->execute();
		if(!$exec)
			return NULL;
			
		$stmt->store_result();
			
		if($stmt->num_rows == 0)
			return NULL
			
		$stmt->bind_result($uid);
		$stmt->fetch();
		
		return $uid;
	}
	
	/*
	 *	ENSURES: returns true if the password is correct, false otherwise
	 */
	public function verifyPassword($uid, $pw){
		$query = "SELECT user_password FROM user WHERE user_id = ?";
		
		$stmt = prepareStatement($query);
		$bind = $stmt->bind_param("i", $uid);
		if(!$bind)
			return false;
		
		$exec = $stmt->execute();
		if(!$exec)
			return false;
			
		$stmt->store_result();
			
		if($stmt->num_rows == 0)
			return false;
			
		$stmt->bind_result($stored_pw);
		$stmt->fetch();
		
		$pw = hashPassword($pw);
		
		return (strcmp($pw, $stored_pw) == 0);
	}
	
	/*
	 * 	hash GCM Registration ID with SHA256 to use as key in checking 
	 *		duplicate devices
	 */
	private function hashGCMRegID($id){
		return hash("sha256", $id);
	}
	
	/*
	 * ENSURES: returns NULL if addAndroidDevice failed, device_id if successful 
	 */
	public function addAndroidDevice($uid, $gcm_reg_id){
		$gcm_reg_id_hash = hashGCMRegID($gcm_reg_id);
		
		$query = "INSERT INTO android_device(
			user_id, 
			gcm_reg_id,
			gcm_reg_id_hash)
			VALUES(?, ?, ?)
			ON DUPLICATE KEY UPDATE gcm_reg_id = ?;
			";
		
		$stmt = prepareStatement($query);
		$bind = $stmt->bind_param("isss", $uid, $gcm_reg_id, $gcm_reg_id_hash, 
      $gcm_reg_id);
		if(!$bind)
			return NULL;
		
		$exec = $stmt->execute();
		if(!$exec)
			return NULL;
			
		return $stmt->insert_id;
	}
		
	/*
	 * ENSURES: returns a list of Person object who are roommates 
	 *		of $uid living the room $room_id
	 */
	public function findRoommates($uid, $room_id){
		$query = 
      "SELECT user_id FROM room_member WHERE room_id = ? AND user_id <> ?";

		$stmt = prepareStatement($query);
		$bind = $stmt->bind_param("ii", $room_id, $uid);
		if(!$bind)
			return NULL;
		
		$exec = $stmt->execute();
		if(!$exec)
			return NULL;
			
		$stmt->store_result();
			
		if($stmt->num_rows == 0)
			return NULL;
			
		$result = $stmt->fetch_all();
		$roommates = array();
		
    require_once "../common/person.php";

		$index = 0;
		foreach($result as $r){	
			if($uid == $r['user_id']){
				//don't include a person as his own roommate
				continue;
			}
				
			$mate = new Person();
			$mate.setUID($r['user_id']);
			$roommates[$index] = $mate;
			$index++;
		}
		
		return $roommates;		
	}
	
	/*
	 *	get a list of registered devices of a user
	 *	ENSURES: returns a list of ClientDevice that belong to the user,
   *    return NULL on failure
	 */
	public function getDevices($uid){
    require_once "../common/constants.php";
    require_once "../common/client_device.php";

    //get android devices
		$query = "SELECT 
      device_id, gcm_reg_id 
      FROM android_device 
      WHERE user_id = ?";

		$stmt = prepareStatement($query);
		$bind = $stmt->bind_param("i", $uid);
		if(!$bind)
			return NULL;
		
		$exec = $stmt->execute();
		if(!$exec)
			return NULL;
			
		$stmt->store_result();
			
		$result = $stmt->fetch_all();
		$android = array();
		
		$index = 0;
		foreach($result as $r){	
      $info = array (
        'gcm_reg_id' = $r['gcm_reg_id'],
        'device_id' = $r['device_id']
      );

      $android[$index] = new ClientDevice(ANDROID_DEVICE, $uid, $info);
			$index++;
		}
		
		return $android;
	}
	
	public function close() {
		if ($this->db != NULL)
			$this->db->close();
	}
}
?>
