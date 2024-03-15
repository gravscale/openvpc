from tortoise import fields, models


class Config(models.Model):
    id = fields.UUIDField(pk=True)
    param = fields.CharField(max_length=255, index=True)
    value = fields.CharField(max_length=255)
    format = fields.CharField(max_length=10)
    scope_zone = fields.ForeignKeyField("models.Zone", null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "config"
        ordering = ["created_at"]
