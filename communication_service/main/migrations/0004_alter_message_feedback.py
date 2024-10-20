# Generated by Django 5.0.3 on 2024-04-20 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_language_user_remove_feedback_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='feedback',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='main.feedback'),
        ),
    ]
