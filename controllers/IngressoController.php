<?php

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../models/Ingresso.php';

class IngressoController {
    public function comprar($email, $evento_id) {
        $database = new Database();
        $db = $database->getConnection();
        $ingressoModel = new Ingresso($db);

        if ($ingressoModel->comprar($email, $evento_id)) {
            return [
                "status" => "sucesso",
                "mensagem" => "Ingresso adquirido com sucesso"
            ];
        }
        return [
            "status" => "erro",
            "mensagem" => "Falha ao adquirir ingresso"
        ];
    }

    public function getMeusIngressos($email) {
        $database = new Database();
        $db = $database->getConnection();
        $ingressoModel = new Ingresso($db);

        $ingressos = $ingressoModel->listarPorUsuario($email);
        return $ingressos;
    }
}
