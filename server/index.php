<?php
    require __DIR__ . '/functions.php';
    /* 
    *   Server code for Vital (PHP)
    *   ===========================
    *   Collects the data sent from
    *   client file (main.py)
    *
    */
    
    $content    =   "";
    $webhook    =   fopen('php://input' , 'rb');
    $random     =   randomString('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 7);

    while (!feof($webhook)) {
        $content .= fread($webhook, 4096);
    }

    fclose($webhook);

    $data = json_decode($content, true);
    
    $fhandle = fopen("REPORT-{$random}", "w") or die("Could not create a new output file.");

    fwrite($fhandle, $data);
    fclose($fhandle);

?>
