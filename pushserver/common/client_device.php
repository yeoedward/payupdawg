<?php
require_once "./constants.php";

//generic client device
class ClientDevice {
	private final int $device_type;
	private final int $uid;
  private final $device_info;
	
	public function __construct($type, $id, $info){
		$this->device_type = $type;
		$this->uid = $uid;
    $this->device_info = $info;
	}

  public getDeviceType(){
    return $this->device_type;
  }

  public getUID(){
    return $this->uid;
  }

  public getDeviceInfo(){
    return $this->device_info;
  }
}
?>
