# Generated by Django 2.2.12 on 2020-08-12 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('images', '0002_auto_20200729_2232'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('enterprises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enterprise',
            fields=[
            ],
            options={
                'ordering': ('date_joined',),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.snekuser',),
        ),
        migrations.AddField(
            model_name='projectcontributor',
            name='codelanguages',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='projectcontributor_codelanguages', to='enterprises.CodeLanguageStatistic'),
        ),
        migrations.AddField(
            model_name='projectcontributor',
            name='codetransition',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='projectcontributor_codetransition', to='enterprises.CodeTransitionStatistic'),
        ),
        migrations.AddField(
            model_name='projectcontributor',
            name='contribution_feed',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='projectcontributor_feed', to='enterprises.ContributionFeed'),
        ),
        migrations.AddField(
            model_name='projectcontributor',
            name='project',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_projectcontributor', to='enterprises.Project'),
        ),
        migrations.AddField(
            model_name='project',
            name='codelanguages',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='project_codelanguages', to='enterprises.CodeLanguageStatistic'),
        ),
        migrations.AddField(
            model_name='project',
            name='codetransition',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='project_codetransition', to='enterprises.CodeTransitionStatistic'),
        ),
        migrations.AddField(
            model_name='project',
            name='contribution_feed',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='project_feed', to='enterprises.ContributionFeed'),
        ),
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='project_contributor', to='enterprises.ProjectContributor'),
        ),
        migrations.AddField(
            model_name='project',
            name='page',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enterprise_projects', to='enterprises.EnterpriseFormPage'),
        ),
        migrations.AddField(
            model_name='enterpriseindex',
            name='listing_image',
            field=models.ForeignKey(blank=True, help_text='Choose the image you wish to be displayed when this page appears in listings', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.SNEKImage'),
        ),
        migrations.AddField(
            model_name='enterpriseindex',
            name='social_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.SNEKImage'),
        ),
        migrations.AddField(
            model_name='enterpriseformsubmission',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='enterpriseformsubmission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
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
            model_name='enterpriseformpage',
            name='user',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprisepage', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enterpriseformfield',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='enterprises.EnterpriseFormPage'),
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
