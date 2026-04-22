<?php

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../models/Usuario.php';

class LoginController {
    public function validacao() {
        $database = new Database();
        $db = $database->getConnection();
        $usuarioModel = new Usuario($db);
    
        if ($_SERVER['REQUEST_METHOD'] == "POST" && isset($_POST['entrar'])){
            $senha = $_POST['senha'];
            $userRecord = $usuarioModel->buscarPorEmail($_POST['email']);

            if ($userRecord && password_verify($senha, $userRecord['hash_senha'])){
                $_SESSION['logado'] = true;
                $_SESSION['email'] = $userRecord['email'];
                $_SESSION['nome'] = $userRecord['nome'];
                header("Location: index.php?page=eventos");
                exit;
            } else {
                $_SESSION["erro_login"] = "Senha ou usuário incorretos, tente novamente!";
                header("Location: index.php?page=login");
                exit;
            }
        }
    }

    public function loginApi($email, $senha) {
        $database = new Database();
        $db = $database->getConnection();
        $usuarioModel = new Usuario($db);

        $userRecord = $usuarioModel->buscarPorEmail($email);
        if ($userRecord && password_verify($senha, $userRecord['hash_senha'])) {
            return [
                "status" => "sucesso",
                "mensagem" => "Login bem-sucedido",
                "nome" => $userRecord['nome']
            ];
        }
        return [
            "status" => "erro",
            "mensagem" => "Email ou senha incorretos"
        ];
    }

    public function registrarApi($nome, $email, $senha) {
        $database = new Database();
        $db = $database->getConnection();
        $usuarioModel = new Usuario($db);

        if ($usuarioModel->criar($nome, $email, $senha)) {
            return [
                "status" => "sucesso",
                "mensagem" => "Usuário criado com sucesso"
            ];
        }
        return [
            "status" => "erro",
            "mensagem" => "Falha ao criar usuário"
        ];
    }

    public function getPerfil($email) {
        $database = new Database();
        $db = $database->getConnection();
        $usuarioModel = new Usuario($db);

        $user = $usuarioModel->buscarPorEmail($email);
        if ($user) {
            unset($user['hash_senha']); // Segurança
            return [
                "status" => "sucesso",
                "dados" => $user
            ];
        }
        return [
            "status" => "erro",
            "mensagem" => "Usuário não encontrado"
        ];
    }
}