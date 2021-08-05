# Generated by Django 2.1.5 on 2021-08-04 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210727_1602'),
        ('music', '0016_auto_20210803_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Album')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Profile')),
                ('songs', models.ManyToManyField(blank=True, to='music.Song')),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterUniqueTogether(
            name='libraryalbum',
            unique_together={('profile', 'album')},
        ),
    ]
