# Generated by Django 3.1.4 on 2023-02-25 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0020_auto_20230225_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='category',
            field=models.ForeignKey(blank=True, default=4, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_cat', to='leads.category'),
        ),
    ]
