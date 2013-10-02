<?php
class GCMHandler{
	public function __construct(){
	}
	
	public function __destruct(){
	}
	
	/*	send push notification
	 * 	REQUIRES: $reg_ids are registration ids of Android devices 
	 *		registered with GCM. 
	 *		$data is an array containing any data that needs to be passed 
	 *		along, but cannot exceed 4kb
	 *	ENSURES: returns json with 'success' = 1 indicating successful send,
	 *		'success' = 0 indicating failed. 
	 *		'error_message' contains any error message
	 */
	private function sendNotification($reg_ids, $data){
		require_once "./gcm_config.php";
		
		$ret = array(
			'success' => 1,
			'error_message' => "none"
		);

    if (sizeof($reg_ids) == 0){
      $ret['success'] = 0;
      $ret['error_message'] = "no registration id given";
      return json_encode($ret);
    }

    //set POST variables
    $url = 'https://android.googleapis.com/gcm/send';

    $fields = array(
        'registration_ids' => $reg_ids,
        'data' => $data,
    );

    $headers = array(
        'Authorization: key='.GOOGLE_API_KEY,
        'Content-Type: application/json'
    );

    $con = curl_init();

    //set url
    curl_setopt($con, CURLOPT_URL, $url);
 
		//set POST
    curl_setopt($con, CURLOPT_POST, true);
    curl_setopt($con, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($con, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($con, CURLOPT_POSTFIELDS, json_encode($fields));

    //POST to GCM
    $result = curl_exec($con);
		
    if (!$result){
			//error occurred
			$ret['success'] = 0;
			$ret['error_message'] = curl_error($con);
    }
 
    //close connection
    curl_close($con);
        
		//output success as json
		return json_encode($ret);
	}
	
	/*
	 *	send a purchase request to roommates
	 *	REQUIRES: $uid is the user_id of the person requesting the purchase,
	 *		$data contains data about the purchase as a string-indexed array,
   *    $roommates is an array of person objects representing the roommates 
   *    that this request is targeted to
	 *	ENSURES: returns json with 'success' = 1 indicating successful send,
	 *		'success' = 0 indicating failed. 
	 *		'error_message' contains any error message
	 */
	public function sendPurchaseRequest($uid, $roommates, $data){
    //get roommate android devices
    $getDevice = function($r) { 
      $r->updateDevices(true); 
      return $r->getAndroidDevices(); 
    };
    $android = array_map ($getDevice, $roommates);

    //get all gcm_reg_id
    $gcm_reg_id = array();
    $index = 0;
    for($i = 0; $i < sizeof($android); $i++){
      $getGCMID = function($a) { 
        $info = $a->getDeviceInfo(); 
        return $info['gcm_reg_id']; };

      $gcm_reg_id = array_merge($gcm_reg_id, 
        array_map($getGCMID, $android[i]));
    }

    //send notification
    return $this->sentNotification ($gcm_reg_id, $data);
	}
}
?>
