# Generated by Django 4.2.7 on 2024-01-25 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quiz_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice', to='quiz.question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='quiz/media/images/'),
        ),
    ]
