<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include_once 'veza.php';


if(isset($_POST['id'])){
    $pdo->beginTransaction();
    $stm = $pdo->prepare("update stvarnadomena set "
            . " analiziranopoveznica=:analiziranopoveznica, "
            . " status=2 "
            . " where id=:id");
    $stm->execute([
        'analiziranopoveznica' => $_POST['analiziranopoveznica'],
        'id' => $_POST['id']
    ]);

    $poddomene =json_decode($_POST['poddomene']);
    foreach ($poddomene as $pd) {
        $stm = $pdo->prepare("insert into poddomena (naziv,domena) values "
            . " (:pd,:id) ");
        $stm->execute([
            'pd' => $pd,
            'id' => $_POST['id']
        ]);
    }
    $pdo->commit();
}