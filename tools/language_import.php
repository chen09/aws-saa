<?php
require_once __DIR__ . '/vendor/autoload.php';

$db = new MysqliDb (Array (
    'host' => '192.168.99.100',
    'username' => 'root',
    'password' => 'root1234',
    'db'=> 'aws_saa',
    'port' => 32781,
    'charset' => 'utf8'));

$answers = $db->get('answer');
var_dump($answers);

$file = __DIR__ ."/../languages.json";
$json = file_get_contents($file);

$languages = json_decode($json, true);
$languages = $languages['languages'];
foreach  ($languages as $language){
    $languageCode = $language['languageCode'];
    $supportSource = $language['supportSource'];
    $supportTarget = $language['supportTarget'];
    $data = [];
    $data['code'] = $language['languageCode'];
    $data['source'] = $language['supportSource'];
    $data['target'] = $language['supportTarget'];

    $id = $db->insert ('language', $data);

    if ($id)
        echo 'language was created. Id=' . $id."\n";
    else
        echo 'insert failed: ' . $db->getLastError()."\n";
}
//
//supportTargetsupportTarget$data = Array ("login" => "admin",
//    "firstName" => "John",
//    "lastName" => 'Doe'
//);
//$id = $db->insert ('users', $data);