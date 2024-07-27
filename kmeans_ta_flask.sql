-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 27, 2023 at 06:35 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kmeans_ta_flask`
--

-- --------------------------------------------------------

--
-- Table structure for table `dataset`
--

CREATE TABLE `dataset` (
  `id` bigint(20) NOT NULL,
  `sintaid` bigint(20) DEFAULT NULL,
  `nidn` bigint(20) DEFAULT NULL,
  `nama` varchar(225) DEFAULT NULL,
  `afiliasi` varchar(255) DEFAULT NULL,
  `prodi` varchar(255) DEFAULT NULL,
  `pendidikan` varchar(255) DEFAULT NULL,
  `jabatan` varchar(255) DEFAULT NULL,
  `gelar_depan` varchar(255) DEFAULT NULL,
  `gelar_belakang` varchar(255) DEFAULT NULL,
  `sinta_overall_v2` varchar(255) DEFAULT NULL,
  `sinta_3y_v2` varchar(255) DEFAULT NULL,
  `sinta_overall_v3` varchar(255) DEFAULT NULL,
  `sinta_3y_v3` varchar(255) DEFAULT NULL,
  `afiliasi_overall` varchar(255) DEFAULT NULL,
  `afiliasi_3y` varchar(255) DEFAULT NULL,
  `dok_scopus` varchar(255) DEFAULT NULL,
  `sit_scopus` varchar(255) DEFAULT NULL,
  `dok_sit_scopus` varchar(255) DEFAULT NULL,
  `h_i_scopus` varchar(255) DEFAULT NULL,
  `g_i_scopus` varchar(255) DEFAULT NULL,
  `i10_i_scopus` varchar(255) DEFAULT NULL,
  `dok_gs` varchar(255) DEFAULT NULL,
  `sit_gs` varchar(255) DEFAULT NULL,
  `dok_sit_gs` varchar(255) DEFAULT NULL,
  `h_i_gs` varchar(255) DEFAULT NULL,
  `g_i_gs` varchar(255) DEFAULT NULL,
  `i10_i_gs` varchar(255) DEFAULT NULL,
  `dok_wos` varchar(255) DEFAULT NULL,
  `sit_wos` varchar(255) DEFAULT NULL,
  `dok_sit_wos` varchar(255) DEFAULT NULL,
  `h_i_wos` varchar(255) DEFAULT NULL,
  `g_i_wos` varchar(255) DEFAULT NULL,
  `i10_i_wos` varchar(255) DEFAULT NULL,
  `dok_garuda` varchar(255) DEFAULT NULL,
  `sit_garuda` varchar(255) DEFAULT NULL,
  `dok_sit_garuda` varchar(255) DEFAULT NULL,
  `stat_aktif` varchar(255) DEFAULT NULL,
  `stat_verif` varchar(255) DEFAULT NULL,
  `cluster` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `instruksi`
--

CREATE TABLE `instruksi` (
  `id` int(11) NOT NULL,
  `kluster` int(11) NOT NULL,
  `iterasi` int(11) NOT NULL,
  `parameter` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tester`
--

CREATE TABLE `tester` (
  `id` int(11) NOT NULL,
  `merk` varchar(225) NOT NULL,
  `produk` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tester`
--

INSERT INTO `tester` (`id`, `merk`, `produk`) VALUES
(1, 'lenovo', 'laptop'),
(2, 'samsung', 'smartphone'),
(3, 'apple', 'ipda');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(225) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`) VALUES
(1, '1911500583', '1911500583@student.budiluhur.ac.id', '1911500583');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dataset`
--
ALTER TABLE `dataset`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `instruksi`
--
ALTER TABLE `instruksi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tester`
--
ALTER TABLE `tester`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dataset`
--
ALTER TABLE `dataset`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `instruksi`
--
ALTER TABLE `instruksi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tester`
--
ALTER TABLE `tester`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
