from marshmallow import Schema, fields, validate
from models.user import User


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'image',
                  'is_verified', 'created_at', 'updated_at')

    email = fields.Email()
    phone = fields.Str(validate=validate.Regexp(r'^\+\d{1,15}$'))
    image = fields.URL(relative=False)
    created_at = fields.DateTime(format='iso')
    updated_at = fields.DateTime(format='iso')