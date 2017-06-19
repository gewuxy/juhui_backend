
USE `juhui`;

/*Table structure for table `alipay_card` */

DROP TABLE IF EXISTS `account_jh_user`;

CREATE TABLE `account_jh_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL COMMENT 'Django用户',
  `nickname` varchar(40) DEFAULT NULL COMMENT '用户昵称',
  `mobile` varchar(12) DEFAULT NULL COMMENT '手机好',
  `img_url` varchar(255) DEFAULT NULL COMMENT '头像url',
  `email` varchar(64) DEFAULT NULL COMMENT '用户邮箱',
  `role` tinyint(1) DEFAULT NULL COMMENT '用户角色（0:普通，1:管理员）',
  `is_delete` tinyint(1) DEFAULT NULL COMMENT '是否无效用户',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user`) REFERENCES `auth_user` (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
 
