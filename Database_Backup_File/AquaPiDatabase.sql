-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 25, 2020 at 09:27 PM
-- Server version: 10.3.22-MariaDB-0+deb10u1
-- PHP Version: 7.3.14-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `AquaPiDatabase`
--
CREATE DATABASE IF NOT EXISTS `AquaPiDatabase` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `AquaPiDatabase`;

-- --------------------------------------------------------

--
-- Table structure for table `Client`
--

DROP TABLE IF EXISTS `Client`;
CREATE TABLE `Client` (
  `macAdress` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ipAdress` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `hostName` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `Client`
--

-- --------------------------------------------------------

--
-- Table structure for table `SensorMeasurement`
--

DROP TABLE IF EXISTS `SensorMeasurement`;
CREATE TABLE `SensorMeasurement` (
  `sensorMeasurementId` int(10) UNSIGNED NOT NULL,
  `plantHumidity` float UNSIGNED NOT NULL,
  `roomHumidity` float UNSIGNED NOT NULL,
  `roomTemperature` float UNSIGNED NOT NULL,
  `waterTankLevel` float UNSIGNED NOT NULL,
  `timeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `clientMacAdressRefference` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `WateringProcess`
--

DROP TABLE IF EXISTS `WateringProcess`;
CREATE TABLE `WateringProcess` (
  `wateringProcessId` int(10) UNSIGNED NOT NULL,
  `timeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `clientMacAdressRefference` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=COMPACT;

--
-- Dumping data for table `WateringProcess`
--
-- Indexes for dumped tables
--

--
-- Indexes for table `Client`
--
ALTER TABLE `Client`
  ADD PRIMARY KEY (`macAdress`);

--
-- Indexes for table `SensorMeasurement`
--
ALTER TABLE `SensorMeasurement`
  ADD PRIMARY KEY (`sensorMeasurementId`),
  ADD KEY `clientMacAdressRefference` (`clientMacAdressRefference`);

--
-- Indexes for table `WateringProcess`
--
ALTER TABLE `WateringProcess`
  ADD PRIMARY KEY (`wateringProcessId`),
  ADD KEY `clientMacAdressRefference` (`clientMacAdressRefference`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `SensorMeasurement`
--
ALTER TABLE `SensorMeasurement`
  MODIFY `sensorMeasurementId` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1772;
--
-- AUTO_INCREMENT for table `WateringProcess`
--
ALTER TABLE `WateringProcess`
  MODIFY `wateringProcessId` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=217;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `SensorMeasurement`
--
ALTER TABLE `SensorMeasurement`
  ADD CONSTRAINT `SensorMeasurement_ibfk_1` FOREIGN KEY (`clientMacAdressRefference`) REFERENCES `Client` (`macAdress`) ON UPDATE CASCADE;

--
-- Constraints for table `WateringProcess`
--
ALTER TABLE `WateringProcess`
  ADD CONSTRAINT `WateringProcess_ibfk_1` FOREIGN KEY (`clientMacAdressRefference`) REFERENCES `Client` (`macAdress`) ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
