-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 06, 2026 at 11:50 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `database_eatogo`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`admin_id`, `username`, `password`) VALUES
(1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9');

-- --------------------------------------------------------

--
-- Table structure for table `menu_items`
--

CREATE TABLE `menu_items` (
  `menu_id` int(11) NOT NULL,
  `category` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int(11) DEFAULT 0,
  `image_path` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_available` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`menu_id`, `category`, `name`, `price`, `stock`, `image_path`, `created_at`, `is_available`) VALUES
(2, 'Burgers', 'cheesy burger', 55.00, 91, 'C:/Users/keith baslan/Downloads/Cheesy Burger.jpg', '2026-01-22 15:23:00', 1),
(3, 'Burgers', 'creamy cheese bacon burger', 60.00, 96, 'C:/Users/keith baslan/Downloads/Just Wanted Bacon on My Burger.jpg', '2026-01-28 16:04:04', 1),
(4, 'Pizza', 'peperoni', 450.00, 50, 'C:/Users/keith baslan/Downloads/Must Try Pepperoni Pizza.jpg', '2026-01-28 16:05:54', 1),
(5, 'Pizza', 'Hawaian Pizza', 450.00, 22, 'C:/Users/keith baslan/Downloads/Pineapple Pizza Recipe (Hawaiian Pizza).jpg', '2026-01-28 16:09:43', 1),
(6, 'Drinks', 'Apple soda', 75.00, 48, 'C:/Users/keith baslan/Downloads/Sex on the Beach_ Um Clássico entre os Coquetéis Refrescantes.jpg', '2026-01-28 16:10:42', 1),
(7, 'Drinks', 'Strawberry Smoothie', 120.00, 20, 'C:/Users/keith baslan/Downloads/Strawberry Banana Smoothie (+ Easy Recipe).jpg', '2026-01-28 16:11:37', 1),
(8, 'Drinks', 'Caramel Milk Tea', 85.00, 23, 'C:/Users/keith baslan/Downloads/Boba Tea Pearls Recipe_ Craft Chewy Tapioca Pearls at Home.jpg', '2026-01-28 16:13:15', 1),
(9, 'Meals', 'Kimbap(korean Rice rolls)', 100.00, 15, 'C:/Users/keith baslan/Downloads/Kimbap (Korean Seaweed Rice Rolls) - EricTriesIt.jpg', '2026-01-28 16:14:25', 1),
(10, 'Meals', 'Meatballs pasta', 150.00, 27, 'C:/Users/keith baslan/Downloads/download (1).jpg', '2026-01-28 16:15:16', 1),
(11, 'Drinks', 'Cola', 25.00, 50, 'C:/Users/keith baslan/Downloads/Coca-Cola spends millions on research to counter obesity link claims.jpg', '2026-03-06 08:08:39', 1);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `status` enum('Pending','Processing','Completed','Cancelled') DEFAULT 'Pending',
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `delivery_address` text DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT 'Cash on Delivery'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `user_id`, `total_amount`, `status`, `order_date`, `delivery_address`, `payment_method`) VALUES
(1, 2, 160.00, 'Completed', '2026-01-22 15:24:32', 'barangy 23-c', 'Cash on Delivery'),
(2, 3, 105.00, 'Completed', '2026-01-23 08:42:20', 'um matina', 'Cash on Delivery'),
(3, 3, 105.00, 'Completed', '2026-01-23 08:53:55', 'um matina', 'Bank Transfer'),
(4, 1, 490.00, 'Completed', '2025-01-05 02:30:00', '123 Main St, Manila', 'Cash on Delivery'),
(5, 2, 620.00, 'Completed', '2025-01-05 03:15:00', '456 Elm St, Quezon City', 'Cash on Delivery'),
(6, 3, 370.00, 'Completed', '2025-01-05 06:20:00', '789 Oak Ave, Makati', 'Cash on Delivery'),
(7, 4, 800.00, 'Completed', '2025-01-06 01:45:00', '321 Pine Rd, Pasig', 'Cash on Delivery'),
(8, 5, 550.00, 'Completed', '2025-01-06 04:30:00', '654 Maple Dr, Taguig', 'Bank Transfer'),
(9, 6, 430.00, 'Completed', '2025-01-06 07:10:00', '987 Cedar Ln, Mandaluyong', 'Cash on Delivery'),
(10, 7, 680.00, 'Completed', '2025-01-07 02:00:00', '147 Birch St, Pasay', 'Cash on Delivery'),
(11, 8, 520.00, 'Completed', '2025-01-07 05:45:00', '258 Willow Ave, Para?aque', 'Cash on Delivery'),
(12, 9, 740.00, 'Completed', '2025-01-07 08:30:00', '369 Ash Rd, Las Pi?as', 'Cash on Delivery'),
(13, 10, 390.00, 'Completed', '2025-01-08 03:20:00', '741 Spruce Dr, Muntinlupa', 'Cash on Delivery'),
(14, 11, 610.00, 'Completed', '2025-01-08 06:00:00', '852 Poplar Ln, Valenzuela', 'Cash on Delivery'),
(15, 12, 470.00, 'Completed', '2025-01-08 09:15:00', '963 Hickory St, Caloocan', 'Cash on Delivery'),
(16, 13, 580.00, 'Completed', '2025-01-09 02:30:00', '159 Walnut Ave, Malabon', 'Cash on Delivery'),
(17, 14, 650.00, 'Completed', '2025-01-09 04:45:00', '267 Chestnut Rd, Navotas', 'Cash on Delivery'),
(18, 15, 410.00, 'Completed', '2025-01-09 07:30:00', '378 Sycamore Dr, San Juan', 'Bank Transfer'),
(19, 16, 720.00, 'Completed', '2025-01-12 01:30:00', '489 Magnolia Ln, Marikina', 'Cash on Delivery'),
(20, 17, 540.00, 'Completed', '2025-01-12 03:45:00', '591 Dogwood St, Pateros', 'Bank Transfer'),
(21, 18, 830.00, 'Completed', '2025-01-12 06:20:00', '612 Redwood Ave, Manila', 'Cash on Delivery'),
(22, 19, 460.00, 'Completed', '2025-01-13 02:15:00', '723 Fir Rd, Quezon City', 'Bank Transfer'),
(23, 20, 590.00, 'Completed', '2025-01-13 05:00:00', '834 Beech Dr, Makati', 'Cash on Delivery'),
(24, 21, 710.00, 'Completed', '2025-01-13 08:45:00', '945 Hemlock Ln, Pasig', 'Bank Transfer'),
(25, 22, 380.00, 'Completed', '2025-01-14 03:30:00', '156 Juniper St, Taguig', 'Cash on Delivery'),
(26, 23, 620.00, 'Completed', '2025-01-14 06:15:00', '267 Cypress Ave, Mandaluyong', 'Cash on Delivery'),
(27, 24, 750.00, 'Completed', '2025-01-14 09:00:00', '378 Alder Rd, Pasay', 'Cash on Delivery'),
(28, 25, 490.00, 'Completed', '2025-01-15 02:20:00', '489 Sequoia Dr, Para?aque', 'Cash on Delivery'),
(29, 26, 560.00, 'Completed', '2025-01-15 05:30:00', '591 Mahogany Ln, Las Pi?as', 'Cash on Delivery'),
(30, 27, 640.00, 'Completed', '2025-01-15 08:10:00', '612 Acacia St, Muntinlupa', 'Cash on Delivery'),
(31, 28, 420.00, 'Completed', '2025-01-16 01:45:00', '723 Bamboo Ave, Valenzuela', 'Cash on Delivery'),
(32, 29, 780.00, 'Completed', '2025-01-16 04:20:00', '834 Palm Rd, Caloocan', 'Bank Transfer'),
(33, 30, 510.00, 'Completed', '2025-01-16 07:40:00', '945 Coconut Dr, Malabon', 'Cash on Delivery'),
(34, 31, 670.00, 'Completed', '2025-01-19 02:00:00', '156 Mango Ln, Navotas', 'Cash on Delivery'),
(35, 32, 530.00, 'Completed', '2025-01-19 05:15:00', '267 Banana St, San Juan', 'Cash on Delivery'),
(36, 33, 810.00, 'Completed', '2025-01-19 08:30:00', '378 Papaya Ave, Marikina', 'Cash on Delivery'),
(37, 34, 440.00, 'Completed', '2025-01-20 03:10:00', '489 Guava Rd, Pateros', 'Cash on Delivery'),
(38, 35, 600.00, 'Completed', '2025-01-20 06:00:00', '591 Orange Dr, Manila', 'Bank Transfer'),
(39, 36, 690.00, 'Completed', '2025-01-20 09:20:00', '612 Lemon Ln, Quezon City', 'Cash on Delivery'),
(40, 37, 370.00, 'Completed', '2025-01-21 02:30:00', '723 Lime St, Makati', 'Bank Transfer'),
(41, 38, 730.00, 'Completed', '2025-01-21 05:45:00', '834 Peach Ave, Pasig', 'Cash on Delivery'),
(42, 39, 580.00, 'Completed', '2025-01-21 08:50:00', '945 Plum Rd, Taguig', 'Bank Transfer'),
(43, 40, 450.00, 'Completed', '2025-01-22 01:20:00', '156 Cherry Dr, Mandaluyong', 'Cash on Delivery'),
(44, 41, 770.00, 'Completed', '2025-01-22 04:35:00', '267 Apple Ln, Pasay', 'Bank Transfer'),
(45, 42, 520.00, 'Completed', '2025-01-22 07:15:00', '378 Pear St, Para?aque', 'Cash on Delivery'),
(46, 43, 630.00, 'Completed', '2025-01-23 02:40:00', '489 Grape Ave, Las Pi?as', 'Bank Transfer'),
(47, 44, 410.00, 'Completed', '2025-01-23 05:50:00', '591 Berry Rd, Muntinlupa', 'Cash on Delivery'),
(48, 45, 790.00, 'Completed', '2025-01-23 08:25:00', '612 Melon Dr, Valenzuela', 'Bank Transfer'),
(49, 46, 540.00, 'Completed', '2025-01-26 02:15:00', '723 Kiwi Ln, Caloocan', 'Cash on Delivery'),
(50, 47, 660.00, 'Completed', '2025-01-26 05:30:00', '834 Fig St, Malabon', 'Cash on Delivery'),
(51, 48, 480.00, 'Completed', '2025-01-26 08:00:00', '945 Date Ave, Navotas', 'Cash on Delivery'),
(52, 49, 720.00, 'Completed', '2025-01-27 01:45:00', '156 Apricot Rd, San Juan', 'Bank Transfer'),
(53, 50, 390.00, 'Completed', '2025-01-27 04:20:00', '267 Pomegranate Dr, Marikina', 'Cash on Delivery'),
(54, 1, 820.00, 'Completed', '2025-01-27 07:10:00', '123 Main St, Manila', 'Bank Transfer'),
(55, 2, 570.00, 'Completed', '2025-01-28 02:00:00', '456 Elm St, Quezon City', 'Cash on Delivery'),
(56, 3, 640.00, 'Completed', '2025-01-28 03:30:00', '789 Oak Ave, Makati', 'Bank Transfer'),
(57, 4, 460.00, 'Processing', '2025-01-28 05:00:00', '321 Pine Rd, Pasig', 'Cash on Delivery'),
(58, 5, 750.00, 'Pending', '2025-01-28 06:30:00', '654 Maple Dr, Taguig', 'Bank Transfer'),
(59, 6, 530.00, 'Completed', '2024-12-05 02:30:00', '987 Cedar Ln, Mandaluyong', 'Cash on Delivery'),
(60, 7, 690.00, 'Completed', '2024-12-08 05:15:00', '147 Birch St, Pasay', 'Cash on Delivery'),
(61, 8, 410.00, 'Completed', '2024-12-10 03:45:00', '258 Willow Ave, Para?aque', 'Cash on Delivery'),
(62, 9, 780.00, 'Completed', '2024-12-12 06:30:00', '369 Ash Rd, Las Pi?as', 'Bank Transfer'),
(63, 10, 620.00, 'Completed', '2024-12-15 02:00:00', '741 Spruce Dr, Muntinlupa', 'Cash on Delivery'),
(64, 11, 540.00, 'Completed', '2024-12-18 04:45:00', '852 Poplar Ln, Valenzuela', 'Bank Transfer'),
(65, 12, 710.00, 'Completed', '2024-12-20 07:20:00', '963 Hickory St, Caloocan', 'Cash on Delivery'),
(66, 13, 480.00, 'Completed', '2024-12-22 03:30:00', '159 Walnut Ave, Malabon', 'Cash on Delivery'),
(67, 14, 820.00, 'Completed', '2024-12-24 05:00:00', '267 Chestnut Rd, Navotas', 'Cash on Delivery'),
(68, 15, 590.00, 'Completed', '2024-12-26 08:15:00', '378 Sycamore Dr, San Juan', 'Cash on Delivery'),
(69, 16, 670.00, 'Completed', '2024-11-05 02:20:00', '489 Magnolia Ln, Marikina', 'Cash on Delivery'),
(70, 17, 430.00, 'Completed', '2024-11-08 05:40:00', '591 Dogwood St, Pateros', 'Bank Transfer'),
(71, 18, 760.00, 'Completed', '2024-11-10 03:15:00', '612 Redwood Ave, Manila', 'Cash on Delivery'),
(72, 19, 520.00, 'Completed', '2024-11-12 06:50:00', '723 Fir Rd, Quezon City', 'Bank Transfer'),
(73, 20, 640.00, 'Completed', '2024-11-15 02:35:00', '834 Beech Dr, Makati', 'Cash on Delivery'),
(74, 21, 390.00, 'Completed', '2024-11-18 04:20:00', '945 Hemlock Ln, Pasig', 'Bank Transfer'),
(75, 22, 730.00, 'Completed', '2024-11-20 07:40:00', '156 Juniper St, Taguig', 'Cash on Delivery'),
(76, 23, 580.00, 'Completed', '2024-11-22 03:00:00', '267 Cypress Ave, Mandaluyong', 'Bank Transfer'),
(77, 24, 810.00, 'Completed', '2024-11-24 05:30:00', '378 Alder Rd, Pasay', 'Cash on Delivery'),
(78, 25, 470.00, 'Completed', '2024-11-26 08:10:00', '489 Sequoia Dr, Para?aque', 'Cash on Delivery'),
(79, 26, 690.00, 'Completed', '2024-10-05 02:45:00', '591 Mahogany Ln, Las Pi?as', 'Cash on Delivery'),
(80, 27, 540.00, 'Completed', '2024-10-08 05:20:00', '612 Acacia St, Muntinlupa', 'Cash on Delivery'),
(81, 28, 620.00, 'Completed', '2024-10-10 03:50:00', '723 Bamboo Ave, Valenzuela', 'Cash on Delivery'),
(82, 29, 450.00, 'Completed', '2024-10-12 06:15:00', '834 Palm Rd, Caloocan', 'Bank Transfer'),
(83, 30, 780.00, 'Completed', '2024-10-15 02:30:00', '945 Coconut Dr, Malabon', 'Cash on Delivery'),
(84, 31, 610.00, 'Completed', '2024-10-18 04:40:00', '156 Mango Ln, Navotas', 'Bank Transfer'),
(85, 32, 490.00, 'Completed', '2024-10-20 07:25:00', '267 Banana St, San Juan', 'Cash on Delivery'),
(86, 33, 740.00, 'Completed', '2024-10-22 03:10:00', '378 Papaya Ave, Marikina', 'Bank Transfer'),
(87, 34, 570.00, 'Completed', '2024-10-24 05:55:00', '489 Guava Rd, Pateros', 'Cash on Delivery'),
(88, 35, 830.00, 'Completed', '2024-10-26 08:30:00', '591 Orange Dr, Manila', 'Cash on Delivery'),
(89, 57, 280.00, 'Completed', '2026-01-28 16:17:00', 'Davao city', 'Cash on Delivery'),
(90, 59, 750.00, 'Completed', '2026-02-04 08:36:18', 'Davao City', 'Cash on Delivery'),
(91, 58, 265.00, 'Completed', '2026-02-04 08:36:48', 'Davao city', 'Cash on Delivery'),
(92, 60, 345.00, 'Completed', '2026-02-10 02:17:47', 'matina', 'Cash on Delivery'),
(93, 61, 630.00, 'Completed', '2026-02-10 02:20:14', 'Magsaysay', 'Cash on Delivery'),
(94, 62, 360.00, 'Completed', '2026-02-11 09:49:46', 'Barangy 21-c', 'Cash on Delivery'),
(95, 63, 190.00, 'Completed', '2026-02-25 06:16:06', 'Davao City', 'Cash on Delivery'),
(96, 64, 165.00, 'Completed', '2026-03-02 08:33:38', 'SA SA', 'Cash on Delivery'),
(97, 65, 500.00, 'Completed', '2026-03-04 06:36:46', 'maa', 'Cash on Delivery'),
(98, 66, 150.00, 'Completed', '2026-03-06 08:06:54', 'davao city', 'Cash on Delivery');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `order_item_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`order_item_id`, `order_id`, `menu_id`, `quantity`, `price`) VALUES
(1, 1, 2, 2, 55.00),
(2, 2, 2, 1, 55.00),
(3, 3, 2, 1, 55.00),
(4, 89, 6, 1, 75.00),
(5, 89, 2, 1, 55.00),
(6, 89, 9, 1, 100.00),
(8, 90, 9, 1, 100.00),
(9, 90, 10, 1, 150.00),
(10, 90, 5, 1, 450.00),
(11, 91, 2, 1, 55.00),
(12, 91, 3, 1, 60.00),
(13, 91, 9, 1, 100.00),
(14, 92, 8, 1, 85.00),
(15, 92, 10, 1, 150.00),
(16, 92, 3, 1, 60.00),
(17, 93, 2, 1, 55.00),
(18, 93, 6, 1, 75.00),
(19, 93, 5, 1, 450.00),
(20, 94, 9, 1, 100.00),
(21, 94, 10, 1, 150.00),
(22, 94, 3, 1, 60.00),
(23, 95, 8, 1, 85.00),
(24, 95, 2, 1, 55.00),
(25, 96, 2, 1, 55.00),
(26, 96, 3, 1, 60.00),
(27, 97, 5, 1, 450.00),
(28, 98, 9, 1, 100.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password`, `full_name`, `phone`, `address`, `created_at`, `is_active`) VALUES
(1, 'ren', 'ren@gmail.com', 'c627f6395ef52734847b2a6ad5c0ebaed34062f2871401f27df250c29ef3217a', NULL, NULL, NULL, '2026-01-21 06:36:17', 1),
(2, 'rever', 'rever@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'rever lacia', '09122653212', 'barangy 23-c', '2026-01-22 15:19:54', 1),
(3, 'yutee', 'yutee@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'christina yutee', '091233654', 'um matina', '2026-01-23 08:40:58', 1),
(4, 'veronica', 'veronica@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', NULL, NULL, NULL, '2026-01-23 10:55:45', 1),
(5, 'jul', 'jul@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', NULL, NULL, NULL, '2026-01-27 02:10:19', 1),
(6, 'keith', 'keith@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', NULL, NULL, NULL, '2026-01-28 15:07:04', 1),
(7, 'john_doe', 'john.doe@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'John Doe', '09171234567', '123 Main St, Manila', '2026-01-28 15:31:46', 1),
(8, 'jane_smith', 'jane.smith@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Jane Smith', '09181234568', '456 Elm St, Quezon City', '2026-01-28 15:31:46', 1),
(9, 'bob_johnson', 'bob.johnson@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Bob Johnson', '09191234569', '789 Oak Ave, Makati', '2026-01-28 15:31:46', 1),
(10, 'alice_williams', 'alice.williams@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Alice Williams', '09201234570', '321 Pine Rd, Pasig', '2026-01-28 15:31:46', 1),
(11, 'charlie_brown', 'charlie.brown@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Charlie Brown', '09211234571', '654 Maple Dr, Taguig', '2026-01-28 15:31:46', 1),
(12, 'diana_prince', 'diana.prince@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Diana Prince', '09221234572', '987 Cedar Ln, Mandaluyong', '2026-01-28 15:31:46', 1),
(13, 'edward_stark', 'edward.stark@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Edward Stark', '09231234573', '147 Birch St, Pasay', '2026-01-28 15:31:46', 1),
(14, 'fiona_gallagher', 'fiona.gallagher@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Fiona Gallagher', '09241234574', '258 Willow Ave, Para?aque', '2026-01-28 15:31:46', 1),
(15, 'george_martin', 'george.martin@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'George Martin', '09251234575', '369 Ash Rd, Las Pi?as', '2026-01-28 15:31:46', 1),
(16, 'hannah_montana', 'hannah.montana@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Hannah Montana', '09261234576', '741 Spruce Dr, Muntinlupa', '2026-01-28 15:31:46', 1),
(17, 'ian_somerhalder', 'ian.somerhalder@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Ian Somerhalder', '09271234577', '852 Poplar Ln, Valenzuela', '2026-01-28 15:31:46', 1),
(18, 'julia_roberts', 'julia.roberts@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Julia Roberts', '09281234578', '963 Hickory St, Caloocan', '2026-01-28 15:31:46', 1),
(19, 'kevin_hart', 'kevin.hart@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Kevin Hart', '09291234579', '159 Walnut Ave, Malabon', '2026-01-28 15:31:46', 1),
(20, 'laura_croft', 'laura.croft@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Laura Croft', '09301234580', '267 Chestnut Rd, Navotas', '2026-01-28 15:31:46', 1),
(21, 'michael_scott', 'michael.scott@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Michael Scott', '09311234581', '378 Sycamore Dr, San Juan', '2026-01-28 15:31:46', 1),
(22, 'nancy_drew', 'nancy.drew@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Nancy Drew', '09321234582', '489 Magnolia Ln, Marikina', '2026-01-28 15:31:46', 1),
(23, 'oliver_twist', 'oliver.twist@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Oliver Twist', '09331234583', '591 Dogwood St, Pateros', '2026-01-28 15:31:46', 1),
(24, 'patricia_jones', 'patricia.jones@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Patricia Jones', '09341234584', '612 Redwood Ave, Manila', '2026-01-28 15:31:46', 1),
(25, 'quincy_adams', 'quincy.adams@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Quincy Adams', '09351234585', '723 Fir Rd, Quezon City', '2026-01-28 15:31:46', 1),
(26, 'rachel_green', 'rachel.green@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Rachel Green', '09361234586', '834 Beech Dr, Makati', '2026-01-28 15:31:46', 1),
(27, 'samuel_jackson', 'samuel.jackson@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Samuel Jackson', '09371234587', '945 Hemlock Ln, Pasig', '2026-01-28 15:31:46', 1),
(28, 'tina_fey', 'tina.fey@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Tina Fey', '09381234588', '156 Juniper St, Taguig', '2026-01-28 15:31:46', 1),
(29, 'ursula_burns', 'ursula.burns@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Ursula Burns', '09391234589', '267 Cypress Ave, Mandaluyong', '2026-01-28 15:31:46', 1),
(30, 'victor_hugo', 'victor.hugo@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Victor Hugo', '09401234590', '378 Alder Rd, Pasay', '2026-01-28 15:31:46', 1),
(31, 'wendy_williams', 'wendy.williams@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Wendy Williams', '09411234591', '489 Sequoia Dr, Para?aque', '2026-01-28 15:31:46', 1),
(32, 'xavier_woods', 'xavier.woods@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Xavier Woods', '09421234592', '591 Mahogany Ln, Las Pi?as', '2026-01-28 15:31:46', 1),
(33, 'yolanda_king', 'yolanda.king@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Yolanda King', '09431234593', '612 Acacia St, Muntinlupa', '2026-01-28 15:31:46', 1),
(34, 'zachary_smith', 'zachary.smith@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Zachary Smith', '09441234594', '723 Bamboo Ave, Valenzuela', '2026-01-28 15:31:46', 1),
(35, 'amy_adams', 'amy.adams@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Amy Adams', '09451234595', '834 Palm Rd, Caloocan', '2026-01-28 15:31:46', 1),
(36, 'brian_cox', 'brian.cox@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Brian Cox', '09461234596', '945 Coconut Dr, Malabon', '2026-01-28 15:31:46', 1),
(37, 'cathy_lee', 'cathy.lee@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Cathy Lee', '09471234597', '156 Mango Ln, Navotas', '2026-01-28 15:31:46', 1),
(38, 'david_bowie', 'david.bowie@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'David Bowie', '09481234598', '267 Banana St, San Juan', '2026-01-28 15:31:46', 1),
(39, 'emma_stone', 'emma.stone@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Emma Stone', '09491234599', '378 Papaya Ave, Marikina', '2026-01-28 15:31:46', 1),
(40, 'frank_ocean', 'frank.ocean@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Frank Ocean', '09501234600', '489 Guava Rd, Pateros', '2026-01-28 15:31:46', 1),
(41, 'grace_kelly', 'grace.kelly@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Grace Kelly', '09511234601', '591 Orange Dr, Manila', '2026-01-28 15:31:46', 1),
(42, 'henry_cavill', 'henry.cavill@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Henry Cavill', '09521234602', '612 Lemon Ln, Quezon City', '2026-01-28 15:31:46', 1),
(43, 'iris_west', 'iris.west@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Iris West', '09531234603', '723 Lime St, Makati', '2026-01-28 15:31:46', 1),
(44, 'jack_sparrow', 'jack.sparrow@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Jack Sparrow', '09541234604', '834 Peach Ave, Pasig', '2026-01-28 15:31:46', 1),
(45, 'kelly_clarkson', 'kelly.clarkson@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Kelly Clarkson', '09551234605', '945 Plum Rd, Taguig', '2026-01-28 15:31:46', 1),
(46, 'luke_skywalker', 'luke.skywalker@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Luke Skywalker', '09561234606', '156 Cherry Dr, Mandaluyong', '2026-01-28 15:31:46', 1),
(47, 'mary_jane', 'mary.jane@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Mary Jane', '09571234607', '267 Apple Ln, Pasay', '2026-01-28 15:31:46', 1),
(48, 'nathan_drake', 'nathan.drake@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Nathan Drake', '09581234608', '378 Pear St, Para?aque', '2026-01-28 15:31:46', 1),
(49, 'ophelia_white', 'ophelia.white@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Ophelia White', '09591234609', '489 Grape Ave, Las Pi?as', '2026-01-28 15:31:46', 1),
(50, 'peter_parker', 'peter.parker@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Peter Parker', '09601234610', '591 Berry Rd, Muntinlupa', '2026-01-28 15:31:46', 1),
(51, 'queen_elizabeth', 'queen.elizabeth@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Queen Elizabeth', '09611234611', '612 Melon Dr, Valenzuela', '2026-01-28 15:31:46', 1),
(52, 'robert_downey', 'robert.downey@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Robert Downey', '09621234612', '723 Kiwi Ln, Caloocan', '2026-01-28 15:31:46', 1),
(53, 'sarah_connor', 'sarah.connor@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Sarah Connor', '09631234613', '834 Fig St, Malabon', '2026-01-28 15:31:46', 1),
(54, 'tony_stark', 'tony.stark@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Tony Stark', '09641234614', '945 Date Ave, Navotas', '2026-01-28 15:31:46', 1),
(55, 'uma_thurman', 'uma.thurman@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Uma Thurman', '09651234615', '156 Apricot Rd, San Juan', '2026-01-28 15:31:46', 1),
(56, 'vince_vaughn', 'vince.vaughn@email.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Vince Vaughn', '09661234616', '267 Pomegranate Dr, Marikina', '2026-01-28 15:31:46', 1),
(57, 'leo', 'leo@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'leo keith', '09111256634', 'Davao city', '2026-01-28 16:15:43', 1),
(58, 'don', 'don@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'don baslan', '09123456738', 'Davao city', '2026-02-04 08:34:06', 1),
(59, 'clark', 'clark@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'clark somson', '09123683719', 'Davao City', '2026-02-04 08:35:19', 1),
(60, 'lex', 'lex@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'lex keith', '09872537123', 'matina', '2026-02-10 02:16:45', 1),
(61, 'king', 'king@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'king', '09234679850', 'Magsaysay', '2026-02-10 02:19:10', 1),
(62, 'jake', 'jake@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'jake band', '09872345682', 'Barangy 21-c', '2026-02-11 09:48:18', 1),
(63, 'kenneth', 'kenneth@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'kenneth john', '09222565532', 'Davao City', '2026-02-25 06:15:11', 1),
(64, 'palor', 'palor@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'palor', '0912235564', 'SA SA', '2026-03-02 08:32:55', 1),
(65, 'jamm', 'jamm@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'jamm santi', '0912361616', 'maa', '2026-03-04 06:34:11', 1),
(66, 'keith123', 'keith123@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'keith baslan', '091255445', 'davao city', '2026-03-06 08:05:28', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`menu_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`order_item_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `menu_id` (`menu_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `menu_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `order_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `menu_items` (`menu_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
