from tortoise import fields, models


class Credential(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255, null=True)
    private_key = fields.CharField(max_length=2048, null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        table = "credential"
        ordering = ["created_at"]
