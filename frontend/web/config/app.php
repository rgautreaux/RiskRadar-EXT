<?php

$defaultConfig = [
    'app' => [
        'name' => 'RiskRadar Web',
        'base_path' => '/'
    ],
    'api' => [
        'base_url' => getenv('RISKRADAR_API_BASE_URL') ?: 'http://127.0.0.1:8000',
        'prefix' => getenv('RISKRADAR_API_PREFIX') ?: '/api/v1',
        'timeout' => (float) (getenv('RISKRADAR_API_TIMEOUT') ?: 5.0),
    ],
];

$localConfigPath = __DIR__ . '/config.local.php';
if (file_exists($localConfigPath)) {
    $localConfig = require $localConfigPath;
    if (is_array($localConfig)) {
        $defaultConfig = array_replace_recursive($defaultConfig, $localConfig);
    }
}

return $defaultConfig;