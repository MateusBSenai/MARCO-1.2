<?php

class Evento {
    private $conn;

    public function __construct($db) {
        $this->conn = $db; // Recebe a conexão
    }

    public function lerTodos(){
        $query = "SELECT * FROM eventos_db";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    public function criar($titulo, $foto, $tipo, $data_evento, $hora_evento, $local_evento, $valor_evento) {
        $query = "INSERT INTO eventos_db
                (titulo, foto_evento, tipo_imagem, data_evento, hora_evento, local_evento, valor_evento)
                VALUES (?, ?, ?, ?, ?, ?, ?)";

        $stmt = $this->conn->prepare($query);

        $stmt->bindParam(1, $titulo);
        $stmt->bindParam(2, $foto, PDO::PARAM_LOB);
        $stmt->bindParam(3, $tipo);
        $stmt->bindParam(4, $data_evento);
        $stmt->bindParam(5, $hora_evento);
        $stmt->bindParam(6, $local_evento);
        $stmt->bindParam(7, $valor_evento);

        return $stmt->execute();
    }
    public function criarSimg($titulo, $data_evento, $hora_evento, $local_evento, $valor_evento) {
        $query = "INSERT INTO eventos_db
                (titulo, data_evento, hora_evento, local_evento, valor_evento)
                VALUES (?, ?, ?, ?, ?)";

        $stmt = $this->conn->prepare($query);

        $stmt->bindParam(1, $titulo);
        $stmt->bindParam(2, $data_evento);
        $stmt->bindParam(3, $hora_evento);
        $stmt->bindParam(4, $local_evento);
        $stmt->bindParam(5, $valor_evento);

        return $stmt->execute();
    }

    public function apagar($id) {
        $query = "DELETE FROM eventos_db WHERE id = :id";

        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':id', $id);

        return $stmt->execute();
    }

    public function editar($id, $titulo, $data, $hora, $local, $valor) {
        $query = "UPDATE eventos_db SET titulo = :titulo, 
                                    data_evento = :data, 
                                    hora_evento = :hora, 
                                    local_evento = :local, 
                                    valor_evento = :valor
                                    WHERE id = :id";

        $stmt = $this->conn->prepare($query);

        $stmt->bindParam(':titulo', $titulo);
        $stmt->bindParam(':data', $data);
        $stmt->bindParam(':hora', $hora);
        $stmt->bindParam(':local', $local);
        $stmt->bindParam(':valor', $valor);
        $stmt->bindParam(':id', $id);

        return $stmt->execute();
    }
    public function editarComFoto($id, $titulo, $foto, $tipo, $data, $hora, $local, $valor) {
        $query = "UPDATE eventos_db SET titulo = :titulo, 
                                    foto_evento = :foto,
                                    tipo_imagem = :tipo,
                                    data_evento = :data, 
                                    hora_evento = :hora, 
                                    local_evento = :local, 
                                    valor_evento = :valor
                                    WHERE id = :id";

        $stmt = $this->conn->prepare($query);

        $stmt->bindParam(':titulo', $titulo);
        $stmt->bindParam(':foto', $foto, PDO::PARAM_LOB);
        $stmt->bindParam(':tipo', $tipo);
        $stmt->bindParam(':data', $data);
        $stmt->bindParam(':hora', $hora);
        $stmt->bindParam(':local', $local);
        $stmt->bindParam(':valor', $valor);
        $stmt->bindParam(':id', $id);

        return $stmt->execute();
    }

    public function buscarPorId($id) {
        $query = "SELECT * FROM eventos_db WHERE id = :id";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':id', $id);
        $stmt->execute();
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }
}