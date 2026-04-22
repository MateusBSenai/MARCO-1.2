<?php

class Ingresso {
    private $conn;

    public function __construct($db) {
        $this->conn = $db;
    }

    public function comprar($user_email, $evento_id) {
        // Primeiro, buscar o ID do usuário pelo email
        $query_user = "SELECT id FROM users WHERE email = :email";
        $stmt_user = $this->conn->prepare($query_user);
        $stmt_user->bindParam(':email', $user_email);
        $stmt_user->execute();
        $user = $stmt_user->fetch(PDO::FETCH_ASSOC);

        if (!$user) return false;

        $user_id = $user['id'];
        $qr_code_hash = md5($user_id . $evento_id . time());

        $query = "INSERT INTO ingressos (user_id, evento_id, qr_code_hash) VALUES (:user_id, :evento_id, :qr_code_hash)";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':user_id', $user_id);
        $stmt->bindParam(':evento_id', $evento_id);
        $stmt->bindParam(':qr_code_hash', $qr_code_hash);

        return $stmt->execute();
    }

    public function listarPorUsuario($user_email) {
        $query = "SELECT e.*, i.qr_code_hash, i.data_compra 
                  FROM ingressos i 
                  JOIN eventos_db e ON i.evento_id = e.id 
                  JOIN users u ON i.user_id = u.id 
                  WHERE u.email = :email";
        
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':email', $user_email);
        $stmt->execute();
        
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
