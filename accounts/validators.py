import os

from django.core.exceptions import ValidationError


def allow_only_image_validator(value):

    extention = os.path.splitext(value.name)[1]
    valid_extentions = [".jpg", ".jpeg", ".png"]
    print(extention)
    if not extention.lower() in valid_extentions:
        raise ValidationError("unsupported file extention. Allowed ones are : " + str(valid_extentions))
