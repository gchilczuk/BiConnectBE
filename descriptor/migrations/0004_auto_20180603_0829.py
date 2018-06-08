# Generated by Django 2.0.3 on 2018-06-03 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('descriptor', '0003_auto_20180420_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='meeting',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='recommendation',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='requirement',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='speech',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='speech',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='speech',
            name='meeting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='speeches', related_query_name='speech', to='descriptor.Meeting'),
        ),
        migrations.AlterField(
            model_name='speech',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='speeches', related_query_name='speech', to='descriptor.Person'),
        ),
        migrations.AddField(
            model_name='speech',
            name='business_description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='speech', to='descriptor.BusinessDescription'),
        ),
    ]
