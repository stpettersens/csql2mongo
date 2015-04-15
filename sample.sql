-- SQL table dump from MongoDB collection: sample (sample.json -> sample.sql)
-- Generated by: cmongo2sql 1.0.1 (https://github.com/stpettersens/cmongo2sql)
-- Generated at: 2015-04-15 18:58:38.744000

DROP TABLE IF EXISTS `sample`;
CREATE TABLE IF NOT EXISTS `sample` (
_id VARCHAR(30) NOT NULL,
name VARCHAR(50) NOT NULL,
value NUMERIC(15, 2) NOT NULL,
createdAt TIMESTAMP NOT NULL)
ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `sample` VALUES (
'552dbf77588030e5525790bd',
'Sample1',
1.55,
'2015-01-01 08:00:00'); -- 0.5

INSERT INTO `sample` VALUES (
'552dbf89588030e5525790be',
'Sample2',
1.55,
'2015-01-01 08:00:00'); -- 1

INSERT INTO `sample` VALUES (
'552dbf92588030e5525790bf',
'Sample3',
0.25,
'2015-01-01 08:00:00');

INSERT INTO `sample` VALUES (
'552dbf99588030e5525790c0',
'Sample4',
1.75,
'2015-01-01 08:00:00');

