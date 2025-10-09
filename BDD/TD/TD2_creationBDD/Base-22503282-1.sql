-- phpMyAdmin SQL Dump
-- version 5.2.1deb1+deb12u1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : mar. 16 sep. 2025 à 09:49
-- Version du serveur : 10.11.14-MariaDB-0+deb12u2
-- Version de PHP : 8.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `Base-22503282-1`
--

-- --------------------------------------------------------

--
-- Structure de la table `driver`
--

CREATE TABLE `driver` (
  `driverID` int(6) NOT NULL,
  `dFirstName` varchar(25) NOT NULL,
  `dLastName` varchar(25) NOT NULL,
  `dBirthDate` date NOT NULL,
  `dDeathDate` date DEFAULT NULL,
  `dCountry` varchar(25) NOT NULL,
  `dGender` enum('M','F') NOT NULL DEFAULT 'F'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Déchargement des données de la table `driver`
--

INSERT INTO `driver` (`driverID`, `dFirstName`, `dLastName`, `dBirthDate`, `dDeathDate`, `dCountry`, `dGender`) VALUES
(1, 'Fernando', 'Alonso', '1981-07-29', NULL, 'Spain', 'M'),
(2, 'Jules', 'Bianchi', '1989-08-03', '2015-07-17', 'France', 'M'),
(23, 'Sebastian', 'Vettel', '1987-07-03', NULL, 'Germany', 'M');

-- --------------------------------------------------------

--
-- Structure de la table `racedriver`
--

CREATE TABLE `racedriver` (
  `teamID` int(6) NOT NULL,
  `driverID` int(6) NOT NULL,
  `rSeason` year(4) NOT NULL,
  `rDriverNb` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Déchargement des données de la table `racedriver`
--

INSERT INTO `racedriver` (`teamID`, `driverID`, `rSeason`, `rDriverNb`) VALUES
(2, 23, '2014', 1),
(4, 1, '2014', 14);

-- --------------------------------------------------------

--
-- Structure de la table `team`
--

CREATE TABLE `team` (
  `teamID` int(6) NOT NULL,
  `tName` varchar(25) NOT NULL,
  `tCountry` varchar(25) NOT NULL,
  `twas` int(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Déchargement des données de la table `team`
--

INSERT INTO `team` (`teamID`, `tName`, `tCountry`, `twas`) VALUES
(2, 'Red Bull Racing-Renault', 'Austria', NULL),
(4, 'Ferrari', 'Italy', NULL);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `driver`
--
ALTER TABLE `driver`
  ADD PRIMARY KEY (`driverID`);

--
-- Index pour la table `racedriver`
--
ALTER TABLE `racedriver`
  ADD PRIMARY KEY (`teamID`,`driverID`,`rSeason`),
  ADD KEY `driverID` (`driverID`);

--
-- Index pour la table `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`teamID`),
  ADD KEY `teamID` (`twas`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `driver`
--
ALTER TABLE `driver`
  MODIFY `driverID` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT pour la table `team`
--
ALTER TABLE `team`
  MODIFY `teamID` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `racedriver`
--
ALTER TABLE `racedriver`
  ADD CONSTRAINT `racedriver_ibfk_1` FOREIGN KEY (`teamID`) REFERENCES `team` (`teamID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `racedriver_ibfk_2` FOREIGN KEY (`driverID`) REFERENCES `driver` (`driverID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `team`
--
ALTER TABLE `team`
  ADD CONSTRAINT `team_ibfk_1` FOREIGN KEY (`twas`) REFERENCES `team` (`teamID`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
