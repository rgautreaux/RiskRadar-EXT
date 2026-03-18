<?php

require_once __DIR__ . '/../services/bootstrap.php';

http_response_code(500);
$errorTitle = rr_read_query_string('title', 80) ?? 'Something went wrong';
$errorMessage = rr_read_query_string('message', 240) ?? 'The request could not be completed.';

require __DIR__ . '/../views/error.php';
