import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_comment_content_alter_comment_date_of_creation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='is_private',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='password',
        ),
        migrations.RemoveField(
            model_name='post',
            name='visibility',
        ),
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='post',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='mainapp.post'),
        ),
    ]
