-- Cria usuario de acesso
CREATE USER 'admin'@'%' IDENTIFIED BY 'admin';
FLUSH PRIVILEGES;

-- Armazena as configurações atuais e desativa temporariamente algumas verificações de integridade para permitir operações em massa ou específicas
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Cria e usa a database
CREATE SCHEMA IF NOT EXISTS `data_db` DEFAULT CHARACTER SET utf8 ;
USE `data_db` ;

-- Garante acesso ao usuario à database
GRANT SELECT, UPDATE, DELETE, INSERT ON data_db.* TO 'admin'@'%';
FLUSH PRIVILEGES;

-- Cria e tabela e as culunas de "users"
CREATE TABLE IF NOT EXISTS `data_db`.`users` (
  `idUsers` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`idUsers`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) )
ENGINE = InnoDB;

-- Cria e tabela e as culunas de "tarefas"
CREATE TABLE IF NOT EXISTS `data_db`.`tarefas` (
  `idTarefa` INT NOT NULL AUTO_INCREMENT,
  `users_idUsers` INT NOT NULL,
  `descricao` VARCHAR(255) NULL,
  `nomeSetor` VARCHAR(45) NOT NULL,
  `prioridade` VARCHAR(45) NOT NULL,
  `dataCadastro` DATE NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTarefa`, `users_idUsers`),
  INDEX `fk_tarefas_users_idx` (`users_idUsers` ASC),
  CONSTRAINT `fk_tarefas_users`
    FOREIGN KEY (`users_idUsers`)
    REFERENCES `data_db`.`users` (`idUsers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Restaura as configurações originais de SQL_MODE, verificação de chaves estrangeiras e verificação de unicidade
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
