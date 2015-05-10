-- Database
CREATE DATABASE `example`;
USE `example`;

-- Table structure for table `users`
CREATE TABLE `users` (
 `id` INT(8) UNSIGNED NOT NULL AUTO_INCREMENT,
 `username` VARCHAR(16) NOT NULL,
 `password` VARCHAR(16) NOT NULL,
 PRIMARY KEY (`id`)
);

-- Data for table `users`
INSERT INTO `users` VALUES (1, 'alice','secret');
INSERT INTO `users` VALUES (2, 'bob','secret');
INSERT INTO `users` VALUES (3, 'jeff', 'secret')
INSERT INTO `users` VALUES (4, 'dan', 'secret');

