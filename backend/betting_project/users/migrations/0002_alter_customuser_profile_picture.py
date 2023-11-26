# Generated by Django 4.2.3 on 2023-10-27 16:35

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="profile_picture",
            field=models.FileField(
                blank=True,
                default=users.models.default_icon_image,
                null=True,
                upload_to=users.models.profile_picture_upload_path,
            ),
        ),
    ]