# Generated by Django 5.0.3 on 2024-04-13 02:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("uesc_app", "0004_banner_grupo_link_tipo_delete_resultado_grupo_tipo"),
    ]

    operations = [
        migrations.AddField(
            model_name="grupo",
            name="data",
            field=models.DateTimeField(auto_now=True),
        ),
    ]