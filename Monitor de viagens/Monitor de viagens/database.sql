-- Linha 1: Cria o banco de dados especificado.
CREATE DATABASE IF NOT EXISTS monitor_viagens CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Linha 2: Executa uma instrução SQL desta linha.
USE monitor_viagens;
-- Linha 3: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS usuarios (
 -- Linha 4: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 5: Executa uma instrução SQL desta linha.
 nome VARCHAR(120) NOT NULL,
 -- Linha 6: Executa uma instrução SQL desta linha.
 email VARCHAR(180) NOT NULL UNIQUE,
 -- Linha 7: Executa uma instrução SQL desta linha.
 telefone VARCHAR(25) NOT NULL UNIQUE,
 -- Linha 8: Executa uma instrução SQL desta linha.
 senha VARCHAR(255) NOT NULL,
 -- Linha 9: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
-- Linha 10: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;
-- Linha 11: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS viagens (
 -- Linha 12: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 13: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 14: Executa uma instrução SQL desta linha.
 origem VARCHAR(180) NOT NULL,
 -- Linha 15: Executa uma instrução SQL desta linha.
 destino VARCHAR(180) NOT NULL,
 -- Linha 16: Executa uma instrução SQL desta linha.
 data_ida DATE NOT NULL,
 -- Linha 17: Executa uma instrução SQL desta linha.
 data_volta DATE NULL,
 -- Linha 18: Executa uma instrução SQL desta linha.
 criada_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 19: Executa uma instrução SQL desta linha.
 CONSTRAINT fk_viagens_usuario FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
-- Linha 20: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;
-- Linha 21: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS lugares_favoritos (
 -- Linha 22: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 23: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 24: Executa uma instrução SQL desta linha.
 nome VARCHAR(180) NOT NULL,
 -- Linha 25: Executa uma instrução SQL desta linha.
 cidade VARCHAR(180) NOT NULL DEFAULT '',
 -- Linha 26: Executa uma instrução SQL desta linha.
 tipo VARCHAR(60) NOT NULL DEFAULT 'lugar',
 -- Linha 27: Executa uma instrução SQL desta linha.
 latitude DOUBLE NULL,
 -- Linha 28: Executa uma instrução SQL desta linha.
 longitude DOUBLE NULL,
 -- Linha 29: Executa uma instrução SQL desta linha.
 lista VARCHAR(20) NOT NULL DEFAULT 'favorito',
 -- Linha 30: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 31: Executa uma instrução SQL desta linha.
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 -- Linha 32: Executa uma instrução SQL desta linha.
 INDEX idx_favoritos_usuario (usuario_id)
-- Linha 33: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;
-- Linha 34: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS alertas_preco (
 -- Linha 35: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 36: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 37: Executa uma instrução SQL desta linha.
 destino VARCHAR(180) NOT NULL,
 -- Linha 38: Executa uma instrução SQL desta linha.
 tipo VARCHAR(40) NOT NULL DEFAULT 'pacote',
 -- Linha 39: Executa uma instrução SQL desta linha.
 preco_alvo DECIMAL(12,2) NOT NULL,
 -- Linha 40: Executa uma instrução SQL desta linha.
 ativo BOOLEAN NOT NULL DEFAULT TRUE,
 -- Linha 41: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 42: Executa uma instrução SQL desta linha.
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 -- Linha 43: Executa uma instrução SQL desta linha.
 INDEX idx_alertas_usuario (usuario_id)
-- Linha 44: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;
-- Linha 45: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS itens_carrinho (
 -- Linha 46: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 47: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 48: Executa uma instrução SQL desta linha.
 categoria VARCHAR(40) NOT NULL,
 -- Linha 49: Executa uma instrução SQL desta linha.
 nome VARCHAR(220) NOT NULL,
 -- Linha 50: Executa uma instrução SQL desta linha.
 quantidade INT NOT NULL DEFAULT 1,
 -- Linha 51: Executa uma instrução SQL desta linha.
 preco_unitario DECIMAL(12,2) NOT NULL DEFAULT 0,
 -- Linha 52: Executa uma instrução SQL desta linha.
 total DECIMAL(12,2) NOT NULL DEFAULT 0,
 -- Linha 53: Executa uma instrução SQL desta linha.
 origem VARCHAR(40) NOT NULL DEFAULT 'simulado',
 -- Linha 54: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 55: Executa uma instrução SQL desta linha.
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 -- Linha 56: Executa uma instrução SQL desta linha.
 INDEX idx_carrinho_usuario (usuario_id)
-- Linha 57: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;
-- Linha 58: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS pedidos_orcamento (
 -- Linha 59: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 60: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 61: Executa uma instrução SQL desta linha.
 total DECIMAL(12,2) NOT NULL DEFAULT 0,
 -- Linha 62: Executa uma instrução SQL desta linha.
 status VARCHAR(30) NOT NULL DEFAULT 'planejamento',
 -- Linha 63: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 64: Executa uma instrução SQL desta linha.
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 -- Linha 65: Executa uma instrução SQL desta linha.
 INDEX idx_pedidos_usuario (usuario_id)
-- Linha 66: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;
-- Linha 67: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS itens_roteiro (
 -- Linha 68: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 69: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 70: Executa uma instrução SQL desta linha.
 data DATE NOT NULL,
 -- Linha 71: Executa uma instrução SQL desta linha.
 horario VARCHAR(5) NOT NULL DEFAULT '09:00',
 -- Linha 72: Executa uma instrução SQL desta linha.
 titulo VARCHAR(180) NOT NULL,
 -- Linha 73: Executa uma instrução SQL desta linha.
 tipo VARCHAR(50) NOT NULL DEFAULT 'atividade',
 -- Linha 74: Executa uma instrução SQL desta linha.
 latitude DOUBLE NULL,
 -- Linha 75: Executa uma instrução SQL desta linha.
 longitude DOUBLE NULL,
 -- Linha 76: Executa uma instrução SQL desta linha.
 notas VARCHAR(500) NOT NULL DEFAULT '',
 -- Linha 77: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 78: Executa uma instrução SQL desta linha.
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 -- Linha 79: Executa uma instrução SQL desta linha.
 INDEX idx_roteiro_usuario (usuario_id),
 -- Linha 80: Executa uma instrução SQL desta linha.
 INDEX idx_roteiro_data (data)
-- Linha 81: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;

-- Linha 83: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS roteiros (
 -- Linha 84: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 85: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 86: Executa uma instrução SQL desta linha.
 destino VARCHAR(180) NOT NULL,
 -- Linha 87: Executa uma instrução SQL desta linha.
 data_inicio DATE NOT NULL,
 -- Linha 88: Executa uma instrução SQL desta linha.
 dias INT NOT NULL,
 -- Linha 89: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 90: Executa uma instrução SQL desta linha.
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 -- Linha 91: Executa uma instrução SQL desta linha.
 INDEX idx_roteiros_usuario (usuario_id)
-- Linha 92: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;

-- Linha 94: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS roteiro_itens (
 -- Linha 95: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 96: Executa uma instrução SQL desta linha.
 roteiro_id INT UNSIGNED NOT NULL,
 -- Linha 97: Executa uma instrução SQL desta linha.
 dia INT NOT NULL,
 -- Linha 98: Executa uma instrução SQL desta linha.
 horario_inicio VARCHAR(5) NOT NULL DEFAULT '12:00',
 -- Linha 99: Executa uma instrução SQL desta linha.
 horario_fim VARCHAR(5) NOT NULL DEFAULT '13:00',
 -- Linha 100: Executa uma instrução SQL desta linha.
 titulo VARCHAR(180) NOT NULL,
 -- Linha 101: Executa uma instrução SQL desta linha.
 tipo VARCHAR(50) NOT NULL DEFAULT 'atividade',
 -- Linha 102: Executa uma instrução SQL desta linha.
 latitude DOUBLE NULL,
 -- Linha 103: Executa uma instrução SQL desta linha.
 longitude DOUBLE NULL,
 -- Linha 104: Executa uma instrução SQL desta linha.
 notas VARCHAR(500) NOT NULL DEFAULT '',
 -- Linha 105: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 106: Executa uma instrução SQL desta linha.
 FOREIGN KEY(roteiro_id) REFERENCES roteiros(id) ON DELETE CASCADE,
 -- Linha 107: Executa uma instrução SQL desta linha.
 INDEX idx_roteiro_itens_roteiro (roteiro_id)
-- Linha 108: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;

-- Linha 110: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS roteiro_membros (
 -- Linha 111: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 112: Executa uma instrução SQL desta linha.
 roteiro_id INT UNSIGNED NOT NULL,
 -- Linha 113: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 114: Executa uma instrução SQL desta linha.
 papel VARCHAR(20) NOT NULL DEFAULT 'membro',
 -- Linha 115: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 116: Executa uma instrução SQL desta linha.
 FOREIGN KEY(roteiro_id) REFERENCES roteiros(id) ON DELETE CASCADE,
 -- Linha 117: Executa uma instrução SQL desta linha.
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 -- Linha 118: Executa uma instrução SQL desta linha.
 UNIQUE KEY uq_roteiro_membro (roteiro_id, usuario_id),
 -- Linha 119: Executa uma instrução SQL desta linha.
 INDEX idx_roteiro_membros_usuario (usuario_id)
-- Linha 120: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;

-- Linha 122: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS viagens_grupo (
 -- Linha 123: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 124: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 125: Executa uma instrução SQL desta linha.
 nome VARCHAR(180) NOT NULL,
 -- Linha 126: Executa uma instrução SQL desta linha.
 destino VARCHAR(180) NOT NULL,
 -- Linha 127: Executa uma instrução SQL desta linha.
 data_inicio DATE NULL,
 -- Linha 128: Executa uma instrução SQL desta linha.
 dias INT NOT NULL DEFAULT 1,
 -- Linha 129: Executa uma instrução SQL desta linha.
 descricao VARCHAR(500) NOT NULL DEFAULT '',
 -- Linha 130: Executa uma instrução SQL desta linha.
 token VARCHAR(64) NOT NULL UNIQUE,
 -- Linha 131: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 132: Executa uma instrução SQL desta linha.
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 -- Linha 133: Executa uma instrução SQL desta linha.
 INDEX idx_viagens_grupo_usuario (usuario_id)
-- Linha 134: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;

-- Linha 136: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS viagens_grupo_membros (
 -- Linha 137: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 138: Executa uma instrução SQL desta linha.
 grupo_id INT UNSIGNED NOT NULL,
 -- Linha 139: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 140: Executa uma instrução SQL desta linha.
 papel VARCHAR(20) NOT NULL DEFAULT 'membro',
 -- Linha 141: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 142: Executa uma instrução SQL desta linha.
 FOREIGN KEY(grupo_id) REFERENCES viagens_grupo(id) ON DELETE CASCADE,
 -- Linha 143: Executa uma instrução SQL desta linha.
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 -- Linha 144: Executa uma instrução SQL desta linha.
 UNIQUE KEY uq_grupo_membro (grupo_id, usuario_id),
 -- Linha 145: Executa uma instrução SQL desta linha.
 INDEX idx_grupo_membros_usuario (usuario_id)
-- Linha 146: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;

-- Linha 148: Cria uma tabela para armazenar os dados indicados.
CREATE TABLE IF NOT EXISTS viagens_grupo_itens (
 -- Linha 149: Executa uma instrução SQL desta linha.
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -- Linha 150: Executa uma instrução SQL desta linha.
 grupo_id INT UNSIGNED NOT NULL,
 -- Linha 151: Executa uma instrução SQL desta linha.
 usuario_id INT UNSIGNED NOT NULL,
 -- Linha 152: Executa uma instrução SQL desta linha.
 categoria VARCHAR(50) NOT NULL DEFAULT 'atividade',
 -- Linha 153: Executa uma instrução SQL desta linha.
 nome VARCHAR(220) NOT NULL,
 -- Linha 154: Executa uma instrução SQL desta linha.
 quantidade INT NOT NULL DEFAULT 1,
 -- Linha 155: Executa uma instrução SQL desta linha.
 preco DECIMAL(12,2) NOT NULL DEFAULT 0,
 -- Linha 156: Executa uma instrução SQL desta linha.
 criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- Linha 157: Executa uma instrução SQL desta linha.
 FOREIGN KEY(grupo_id) REFERENCES viagens_grupo(id) ON DELETE CASCADE,
 -- Linha 158: Executa uma instrução SQL desta linha.
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 -- Linha 159: Executa uma instrução SQL desta linha.
 INDEX idx_grupo_itens_grupo (grupo_id)
-- Linha 160: Executa uma instrução SQL desta linha.
) ENGINE=InnoDB;
