# Generated by Django 5.0.5 on 2024-05-11 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_blog_password_alter_profile_date_of_registration'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
