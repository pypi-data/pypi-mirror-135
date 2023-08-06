DROP TABLE IF EXISTS `book`;
CREATE TABLE `book` (
    `title` varchar(255) NOT NULL,
    `author` varchar(255) NOT NULL,
    `subtitle` varchar(255) DEFAULT NULL,
    `key` int NOT NULL,
    PRIMARY KEY (`title`,`author`)
);

DROP TABLE IF EXISTS `reading_log`;
CREATE TABLE `reading_log` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `reader` varchar(255) NOT NULL UNIQUE
);

DROP TABLE IF EXISTS `reading_log_entry`;
CREATE TABLE IF NOT EXISTS `reading_log_entry` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `date` date NOT NULL,
    `reader` varchar(255) NOT NULL,
    `book_title` varchar(255) NOT NULL,
    `book_author` varchar(255) NOT NULL,
    `start_page` int NOT NULL,
    `end_page` int NOT NULL,
    -- KEY `fk_book_idx` (`title`,`author`),
    -- KEY `fk_reader_idx` (`reader`),
    FOREIGN KEY (`book_title`, `book_author`) REFERENCES `book` (`title`, `author`),
    FOREIGN KEY (`reader`) REFERENCES `reading_log` (`reader`)
);