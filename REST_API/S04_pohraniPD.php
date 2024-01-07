<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include_once 'veza.php';


if(isset($_POST['id'])){
    $pdo->beginTransaction();
    $stm = $pdo->prepare("update stvarnadomena set "
            . " datumkraja=now(), "
            . " status=2, "
            . " sekundi=:sekundi,"
            . " racunalo=:racunalo"
            . " where id=:id");
    $stm->execute([
        'id' => $_POST['id'],
        'sekundi'=>$_POST['sekundi'],
        'racunalo'=>$_POST['racunalo']
    ]);

    $lista =json_decode($_POST['poddomene']);
    foreach ($lista as $stavka) {
        $stm = $pdo->prepare("insert into poddomena (domena,naziv) values "
            . " (:domena,:naziv) ");
        $stm->execute([
            'domena' => $_POST['id'],
            'naziv' => $stavka
        ]);
    }

    $lista =json_decode($_POST['poveznice']);
    foreach ($lista as $stavka) {
        $stm = $pdo->prepare("insert into poveznica (domena,url,dugiurl) values "
            . " (:domena,:url,:dugiurl) ");
        if(strlen($stavka)>254){
            $stm->execute([
                'domena' => $_POST['id'],
                'url' => substr($pd,0,254),
                'dugiurl'=>$stavka

            ]);
        }
        else{
            $stm->execute([
                'domena' => $_POST['id'],
                'url' =>$stavka,
                'dugiurl'=>null,
            ]);
        }
    }


    $lista =json_decode($_POST['domene']);
    foreach ($lista as $stavka) {
        $stm = $pdo->prepare("insert into svedomene (domena,url) values "
            . " (:domena,:url); ");
            $stm->execute([
                'domena' => $_POST['id'],
                'url' => $stavka

            ]);
    }


    $pdo->commit();
}