# Generated by Django 5.1.2 on 2024-10-24 16:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="is_blocked",
        ),
        migrations.RemoveField(
            model_name="post",
            name="is_blocked",
        ),
        migrations.AddField(
            model_name="comment",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approved", "Approved"),
                    ("blocked", "Blocked"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approved", "Approved"),
                    ("blocked", "Blocked"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
