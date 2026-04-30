<?php
// Backend endpoint to mark onboarding as complete for the current user (PHP)
session_start();
require_once __DIR__ . '/../../services/api_client.php';

if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    exit('Not logged in');
}

$userId = $_SESSION['user_id'];

try {
    // Call backend API to mark onboarding complete
    $api = new ApiClient();
    $api->post("/users/$userId/onboarding", [ 'completed' => true ]);
    echo 'ok';
} catch (Exception $e) {
    http_response_code(500);
    echo 'error';
}
