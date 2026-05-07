<?php

require_once __DIR__ . '/../services/bootstrap.php';

http_response_code(404);
$errorTitle = 'Page not found';
$errorMessage = 'The page you requested does not exist or has moved.';

require __DIR__ . '/../views/error.php';
