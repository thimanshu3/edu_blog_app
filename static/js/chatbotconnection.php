<?php
session_start();

  if(isset($_POST['message'])){

  $workspace_id = '19d2dd6f-d510-4229-a338-704e3247788f';
  $release_date = '2018-07-10';
  $username = '459a58fb-1f1c-4299-b6ef-c0007fcad29d';
  $password = 'ybIAJLeUxqwW';
   
    $input['input']['text'] = $_POST['message'];
    if(isset($_SESSION['prev_context'])){
      $input['context'] = json_decode($_SESSION['prev_context'], JSON_UNESCAPED_UNICODE); 
    }
    $input['alternate_intents'] = false;

    // Encode json
    $json = json_encode($input, JSON_UNESCAPED_UNICODE);

    // Post the json
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_URL, 'https://gateway.watsonplatform.net/assistant/api/v1/workspaces/'.$workspace_id.'/message?version='.$release_date); 
    curl_setopt($ch, CURLOPT_USERPWD, $username.":".$password); 
    curl_setopt($ch, CURLOPT_POST, true );
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json')); 
    curl_setopt($ch, CURLOPT_POSTFIELDS, $json);
    $result = trim(curl_exec($ch)); 
    curl_close($ch); 

  $result=json_decode($result,true);
  $_SESSION['prev_context'] = json_encode($result['context']);
  //echo $user_context;
  $result = json_encode($result);
  echo $result;

  }
  else
  {
    echo '{"status":"error","msg":"unauthorised access"}';
  }

?>
