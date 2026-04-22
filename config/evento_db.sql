drop database if exists evento_db;
CREATE DATABASE evento_db;

use evento_db;

drop table if exists evento_db;
CREATE TABLE eventos_db (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    
    foto_evento LONGBLOB,
    tipo_imagem VARCHAR(50),
    
    data_evento DATE NOT NULL,
    hora_evento TIME NOT NULL,
    local_evento VARCHAR(255) NOT NULL,
    valor_evento DECIMAL(10,2) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id int primary key auto_increment,
    nome varchar(255) not null,
	email varchar(255) not null unique,
    hash_senha varchar(255) not null,
    admin bool not null default True
);

INSERT INTO users (nome, email, hash_senha, admin) values
( "Marcos", "marcos@gmail.com", "$2y$10$geqhyjlx0FjuLdnzXGhRq.9iDJyo52wY4MBOFk8ufr1DIxfTLKgu6", True );

DROP TABLE IF EXISTS ingressos;
CREATE TABLE ingressos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    evento_id INT NOT NULL,
    data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    qr_code_hash VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (evento_id) REFERENCES eventos_db(id)
);