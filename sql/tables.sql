CREATE TABLE `depts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(45) NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Level` int(11) NOT NULL,
  `LevelCode` varchar(2000) NOT NULL,
  `Parent_id` int(11) DEFAULT NULL,
  `Description` varchar(2000) DEFAULT NULL,
  `CreatedOn` varchar(45) DEFAULT NULL,
  `CreatedBy` varchar(45) DEFAULT NULL,
  `ModifiedOn` datetime DEFAULT NULL,
  `ModifiedBy` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`,`Code`),
  UNIQUE KEY `Code_UNIQUE` (`Code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
