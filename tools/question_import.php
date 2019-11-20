<?php
require_once __DIR__ . '/vendor/autoload.php';

$options = getopt("l:");

if (!isset($options['l'])) {
    echo "usage: -l language is needed.\n";
    exit();
}

$language = $options['l'];
$FILENAME = "AWS-SAA-C01.${language}.csv";

$handle = fopen(__DIR__ . "/" . $FILENAME, "r");
if ($handle == FALSE) {
    echo __DIR__ . "/" . $FILENAME . " open failed. \n";
    exit();
}


$db = new MysqliDb (Array(
    'host' => '192.168.99.100',
    'username' => 'root',
    'password' => 'root1234',
    'db' => 'aws_saa',
    'port' => 18801,
    'charset' => 'utf8'));

$db->where('code', $language);
$language_id = $db->getOne('language')['id'];

while (($data = fgetcsv($handle)) !== FALSE) {
    $question_id = $data[0];
    $question = $data[1];
    $choices = [];
    for ($i = 2; $i < 12; $i++) {
        if (!isset($data[$i]) || strlen($data[$i]) == 0) {
            break;
        }
        $choices[$i - 2] = $data[$i];
    }
    $answer = $data[12];
    $remarks = $data[14];

    $row = [];
    $row['question_id'] = $question_id;
    $row['language_id'] = $language_id;
    $row['question'] = trim($question);
    $row['remarks'] = $remarks;
    $id = $db->insert('question', $row);
//    var_dump($row);

    for ($i = 0; $i < count($choices); $i++) {
        $row = [];
        $row['question_id'] = $question_id;
        $row['language_id'] = $language_id;
        $row['choice_id'] = $i;
        $row['choice'] = trim($choices[$i]);
//        var_dump($row);
        $id = $db->insert('choice', $row);
    }


    $answers = str_split($answer);
    foreach ($answers as $answer) {
        $answer_id = ord($answer) - ord('A');
        $row = [];
        $row['question_id'] = $question_id;
        $row['choice_id'] = $answer_id;
        $id = $db->insert('answer', $row);
    }

}
fclose($handle);



