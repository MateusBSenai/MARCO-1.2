<?php
class Usuario {
    private $conn;

    public function __construct($db) {
        $this->conn = $db; // Recebe a conexão
    }

    public function verificarSenha($user){
        $query = "SELECT hash_senha FROM users WHERE email = :usuario";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':usuario', $user);
        $stmt->execute();

        $resultado = $stmt->fetch(PDO::FETCH_ASSOC);

        return $resultado['hash_senha'] ?? false;
    }
    public function criar($nome, $email, $senha) {
        $hashSenha = password_hash($senha, PASSWORD_DEFAULT);

        $query = "INSERT INTO users (nome, email, hash_senha) VALUES (:nome, :email, :hash_senha)";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':nome', $nome);
        $stmt->bindParam(':email', $email);
        $stmt->bindParam(':hash_senha', $hashSenha);

        return $stmt->execute();
    }

    public function lerTodos(){
        $query = "SELECT id, nome, email, hash_senha, admin FROM users";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
    public function buscarPorId($id) {
        $query = "SELECT nome, email, hash_senha, admin FROM users WHERE id = :id";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':id', $id);
        $stmt->execute();
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }

    public function buscarPorEmail($email) {
        $query = "SELECT id, nome, email, hash_senha, admin FROM users WHERE email = :email";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':email', $email);
        $stmt->execute();
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }
}