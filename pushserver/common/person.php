<?php
class Person {
	private $user_id;
	private $first_name;
	private $last_name;
	private $devices = NULL; //list of devices this person is using
	
	public function __construct($id, $fname, $lname){
		$this->uid = id;
		$this->first_name = $fname;
		$this->last_name = $lname;
	}

  public getUID(){
    return $this->user_id;
  }

  public getFirstName(){
    return $this->first_name;
  }

  public getLastName(){
    return $this->last_name;
  }

  // get all devices
  public getDevices(){
    return $this->devices;
  }

  public getPlatformDevices($platform_id){
    $f = function($d) { return $d->getDeviceType() == $platform_id; };
    return array_map($this->devices, $f);
  }

  public getAndroidDevices(){
    require_once "../common/constants.php";
    return $this->isPlatformDevice(ANDROID_DEVICE);
  }

  public getIOSDevices(){
    require_once "../common/constants.php";
    return $this->isPlatformDevice(IOS_DEVICE);
  }

  public setUID($uid){
    $this->user_id = $uid;
  }

  /*
   *  get this person's devices from database
   *  REQUIRES: set $forceUpdate to true to refresh the user's device list
   *  ENSURES: returns true/false depending on success or not
   */
  public updateDevices($forceUpdate){
    if(!$forceUpdate && $this->devices != NULL)
      return true; //have devices already, no need to update

    if(!$this->user_id)
      return false; //no user_id

    require_once "../db/db_connection.php";
    $db = new DBConnection();
    $db->connect();
    $this->devices = $db->getUserDevices($this->user_id);
    $db->close();

    return !$this->devices;
  }
}
?>
