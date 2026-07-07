<?php


require_once __DIR__ . '/../services/bootstrap.php';

if (rr_access_context() !== 'authenticated') {
	rr_set_flash('warning', 'You’re currently exploring as a guest. Sign in or create an account to unlock personalized forecasts and more!');
	header('Location: login.php');
	exit;
}

require __DIR__ . '/../views/forecast.php';
