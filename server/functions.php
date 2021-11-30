<?php
    
    /*
    *   Contains functions used in Vital server
    *   controller.
    */

    function randomString($input, $len = 16) {
        $string_ = '';

        for($i = 0; $i < $len; $i++) {
            $random_character = $input[mt_rand(0, $strlen($input) - 1)];
            $string_ .= $random_character;
        }

        return $string_;
    }

?>
