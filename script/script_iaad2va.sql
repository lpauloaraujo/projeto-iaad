CREATE SCHEMA startups2va;

USE startups2va;

CREATE TABLE cidades (
    id_cidade INT PRIMARY KEY,
    nome_cidade VARCHAR(255) NOT NULL
);

CREATE TABLE startup (
    id_startup INT PRIMARY KEY,
    nome_startup VARCHAR(255) NOT NULL,
    id_cidade INT,
    FOREIGN KEY (id_cidade) REFERENCES cidades(id_cidade) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE linguagem (
    id_linguagem INT PRIMARY KEY,
    nome_linguagem VARCHAR(20) NOT NULL
);

CREATE TABLE programador (
    id_programador INT PRIMARY KEY,
    nome_programador VARCHAR(255) NOT NULL,
    genero_programador CHAR(1) CHECK (genero_programador IN ('M', 'F')),
    data_nascimento DATE NOT NULL,
    id_startup INT,
    FOREIGN KEY (id_startup) REFERENCES startup(id_startup) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE dependentes (
    id_programador INT,
    nome_dependente VARCHAR(255),
    parentesco VARCHAR(50),
    data_dependente DATE,
    PRIMARY KEY (id_programador, nome_dependente),
    FOREIGN KEY (id_programador) REFERENCES programador(id_programador) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE programador_linguagem (
    id_programador INT,
    id_linguagem INT,
    PRIMARY KEY (id_programador, id_linguagem),
    FOREIGN KEY (id_programador) REFERENCES programador(id_programador) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_linguagem) REFERENCES linguagem(id_linguagem) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Populando a tabela cidades
INSERT INTO cidades VALUES
(1, 'Porto Alegre'),
(2, 'Belo Horizonte'),
(3, 'Rio de Janeiro'),
(4, 'Recife'),
(5, 'São Paulo'),
(6, 'Florianópolis'),
(7, 'Manaus');

-- Populando a tabela startup com a referência correta à cidade
INSERT INTO startup VALUES
(10001, 'Tech4Toy', 1),
(10002, 'Smart123', 2),
(10003, 'knowledgeUp', 3),
(10004, 'BSI Next Level', 4),
(10005, 'QualiHelth', 5),
(10006, 'ProEdu', 6),
(10007, 'CommerceIA', 7);

-- Populando a tabela linguagem
INSERT INTO linguagem VALUES
(20001, 'Python'),
(20002, 'PHP'),
(20003, 'Java'),
(20004, 'C'),
(20005, 'JavaScript'),
(20006, 'Dart'),
(20007, 'SQL');

-- Populando a tabela programador
INSERT INTO programador VALUES
(30001, 'João Pedro', 'M', '1993-06-23', 10001),
(30002, 'Paula Silva', 'F', '1986-01-10', 10002),
(30003, 'Renata Vieira', 'F', '1991-07-05', 10003),
(30004, 'Felipe Santos', 'M', '1976-11-25', 10004),
(30005, 'Ana Cristina', 'F', '1968-02-19', 10001),
(30006, 'Fernando Alves', 'M', '1988-07-07', 10004),
(30007, 'Laura Marques', 'F', '1987-10-04', 10002),
(30008, 'Lucas Lima', 'M', '2000-10-09', NULL),
(30009, 'Camila Macedo', 'F', '1995-07-03', NULL),
(30010, 'Leonardo Ramos', 'M', '2005-07-05', NULL),
(30011, 'Alice Lins', 'F', '2000-10-09', 10007);

-- Populando a tabela dependentes
INSERT INTO dependentes VALUES
(30001, 'André Sousa', 'Filho', '2020-02-15'),
(30002, 'Luciana Silva', 'Filha', '2018-07-26'),
(30002, 'Elisa Silva', 'Filha', '2020-01-06'),
(30002, 'Breno Silva', 'Esposo', '1984-05-21'),
(30004, 'Rafaela Santos', 'Esposa', '1980-02-12'),
(30004, 'Marcos Martins', 'Filho', '2008-03-26'),
(30006, 'Laís Meneses', 'Esposa', '1990-11-09'),
(30007, 'Daniel Marques', 'Filho', '2014-06-06'),
(30009, 'Lidiane Macedo', 'Filha', '2015-04-14');

-- Populando a tabela programador_linguagem
INSERT INTO programador_linguagem VALUES
(30001, 20001),
(30001, 20002),
(30002, 20003),
(30003, 20004),
(30003, 20005),
(30004, 20005),
(30007, 20001),
(30007, 20002),
(30009, 20004),
(30009, 20007),
(30010, 20007);

-- Trigger para impedir programadores menores de 18 anos
DELIMITER $$
CREATE TRIGGER Apenas_Maiores 
BEFORE INSERT ON programador
FOR EACH ROW
BEGIN
    IF TIMESTAMPDIFF(YEAR, NEW.data_nascimento, CURDATE()) < 18 THEN 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Não é permitido inserir programadores que possuem menos de 18 anos.';
    END IF;
END$$
DELIMITER ;

-- Trigger para impedir que a startup 10002 contrate homens
DELIMITER $$
CREATE TRIGGER Apenas_Mulheres
BEFORE INSERT ON programador
FOR EACH ROW
BEGIN
    IF NEW.id_startup = 10002 AND NEW.genero_programador = 'M' THEN 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A startup de id 10002 contrata apenas mulheres.';
    END IF;
END$$
DELIMITER ;

