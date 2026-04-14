<?php

require_once __DIR__ . '/../services/bootstrap.php';


rr_require_feature_access();
$isGuest = rr_is_guest_mode();

require __DIR__ . '/../views/forecast.php';
