-- Adminer 4.8.1 MySQL 8.0.30 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `klastering_siswa`;
CREATE DATABASE `klastering_siswa` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `klastering_siswa`;

DROP TABLE IF EXISTS `dataset`;
CREATE TABLE `dataset` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nis` int NOT NULL,
  `nama_siswa` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `kelas` int DEFAULT NULL,
  `nilai_mtk` int DEFAULT NULL,
  `nilai_bindo` int DEFAULT NULL,
  `nilai_binggris` int DEFAULT NULL,
  `nilai_ipa` int DEFAULT NULL,
  `nilai_ips` int DEFAULT NULL,
  `nilai_total` int DEFAULT NULL,
  `rata_rata` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cluster` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `instruksi`;
CREATE TABLE `instruksi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `kluster` int NOT NULL,
  `iterasi` int NOT NULL,
  `parameter` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

TRUNCATE `users`;
INSERT INTO `users` (`id`, `username`, `email`, `password`) VALUES
(1,	'admin',	'admin@gmail.com',	'admin');

-- 2024-07-27 13:13:49
