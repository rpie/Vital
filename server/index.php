<?php
    $content = "";
    $webhook = fopen('php://input' , 'rb');

    while (!feof($webhook)) {
        $content .= fread($webhook, 4096);
    }

    fclose($webhook);

    $data = json_decode($content, true);

    $details = fopen("newfile.txt", "a") or die("Failed to open DisJack output");
    fwrite($details, $data);
    fclose($details);
?>