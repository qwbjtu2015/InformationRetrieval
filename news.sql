/*
Navicat MySQL Data Transfer

Source Server         : qinwei
Source Server Version : 50719
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2017-12-27 00:21:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `news`
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `news_id` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  `content` text,
  `release_time` varchar(255) DEFAULT NULL,
  `keyword` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `join_num` int(11) DEFAULT NULL,
  `comment_num` int(11) DEFAULT NULL,
  `news_url` varchar(255) DEFAULT NULL,
  `comment_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_unique` (`news_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6030 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of news
-- ----------------------------
