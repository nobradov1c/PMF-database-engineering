-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema library
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema library
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `library` DEFAULT CHARACTER SET utf8 ;
USE `library` ;

-- -----------------------------------------------------
-- Table `library`.`Author`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`Author` (
  `idAuthor` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idAuthor`),
  UNIQUE INDEX `idAuthor_UNIQUE` (`idAuthor` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`Publisher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`Publisher` (
  `idPublisher` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idPublisher`),
  UNIQUE INDEX `idPublisher_UNIQUE` (`idPublisher` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`Book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`Book` (
  `idBook` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `publishYear` INT NOT NULL,
  `idAuthor` INT NOT NULL,
  `idPublisher` INT NOT NULL,
  PRIMARY KEY (`idBook`),
  UNIQUE INDEX `idBook_UNIQUE` (`idBook` ASC) VISIBLE,
  INDEX `fk_Book_Author_idx` (`idAuthor` ASC) VISIBLE,
  INDEX `fk_Book_Publisher1_idx` (`idPublisher` ASC) VISIBLE,
  CONSTRAINT `fk_Book_Author`
    FOREIGN KEY (`idAuthor`)
    REFERENCES `library`.`Author` (`idAuthor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Book_Publisher1`
    FOREIGN KEY (`idPublisher`)
    REFERENCES `library`.`Publisher` (`idPublisher`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`Genre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`Genre` (
  `idGenre` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idGenre`),
  UNIQUE INDEX `idGenre_UNIQUE` (`idGenre` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`Book_has_Genre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`Book_has_Genre` (
  `idBook` INT NOT NULL,
  `idGenre` INT NOT NULL,
  PRIMARY KEY (`idBook`, `idGenre`),
  INDEX `fk_Book_has_Genre_Genre1_idx` (`idGenre` ASC) VISIBLE,
  INDEX `fk_Book_has_Genre_Book1_idx` (`idBook` ASC) VISIBLE,
  CONSTRAINT `fk_Book_has_Genre_Book1`
    FOREIGN KEY (`idBook`)
    REFERENCES `library`.`Book` (`idBook`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Book_has_Genre_Genre1`
    FOREIGN KEY (`idGenre`)
    REFERENCES `library`.`Genre` (`idGenre`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`BookStore`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`BookStore` (
  `idBookStore` INT NOT NULL AUTO_INCREMENT,
  `city` VARCHAR(45) NOT NULL,
  `street` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idBookStore`),
  UNIQUE INDEX `idBookStore_UNIQUE` (`idBookStore` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`Librarian`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`Librarian` (
  `idLibrarian` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `idBookStore` INT NOT NULL,
  PRIMARY KEY (`idLibrarian`),
  UNIQUE INDEX `idLibrarian_UNIQUE` (`idLibrarian` ASC) VISIBLE,
  INDEX `fk_Librarian_BookStore1_idx` (`idBookStore` ASC) VISIBLE,
  CONSTRAINT `fk_Librarian_BookStore1`
    FOREIGN KEY (`idBookStore`)
    REFERENCES `library`.`BookStore` (`idBookStore`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`MembershipType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`MembershipType` (
  `idMembershipType` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `price` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idMembershipType`),
  UNIQUE INDEX `idMembershipType_UNIQUE` (`idMembershipType` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`ActiveMembership`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`ActiveMembership` (
  `idActiveMembership` INT NOT NULL AUTO_INCREMENT,
  `expiredDate` DATE NOT NULL,
  `lastActiveMembershipTypeId` INT NOT NULL,
  PRIMARY KEY (`idActiveMembership`),
  UNIQUE INDEX `idActiveMembership_UNIQUE` (`idActiveMembership` ASC) VISIBLE,
  INDEX `fk_ActiveMembership_MembershipType1_idx` (`lastActiveMembershipTypeId` ASC) VISIBLE,
  CONSTRAINT `fk_ActiveMembership_MembershipType1`
    FOREIGN KEY (`lastActiveMembershipTypeId`)
    REFERENCES `library`.`MembershipType` (`idMembershipType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`Customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`Customer` (
  `idCustomer` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `birthYear` INT NOT NULL,
  `membershipId` INT NOT NULL,
  PRIMARY KEY (`idCustomer`),
  UNIQUE INDEX `idCustomer_UNIQUE` (`idCustomer` ASC) VISIBLE,
  INDEX `fk_Customer_ActiveMembership1_idx` (`membershipId` ASC) VISIBLE,
  CONSTRAINT `fk_Customer_ActiveMembership1`
    FOREIGN KEY (`membershipId`)
    REFERENCES `library`.`ActiveMembership` (`idActiveMembership`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`Book_has_BookStore`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`Book_has_BookStore` (
  `idBook` INT NOT NULL,
  `idBookStore` INT NOT NULL,
  `rentedCount` INT NOT NULL,
  `availableCount` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idBook`, `idBookStore`),
  INDEX `fk_Book_has_BookStore_BookStore1_idx` (`idBookStore` ASC) VISIBLE,
  INDEX `fk_Book_has_BookStore_Book1_idx` (`idBook` ASC) VISIBLE,
  CONSTRAINT `fk_Book_has_BookStore_Book1`
    FOREIGN KEY (`idBook`)
    REFERENCES `library`.`Book` (`idBook`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Book_has_BookStore_BookStore1`
    FOREIGN KEY (`idBookStore`)
    REFERENCES `library`.`BookStore` (`idBookStore`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library`.`RentedBook`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`RentedBook` (
  `idRentedBook` INT NOT NULL AUTO_INCREMENT,
  `idCustomer` INT NOT NULL,
  `startRentDate` DATE NOT NULL,
  `returnDate` DATE NULL,
  `rentLimitDate` DATE NOT NULL,
  `idBook` INT NOT NULL,
  `idBookStore` INT NOT NULL,
  PRIMARY KEY (`idRentedBook`, `idCustomer`),
  UNIQUE INDEX `idRentedBook_UNIQUE` (`idRentedBook` ASC) VISIBLE,
  INDEX `fk_RentedBook_Customer1_idx` (`idCustomer` ASC) VISIBLE,
  INDEX `fk_RentedBook_Book_has_BookStore1_idx` (`idBook` ASC, `idBookStore` ASC) VISIBLE,
  CONSTRAINT `fk_RentedBook_Customer1`
    FOREIGN KEY (`idCustomer`)
    REFERENCES `library`.`Customer` (`idCustomer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_RentedBook_Book_has_BookStore1`
    FOREIGN KEY (`idBook` , `idBookStore`)
    REFERENCES `library`.`Book_has_BookStore` (`idBook` , `idBookStore`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
