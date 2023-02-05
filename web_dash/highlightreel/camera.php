<?php

    $command = "libcamera-still -o /home/pi/HighlightReel/src/web_dash/res/capture.jpg --width 4624 --height 3472 --autofocus";
    exec($command, $output);

    $file = '/home/pi/HighlightReel/src/web_dash/res/capture.jpg';
    $type = 'image/jpeg';
    header('Content-Type:'.$type);
    header('Content-Length: ' . filesize($file));
    readfile($file)

?>