<?php
class Database {
    private $host = "127.0.0.1";
    private $port = "3307";
    private $db_name = "evento_db"; 
    private $username = "root";
    private $password = "";
    private $conn;

    public function getConnection(){
        $this -> conn = null;
        try{
            $this ->conn = new PDO('mysql:host='.$this->host.
                                ";dbname=".$this->db_name.
                                ";port=3307", $this->username, $this->password );
            $this->conn->setAttribute(PDO::ATTR_EMULATE_PREPARES,false);
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch(PDOException $erro){
            echo "Erro de conexão". $erro->getMessage();
        }
        return $this->conn;
    }
}