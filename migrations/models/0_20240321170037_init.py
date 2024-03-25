from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `zone` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `netbox_id` INT NOT NULL,
    `is_active` BOOL NOT NULL  DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `deleted_at` DATETIME(6),
    KEY `idx_zone_name_3b1e0e` (`name`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `credential` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `username` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255),
    `private_key` VARCHAR(2048),
    `is_active` BOOL NOT NULL  DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `deleted_at` DATETIME(6),
    KEY `idx_credential_name_52b323` (`name`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `device` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `device_type` VARCHAR(255) NOT NULL,
    `host` VARCHAR(255) NOT NULL,
    `port` INT NOT NULL,
    `protocol` VARCHAR(50) NOT NULL,
    `netbox_id` INT NOT NULL,
    `is_active` BOOL NOT NULL  DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `deleted_at` DATETIME(6),
    `credential_id` CHAR(36),
    `zone_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_device_credenti_b6c5c6aa` FOREIGN KEY (`credential_id`) REFERENCES `credential` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_device_zone_9081df83` FOREIGN KEY (`zone_id`) REFERENCES `zone` (`id`) ON DELETE CASCADE,
    KEY `idx_device_name_d43932` (`name`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `config` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `param` VARCHAR(255) NOT NULL,
    `value` VARCHAR(255) NOT NULL,
    `format` VARCHAR(10) NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `scope_zone_id` CHAR(36),
    CONSTRAINT `fk_config_zone_7e326ff8` FOREIGN KEY (`scope_zone_id`) REFERENCES `zone` (`id`) ON DELETE CASCADE,
    KEY `idx_config_param_3632ce` (`param`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `vpc` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `primary_device_name` VARCHAR(255) NOT NULL,
    `secondary_device_name` VARCHAR(255) NOT NULL,
    `is_active` BOOL NOT NULL  DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `deleted_at` DATETIME(6),
    KEY `idx_vpc_name_3869b0` (`name`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `router` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `is_active` BOOL NOT NULL  DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `deleted_at` DATETIME(6),
    `vpc_id` CHAR(36),
    CONSTRAINT `fk_router_vpc_8a30376f` FOREIGN KEY (`vpc_id`) REFERENCES `vpc` (`id`) ON DELETE CASCADE,
    KEY `idx_router_name_4eef41` (`name`)
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
