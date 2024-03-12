from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
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
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `config`;"""
