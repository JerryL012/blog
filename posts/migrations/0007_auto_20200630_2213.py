# Generated by Django 3.0.3 on 2020-06-30 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_category_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='content',
        ),
        migrations.AddField(
            model_name='post',
            name='next_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='post',
            name='previous_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous', to='posts.Post'),
        ),
    ]
