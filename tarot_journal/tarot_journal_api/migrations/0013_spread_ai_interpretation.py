from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarot_journal_api', '0012_card_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='spread',
            name='ai_interpretation',
            field=models.TextField(blank=True, default=''),
        ),
    ]
