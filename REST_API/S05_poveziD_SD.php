<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

set_time_limit(0);

include_once 'veza.php';

$stm = $pdo->prepare("select id, naziv from stvarnadomena");
$stm->execute();
$rezultati = $stm->fetchAll(PDO::FETCH_OBJ);

foreach($rezultati as $r){
    $stm = $pdo->prepare("select id from domena where stvarnadomena=:stvarnadomena");
    $stm->execute(['stvarnadomena'=>$r->naziv]);
    $rez = $stm->fetchAll(PDO::FETCH_OBJ);
    foreach($rez as $rr){
        $stm = $pdo->prepare("insert into domena_stvarnadomena (domena,stvarnadomena) values
                            (:domena,:stvarnadomena)");
    $stm->execute(['domena'=>$rr->id, 'stvarnadomena'=>$r->id]);
    }
}
