# Generated by Django 2.2 on 2020-08-21 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enterprises', '0001_initial'),
        ('images', '0003_snekachievementimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='enterpriseformsubmission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enterpriseformpage',
            name='enterprise',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_page', to='enterprises.Enterprise'),
        ),
        migrations.AddField(
            model_name='enterpriseformpage',
            name='listing_image',
            field=models.ForeignKey(blank=True, help_text='Choose the image you wish to be displayed when this page appears in listings', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.SNEKImage'),
        ),
        migrations.AddField(
            model_name='enterpriseformpage',
            name='social_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.SNEKImage'),
        ),
        migrations.AddField(
            model_name='enterpriseformfield',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='enterprises.EnterpriseFormPage'),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='user',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contributor',
            name='codelanguages',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='contributor_codelanguages', to='enterprises.CodeLanguageStatistic'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='codetransition',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='contributor_codetransition', to='enterprises.CodeTransitionStatistic'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='contribution_feed',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='contributor_feed', to='enterprises.ContributionFeed'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='page',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enterprise_contributors', to='enterprises.EnterpriseFormPage'),
        ),
        migrations.AddField(
            model_name='contributionfile',
            name='feed',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_contribution_feed', to='enterprises.ContributionFeed'),
        ),
        migrations.AddField(
            model_name='contributionfeed',
            name='codelanguages',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='contributionfeed_codelanguages', to='enterprises.CodeLanguageStatistic'),
        ),
        migrations.AddField(
            model_name='contributionfeed',
            name='files',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, null=True, related_name='files', to='enterprises.ContributionFile'),
        ),
        migrations.AddField(
            model_name='contributionfeed',
            name='page',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enterprise_contribution_feed', to='enterprises.EnterpriseFormPage'),
        ),
        migrations.AddField(
            model_name='codetransitionstatistic',
            name='page',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enterprise_codetransition_statistic', to='enterprises.EnterpriseFormPage'),
        ),
        migrations.AddField(
            model_name='codelanguagestatistic',
            name='page',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enterprise_codelanguage_statistic', to='enterprises.EnterpriseFormPage'),
        ),
    ]