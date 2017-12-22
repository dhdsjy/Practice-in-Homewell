-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: xuwf
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dage`
--

DROP TABLE IF EXISTS `dage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dage` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dage`
--

LOCK TABLES `dage` WRITE;
/*!40000 ALTER TABLE `dage` DISABLE KEYS */;
INSERT INTO `dage` VALUES (1,'tlw');
/*!40000 ALTER TABLE `dage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_group`
--

DROP TABLE IF EXISTS `t_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_group` (
  `id` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_group`
--

LOCK TABLES `t_group` WRITE;
/*!40000 ALTER TABLE `t_group` DISABLE KEYS */;
INSERT INTO `t_group` VALUES (1,'Group0'),(2,'Group1');
/*!40000 ALTER TABLE `t_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user`
--

DROP TABLE IF EXISTS `t_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_user` (
  `id` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `groupid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `groupid` (`groupid`),
  CONSTRAINT `t_user_ibfk_1` FOREIGN KEY (`groupid`) REFERENCES `t_group` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user`
--

LOCK TABLES `t_user` WRITE;
/*!40000 ALTER TABLE `t_user` DISABLE KEYS */;
INSERT INTO `t_user` VALUES (3,'dai',2);
/*!40000 ALTER TABLE `t_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user2`
--

DROP TABLE IF EXISTS `t_user2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_user2` (
  `id` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `groupid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `groupid` (`groupid`),
  CONSTRAINT `t_user2_ibfk_1` FOREIGN KEY (`groupid`) REFERENCES `t_group` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user2`
--

LOCK TABLES `t_user2` WRITE;
/*!40000 ALTER TABLE `t_user2` DISABLE KEYS */;
INSERT INTO `t_user2` VALUES (1,'qinaxin',1),(2,'yiyi',NULL),(3,'dai',NULL);
/*!40000 ALTER TABLE `t_user2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user3`
--

DROP TABLE IF EXISTS `t_user3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_user3` (
  `id` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `groupid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `groupid` (`groupid`),
  CONSTRAINT `t_user3_ibfk_1` FOREIGN KEY (`groupid`) REFERENCES `t_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user3`
--

LOCK TABLES `t_user3` WRITE;
/*!40000 ALTER TABLE `t_user3` DISABLE KEYS */;
INSERT INTO `t_user3` VALUES (1,'qianxin',1),(2,'yiyu',2),(3,'dai',2);
/*!40000 ALTER TABLE `t_user3` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `table1`
--

DROP TABLE IF EXISTS `table1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `table1` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `name` char(20) NOT NULL,
  `sex` int(4) NOT NULL DEFAULT '0',
  `degree` double(16,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `table1`
--

LOCK TABLES `table1` WRITE;
/*!40000 ALTER TABLE `table1` DISABLE KEYS */;
INSERT INTO `table1` VALUES (2,'xxx',1,3.44),(3,'yyy',0,234.22);
/*!40000 ALTER TABLE `table1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xiaodi`
--

DROP TABLE IF EXISTS `xiaodi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xiaodi` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `dage_id` int(10) DEFAULT NULL,
  `name` varchar(20) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `dage_id` (`dage_id`),
  CONSTRAINT `fk` FOREIGN KEY (`dage_id`) REFERENCES `dage` (`id`),
  CONSTRAINT `xiaodi_ibfk_1` FOREIGN KEY (`dage_id`) REFERENCES `dage` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xiaodi`
--

LOCK TABLES `xiaodi` WRITE;
/*!40000 ALTER TABLE `xiaodi` DISABLE KEYS */;
INSERT INTO `xiaodi` VALUES (1,1,'tlw_xdA');
/*!40000 ALTER TABLE `xiaodi` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-21 15:08:37
