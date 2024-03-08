from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `zone` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `netbox_id` INT NOT NULL,
    `is_active` BOOL NOT NULL  DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `deleted_at` DATETIME(6),
    KEY `idx_zone_name_3b1e0e` (`name`)
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `zone`;"""
