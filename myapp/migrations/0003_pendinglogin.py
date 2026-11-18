from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_pendingsignup'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('otp_hash', models.CharField(max_length=128)),
                ('expires_at', models.DateTimeField()),
                ('attempts', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
