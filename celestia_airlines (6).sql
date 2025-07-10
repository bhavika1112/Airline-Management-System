-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 22, 2025 at 02:18 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `celestia_airlines`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `password`) VALUES
(1, 'mahek@gmail.com', 'mahesh@1'),
(2, 'bhavika@gmail.com', 'bhavi@123');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `passenger_name` varchar(100) DEFAULT NULL,
  `flight_id` int(11) NOT NULL,
  `seat_id` varchar(10) NOT NULL,
  `payment_status` enum('pending','completed') NOT NULL,
  `seat_class` enum('economy','business','first_class') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `customer_id`, `passenger_name`, `flight_id`, `seat_id`, `payment_status`, `seat_class`) VALUES
(49, 5, 'Riya', 20, 'B6', 'pending', 'economy'),
(50, 5, 'Riya', 22, 'A5', 'pending', 'business'),
(51, 5, 'Riya', 20, 'B4', 'pending', 'first_class');

-- --------------------------------------------------------

--
-- Table structure for table `crew`
--

CREATE TABLE `crew` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `passenger_name` varchar(255) DEFAULT NULL,
  `age` text NOT NULL,
  `flight_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `crew`
--

INSERT INTO `crew` (`id`, `name`, `passenger_name`, `age`, `flight_id`) VALUES
(16, 'Nitya', NULL, '33', 20),
(17, 'Nitya', NULL, '33', 20),
(18, 'Raha', NULL, '33', 20),
(19, 'Mahek', NULL, '22', 20),
(20, 'Bhavik', NULL, '44', 21);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `flight_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id`, `email`, `password`, `flight_id`) VALUES
(1, 'customer1@gmail.com', 'cust123', NULL),
(5, 'riya@gmail.com', 'riya@123', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `flights`
--

CREATE TABLE `flights` (
  `id` int(11) NOT NULL,
  `source` varchar(255) NOT NULL,
  `destination` varchar(255) NOT NULL,
  `departure_date` date NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `economy_seats` int(11) NOT NULL DEFAULT 60,
  `business_seats` int(11) NOT NULL DEFAULT 20,
  `first_class_seats` int(11) NOT NULL DEFAULT 10,
  `economy_price` decimal(10,2) NOT NULL,
  `business_price` decimal(10,2) NOT NULL,
  `first_class_price` decimal(10,2) NOT NULL,
  `departure_time` time DEFAULT NULL,
  `arrival_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flights`
--

INSERT INTO `flights` (`id`, `source`, `destination`, `departure_date`, `price`, `economy_seats`, `business_seats`, `first_class_seats`, `economy_price`, `business_price`, `first_class_price`, `departure_time`, `arrival_time`) VALUES
(20, 'Kolkata', 'Mumbai', '2025-04-25', 0.00, 60, 20, 10, 14000.00, 20000.00, 18000.00, '03:30:00', '08:00:00'),
(21, 'Vadodara', 'Mumbai', '2025-04-25', 0.00, 60, 20, 10, 10000.00, 15000.00, 12000.00, '04:00:00', '08:00:00'),
(22, 'Mumbai', 'Delhi', '2025-05-01', 0.00, 60, 20, 10, 4500.00, 9000.00, 15000.00, '08:00:00', '10:15:00'),
(23, 'Mumbai', 'Bangalore', '2025-05-01', 0.00, 60, 20, 10, 4000.00, 8000.00, 13000.00, '10:30:00', '12:15:00'),
(25, 'Mumbai', 'Chennai', '2025-05-02', 0.00, 60, 20, 10, 4200.00, 8500.00, 14000.00, '14:00:00', '16:00:00'),
(26, 'Mumbai', 'Kolkata', '2025-05-03', 0.00, 60, 20, 10, 5000.00, 10000.00, 16000.00, '07:30:00', '10:00:00'),
(27, 'Mumbai', 'Ahmedabad', '2025-05-03', 0.00, 60, 20, 10, 3000.00, 6000.00, 10000.00, '18:00:00', '19:00:00'),
(29, 'Mumbai', 'Jaipur', '2025-05-04', 0.00, 60, 20, 10, 3800.00, 7500.00, 12500.00, '12:00:00', '13:30:00'),
(30, 'Mumbai', 'Lucknow', '2025-05-05', 0.00, 60, 20, 10, 4200.00, 8500.00, 14000.00, '15:00:00', '17:00:00'),
(31, 'Mumbai', 'Goa', '2025-05-05', 0.00, 60, 20, 10, 3200.00, 6500.00, 11000.00, '16:30:00', '17:45:00'),
(32, 'Delhi', 'Mumbai', '2025-05-06', 0.00, 60, 20, 10, 4500.00, 9000.00, 15000.00, '08:00:00', '10:15:00'),
(33, 'Delhi', 'Bangalore', '2025-05-06', 0.00, 60, 20, 10, 5000.00, 10000.00, 16000.00, '11:00:00', '13:45:00'),
(34, 'Delhi', 'Hyderabad', '2025-05-07', 0.00, 60, 20, 10, 4200.00, 8500.00, 14000.00, '09:30:00', '11:45:00'),
(35, 'Delhi', 'Chennai', '2025-05-07', 0.00, 60, 20, 10, 4800.00, 9500.00, 15500.00, '14:30:00', '17:15:00'),
(36, 'Delhi', 'Kolkata', '2025-05-08', 0.00, 60, 20, 10, 3500.00, 7000.00, 12000.00, '07:00:00', '08:30:00'),
(37, 'Delhi', 'Ahmedabad', '2025-05-08', 0.00, 60, 20, 10, 3200.00, 6500.00, 11000.00, '17:30:00', '19:00:00'),
(38, 'Delhi', 'Pune', '2025-05-09', 0.00, 60, 20, 10, 4000.00, 8000.00, 13000.00, '13:00:00', '15:00:00'),
(39, 'Delhi', 'Jaipur', '2025-05-09', 0.00, 60, 20, 10, 2500.00, 5000.00, 8000.00, '18:00:00', '18:45:00'),
(40, 'Delhi', 'Lucknow', '2025-05-10', 0.00, 60, 20, 10, 2800.00, 5500.00, 9000.00, '10:00:00', '11:00:00'),
(41, 'Delhi', 'Goa', '2025-05-10', 0.00, 60, 20, 10, 5200.00, 10500.00, 17000.00, '12:30:00', '15:00:00'),
(42, 'Bangalore', 'Mumbai', '2025-05-11', 0.00, 60, 20, 10, 4000.00, 8000.00, 13000.00, '08:30:00', '10:15:00'),
(43, 'Bangalore', 'Delhi', '2025-05-11', 0.00, 60, 20, 10, 5000.00, 10000.00, 16000.00, '11:00:00', '13:45:00'),
(44, 'Bangalore', 'Hyderabad', '2025-05-12', 0.00, 60, 20, 10, 3000.00, 6000.00, 10000.00, '09:00:00', '10:15:00'),
(45, 'Bangalore', 'Chennai', '2025-05-12', 0.00, 60, 20, 10, 2500.00, 5000.00, 8000.00, '14:00:00', '15:00:00'),
(46, 'Bangalore', 'Kolkata', '2025-05-13', 0.00, 60, 20, 10, 4500.00, 9000.00, 15000.00, '07:30:00', '10:00:00'),
(47, 'Bangalore', 'Ahmedabad', '2025-05-13', 0.00, 60, 20, 10, 4200.00, 8500.00, 14000.00, '16:00:00', '18:00:00'),
(48, 'Bangalore', 'Pune', '2025-05-14', 0.00, 60, 20, 10, 2800.00, 5500.00, 9000.00, '12:00:00', '13:15:00'),
(49, 'Bangalore', 'Jaipur', '2025-05-14', 0.00, 60, 20, 10, 4800.00, 9500.00, 15500.00, '15:30:00', '18:00:00'),
(50, 'Bangalore', 'Lucknow', '2025-05-15', 0.00, 60, 20, 10, 4500.00, 9000.00, 15000.00, '10:30:00', '13:00:00'),
(51, 'Bangalore', 'Goa', '2025-05-15', 0.00, 60, 20, 10, 3200.00, 6500.00, 11000.00, '17:00:00', '18:00:00'),
(52, 'Hyderabad', 'Mumbai', '2025-05-16', 0.00, 60, 20, 10, 3500.00, 7000.00, 12000.00, '09:00:00', '10:30:00'),
(53, 'Hyderabad', 'Delhi', '2025-05-16', 0.00, 60, 20, 10, 4200.00, 8500.00, 14000.00, '11:30:00', '14:00:00'),
(54, 'Hyderabad', 'Bangalore', '2025-05-17', 0.00, 60, 20, 10, 3000.00, 6000.00, 10000.00, '08:00:00', '09:15:00'),
(55, 'Hyderabad', 'Chennai', '2025-05-17', 0.00, 60, 20, 10, 2800.00, 5500.00, 9000.00, '13:30:00', '14:45:00'),
(56, 'Hyderabad', 'Kolkata', '2025-05-18', 0.00, 60, 20, 10, 4000.00, 8000.00, 13000.00, '07:00:00', '09:30:00'),
(57, 'Hyderabad', 'Ahmedabad', '2025-05-18', 0.00, 60, 20, 10, 3500.00, 7000.00, 12000.00, '15:00:00', '16:30:00'),
(58, 'Hyderabad', 'Pune', '2025-05-19', 0.00, 60, 20, 10, 3000.00, 6000.00, 10000.00, '10:30:00', '11:45:00'),
(59, 'Hyderabad', 'Jaipur', '2025-05-19', 0.00, 60, 20, 10, 4500.00, 9000.00, 15000.00, '14:00:00', '16:30:00'),
(60, 'Hyderabad', 'Lucknow', '2025-05-20', 0.00, 60, 20, 10, 4200.00, 8500.00, 14000.00, '09:30:00', '12:00:00'),
(61, 'Hyderabad', 'Goa', '2025-05-20', 0.00, 60, 20, 10, 3800.00, 7500.00, 12500.00, '16:00:00', '17:30:00'),
(62, 'Surat', 'Mumbai', '2025-04-25', 0.00, 60, 20, 10, 4000.00, 10000.00, 7000.00, '03:30:00', '05:30:00'),
(63, 'Mumbai', 'Hyderabad', '2025-05-08', 0.00, 60, 20, 10, 8000.00, 15000.00, 12000.00, '13:00:00', '19:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `pilots`
--

CREATE TABLE `pilots` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `passenger_name` varchar(255) DEFAULT NULL,
  `age` text NOT NULL,
  `flight_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pilots`
--

INSERT INTO `pilots` (`id`, `name`, `passenger_name`, `age`, `flight_id`) VALUES
(18, 'Hiya', NULL, '22', 20);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `flight_id` (`flight_id`);

--
-- Indexes for table `crew`
--
ALTER TABLE `crew`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_crew_flights` (`flight_id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `flights`
--
ALTER TABLE `flights`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pilots`
--
ALTER TABLE `pilots`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_pilots_flights` (`flight_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `crew`
--
ALTER TABLE `crew`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `flights`
--
ALTER TABLE `flights`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `pilots`
--
ALTER TABLE `pilots`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookings_ibfk_3` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`id`),
  ADD CONSTRAINT `fk_bookings_flights` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `crew`
--
ALTER TABLE `crew`
  ADD CONSTRAINT `fk_crew_flights` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`id`);

--
-- Constraints for table `pilots`
--
ALTER TABLE `pilots`
  ADD CONSTRAINT `fk_pilots_flights` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
