-- Banco da API de livros e produtos.
CREATE DATABASE IF NOT EXISTS biblioteca_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE biblioteca_db;

CREATE TABLE IF NOT EXISTS livros (
  id INT NOT NULL AUTO_INCREMENT,
  titulo VARCHAR(150) NOT NULL,
  autor VARCHAR(120) NOT NULL,
  ano_publicacao INT NOT NULL,
  disponivel BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (id),
  INDEX ix_livros_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS produtos (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(100) NOT NULL,
  preco FLOAT NOT NULL,
  quantidade INT NOT NULL,
  PRIMARY KEY (id),
  INDEX ix_produtos_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
