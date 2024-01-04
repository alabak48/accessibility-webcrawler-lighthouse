<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include_once 'veza.php';

$uuid = file_get_contents('/proc/sys/kernel/random/uuid');
$uuid = substr($uuid, 0, -1);
//echo "\n" . strlen($uuid) . "\n";
//odi po prvi slobodan

$stm = $pdo->prepare("update domena set "
        . " datumpocetka=now(), "
        . " uuid=:uuid, "
        . " status=1 "
        . " where status=0 and uuid is null limit 1");
$stm->execute([
    'uuid' => $uuid
]);

$stm = $pdo->prepare("select id, naziv from domena where uuid=:uuid and status=1");
$stm->execute(['uuid' => $uuid]);


$domene = $stm->fetchAll(PDO::FETCH_ASSOC);

echo json_encode($domene);