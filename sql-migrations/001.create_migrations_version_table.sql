CREATE TABLE IF NOT EXISTS versionTable
(
  version INT(11) NOT NULL,
  PRIMARY KEY (version)
);

REPLACE INTO versionTable (version) VALUE (1);
