# Generated by Django 5.0.4 on 2024-04-25 16:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("uesc_app", "0005_grupo_data"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Banner",
        ),
        migrations.AlterField(
            model_name="link",
            name="nome",
            field=models.TextField(null=True),
        ),
    ]