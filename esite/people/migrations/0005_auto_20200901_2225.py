# Generated by Django 2.2 on 2020-09-01 20:25

from django.db import migrations
import esite.colorfield.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_auto_20200901_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='current_statistic',
            field=wagtail.core.fields.StreamField([('statistic_year', wagtail.core.blocks.StructBlock([('calendar3d', wagtail.images.blocks.ImageChooserBlock(required=False)), ('calendar2d', wagtail.core.blocks.TextBlock(required=False)), ('contribution_type2d', wagtail.core.blocks.TextBlock()), ('total_issue_contributions', wagtail.core.blocks.IntegerBlock(required=False)), ('total_commit_contributions', wagtail.core.blocks.IntegerBlock()), ('total_repository_contributions', wagtail.core.blocks.IntegerBlock()), ('total_pull_request_contributions', wagtail.core.blocks.IntegerBlock()), ('total_pull_request_review_contributions', wagtail.core.blocks.IntegerBlock()), ('total_repositories_with_contributed_issues', wagtail.core.blocks.IntegerBlock()), ('total_repositories_with_contributed_commits', wagtail.core.blocks.IntegerBlock()), ('total_repositories_with_contributed_pull_requests', wagtail.core.blocks.IntegerBlock()), ('current_streak', wagtail.core.blocks.StructBlock([('start_date', wagtail.core.blocks.DateBlock(blank=True, null=True)), ('end_date', wagtail.core.blocks.DateBlock(blank=True, null=True)), ('total_days', wagtail.core.blocks.IntegerBlock(blank=True, null=True)), ('total_contributions', wagtail.core.blocks.IntegerBlock(blank=True, null=True))])), ('longest_streak', wagtail.core.blocks.StructBlock([('start_date', wagtail.core.blocks.DateBlock(blank=True, null=True)), ('end_date', wagtail.core.blocks.DateBlock(blank=True, null=True)), ('total_days', wagtail.core.blocks.IntegerBlock(blank=True, null=True)), ('total_contributions', wagtail.core.blocks.IntegerBlock(blank=True, null=True))]))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='languages',
            field=wagtail.core.fields.StreamField([('language', wagtail.core.blocks.StructBlock([('color', esite.colorfield.blocks.ColorBlock(blank=True, null=True)), ('name', wagtail.core.blocks.CharBlock(max_length=255)), ('size', wagtail.core.blocks.IntegerBlock()), ('share', wagtail.core.blocks.FloatBlock())]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='organisations',
            field=wagtail.core.fields.StreamField([('organisation', wagtail.core.blocks.StructBlock([('avatar_url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('name', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('fullname', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('description', wagtail.core.blocks.TextBlock(blank=True, null=True)), ('members', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('avatar_url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('fullname', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('name', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True))]))), ('projects', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('avatar_url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('name', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('fullname', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('owner', wagtail.core.blocks.StructBlock([('avatar_url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('fullname', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('name', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True))])), ('members', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('avatar_url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('fullname', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('name', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True))]))), ('languages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('color', esite.colorfield.blocks.ColorBlock(blank=True, null=True)), ('name', wagtail.core.blocks.CharBlock(max_length=255)), ('size', wagtail.core.blocks.IntegerBlock()), ('share', wagtail.core.blocks.FloatBlock())])))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='projects',
            field=wagtail.core.fields.StreamField([('project', wagtail.core.blocks.StructBlock([('avatar_url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('name', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('fullname', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('owner', wagtail.core.blocks.StructBlock([('avatar_url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('fullname', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('name', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True))])), ('members', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('avatar_url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('url', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True)), ('fullname', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True)), ('name', wagtail.core.blocks.CharBlock(blank=True, max_length=255, null=True))]))), ('languages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('color', esite.colorfield.blocks.ColorBlock(blank=True, null=True)), ('name', wagtail.core.blocks.CharBlock(max_length=255)), ('size', wagtail.core.blocks.IntegerBlock()), ('share', wagtail.core.blocks.FloatBlock())])))]))], blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='years_statistic',
            field=wagtail.core.fields.StreamField([('statistic_year', wagtail.core.blocks.StructBlock([('calendar3d', wagtail.images.blocks.ImageChooserBlock(required=False)), ('calendar2d', wagtail.core.blocks.TextBlock(required=False)), ('contribution_type2d', wagtail.core.blocks.TextBlock()), ('total_issue_contributions', wagtail.core.blocks.IntegerBlock(required=False)), ('total_commit_contributions', wagtail.core.blocks.IntegerBlock()), ('total_repository_contributions', wagtail.core.blocks.IntegerBlock()), ('total_pull_request_contributions', wagtail.core.blocks.IntegerBlock()), ('total_pull_request_review_contributions', wagtail.core.blocks.IntegerBlock()), ('total_repositories_with_contributed_issues', wagtail.core.blocks.IntegerBlock()), ('total_repositories_with_contributed_commits', wagtail.core.blocks.IntegerBlock()), ('total_repositories_with_contributed_pull_requests', wagtail.core.blocks.IntegerBlock()), ('current_streak', wagtail.core.blocks.StructBlock([('start_date', wagtail.core.blocks.DateBlock(blank=True, null=True)), ('end_date', wagtail.core.blocks.DateBlock(blank=True, null=True)), ('total_days', wagtail.core.blocks.IntegerBlock(blank=True, null=True)), ('total_contributions', wagtail.core.blocks.IntegerBlock(blank=True, null=True))])), ('longest_streak', wagtail.core.blocks.StructBlock([('start_date', wagtail.core.blocks.DateBlock(blank=True, null=True)), ('end_date', wagtail.core.blocks.DateBlock(blank=True, null=True)), ('total_days', wagtail.core.blocks.IntegerBlock(blank=True, null=True)), ('total_contributions', wagtail.core.blocks.IntegerBlock(blank=True, null=True))]))]))], blank=True, null=True),
        ),
    ]
