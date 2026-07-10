<?php

require_once __DIR__ . '/../services/bootstrap.php';

rr_require_feature_access();

$filters = rr_collect_summary_filters();
$summariesResult = rr_fetch_summaries($config, $filters);

require __DIR__ . '/../views/summaries.php';