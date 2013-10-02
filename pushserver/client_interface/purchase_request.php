<?php
/*
 *  @author kku
 *  @comment
 *	accepts request from Android client to push notification of a new purchase
 *		to others
 *  REQUIRES:
 *    POST request with 'email', 'pw', 'room_id', 'item_name', 'item_price'
 * 	ENSURES: returns json object with 'success' = 1 on success, 
 *		'success' = 0 otherwise.
 *		'error' field contains error message if the request failed
 */

require_once ("../debug/global_debug.php");
 
function replyClient($ret){
	echo json_encode($ret);
	exit(0);
}

$ret = array(
	'success' => 1,
	'error' => "none"
);
 
if(!isset($_POST['email']) 
	|| !isset($_POST['pw'])
	|| !isset($_POST['room_id'])
  || !isset($_POST['item_name'])
  || !isset($_POST['item_price'])
){
	$ret['success'] = 0;
	$ret['error'] = "Invalid fields.";
	replyClient($ret);
}

$email = $_POST['email'];
$pw = $_POST['pw'];
$room_id = $_POST['room_id'];

require_once "../db/db_connection.php";

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

//check password
if(!$db->verifyPassword($uid, $pw)){
	//invalid password
	$ret['success'] = 0;
	$ret['error'] = "Invalid Password.";
	$db->close();
	replyClient($ret);
}

//get roommates
$roommates = $db->findRoommates($uid, $room_id);
if(!$roommates){
	$ret['success'] = 0;
	$ret['error'] = "No Roommates.";
	$db->close();
	replyClient($ret);
}

$db->close();

//send push notification
require_once "../gcm_server/gcm_handler.php";

$data = array (
  'item_name' => $_POST['item_name'],
  'item_price' => $_POST['item_price']
);

//send push through GCM
$gcm = new GCMHandler();
if(!$gcm->sendPurchaseRequest($uid, $roommates, $data)){
  //gcm failed to send message
  $ret['success'] = 0;
  $ret['error'] = "GCM failed.";
  replyClient($ret);
}

//TODO: send push for IOS

replyClient($ret);

?>
