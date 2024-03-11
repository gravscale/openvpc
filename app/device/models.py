from tortoise import fields, models


class Device(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    device_type = fields.CharField(max_length=255)
    host = fields.CharField(max_length=255)
    port = fields.IntField()
    protocol = fields.CharField(max_length=50)
    netbox_id = fields.IntField()
    zone = fields.ForeignKeyField("models.Zone", related_name="devices")
    credential = fields.ForeignKeyField("models.Credential", null=True, related_name="devices")
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        table = "device"
        ordering = ["created_at"]
