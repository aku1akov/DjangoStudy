# Generated by Django 4.2.7 on 2024-01-03 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_image_options_alter_article_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='news.article')),
            ],
            options={
                'verbose_name': 'Просмотр',
                'verbose_name_plural': 'Просмотры',
                'ordering': ['-date'],
                'indexes': [models.Index(fields=['-date'], name='news_viewco_date_feba56_idx')],
            },
        ),
    ]