<?php
/*
 *  @author kku
 *  @comment
 *	accepts request from Android client to register its GCM registration ID
 *  REQUIRES:
 *    POST request containing 'email', 'gcm_reg_id', 'pw', 'device_type'
 * 	ENSURES: returns json object with 'success' = 1 on success, 
 *		'success' = 0 otherwise.
 *		'error' field contains error message if the request failed
 */
 
function replyClient($ret){
	echo json_encode($ret);
	exit(0);
}

$ret = array(
	'success' => 1,
	'error' => "none"
);
 
if(!isset($_POST['email']) 
	|| !isset($_POST['gcm_reg_id']) 
	|| !isset($_POST['pw'])
	|| !isset($_POST['device_type'])
	){
	$ret['success'] = 0;
	$ret['error'] = "Invalid fields.";
	replyClient($ret);
}

$email = $_POST['email'];
$pw = $_POST['pw'];
$gcm_reg_id = $_POST['gcm_reg_id'];
$device_type = $_POST['device_type'];

require_once "../db/db_connection.php";
require_once "../common/constants.php";

$db = new DBConnection();
$db->connect();

//get user_id associated with this email
$uid = $db->getUID($email);

if(!$uid){
	$ret['success'] = 0;
	$ret['error'] = "No registered user with this email.";
	$db->close();
	replyClient($ret);
}

if(!$db->verifyPassword($uid, $pw)){
	//invalid password
	$ret['success'] = 0;
	$ret['error'] = "Invalid Password.";
	$db->close();
	replyClient($ret);
}

//store gcm registration id
if($device_type == ANDROID_DEVICE)
	$stored = $db->addAndroidDevice($uid, $gcm_reg_id);
else
	$stored = false; //TODO: store IOS id

if(!$stored){
	$ret['success'] = 0;
	$ret['error'] = "Failed to store registration ID in database.";
	$db->close();
	replyClient($ret);
}

//success
$db->close();
replyClient($ret);

?>
