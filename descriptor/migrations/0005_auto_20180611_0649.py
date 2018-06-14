# Generated by Django 2.0.3 on 2018-06-11 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('descriptor', '0004_auto_20180603_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speech',
            name='meeting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='speeches', related_query_name='speech', to='descriptor.Meeting'),
        ),
        migrations.AlterField(
            model_name='speech',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='speeches', related_query_name='speech', to='descriptor.Person'),
        ),
    ]