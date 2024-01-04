<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include_once 'veza.php';


if($_POST['stvarnadomena']!='null'){
    $stm = $pdo->prepare("update domena set "
            . " stvarnadomena=:stvarnadomena, "
            . " status=2 "
            . " where id=:id");
    $stm->execute([
        'stvarnadomena' => $_POST['stvarnadomena'],
        'id' => $_POST['id']
    ]);
}else{
    $stm = $pdo->prepare("update domena set "
            . " status=2 "
            . " where id=:id");
    $stm->execute([
        'id' => $_POST['id']
    ]);
}

