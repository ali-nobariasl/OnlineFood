# Generated by Django 4.1.2 on 2023-01-10 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0003_alter_fooditem_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="category_name",
            field=models.CharField(max_length=50),
        ),
    ]
