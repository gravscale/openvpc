from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
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
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `device`;"""
