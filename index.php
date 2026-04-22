<?php
session_start();

$page = $_GET['page'] ?? 'login';

//Forçar Login
if (!isset($_SESSION['logado']) && $page !== 'login') {
    header("Location: index.php?page=login");
    exit;
}

//Recarregar logado volta pro eventos
if (isset($_SESSION['logado']) && $page === 'login') {
    header("Location: index.php?page=eventos");
    exit;
}

switch ($page) {
    case 'login':
        require_once 'controllers/LoginController.php';
        $controller = new LoginController();
        $controller->validacao();

        require 'views/login.php';
        break;

    case 'eventos':
        require_once 'controllers/EventoController.php';
        $controller = new EventoController();
        $controller->index();
        break;

    case 'logout':
        session_destroy();
        header("Location: index.php?page=login");
        exit;

    default:
        require 'views/404.php';
        break;
}