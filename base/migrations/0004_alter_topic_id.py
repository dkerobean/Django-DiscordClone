# Generated by Django 4.1.3 on 2022-11-09 20:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_message_id_alter_room_id_alter_topic_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
