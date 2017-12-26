/*
Navicat MySQL Data Transfer

Source Server         : qinwei
Source Server Version : 50719
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2017-12-27 00:21:42
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `comments`
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `comment_id` varchar(255) NOT NULL,
  `news_id` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `create_time` varchar(255) DEFAULT NULL,
  `vote_num` int(11) DEFAULT NULL,
  `against_num` int(11) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `user_location` varchar(255) DEFAULT NULL,
  `user_nickname` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_unique` (`comment_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=178031 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comments
-- ----------------------------
