from tortoise import fields, models


class Zone(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    netbox_id = fields.IntField()
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        table = "zone"
        ordering = ["created_at"]
