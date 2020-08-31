from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

import graphene

from esite.bifrost.helpers import register_query_field, register_streamfield_block
from esite.bifrost.models import (
    GraphQLEmbed,
    GraphQLFloat,
    GraphQLForeignKey,
    GraphQLImage,
    GraphQLInt,
    GraphQLStreamfield,
    GraphQLString,
)
from esite.colorfield.blocks import ColorBlock


@register_streamfield_block
class _Person_Language(blocks.StructBlock):
    color = ColorBlock()
    name = blocks.CharBlock(max_length=255)
    size = blocks.IntegerBlock()
    share = blocks.FloatBlock()

    graphql_fields = [
        GraphQLString("color"),
        GraphQLString("name"),
        GraphQLInt("size"),
        GraphQLFloat("share"),
    ]


@register_streamfield_block
class _Person_Member(blocks.StructBlock):
    avatar_url = blocks.URLBlock(
        help_text="Important! Format https://www.domain.tld/xyz"
    )
    url = blocks.URLBlock(help_text="Important! Format https://www.domain.tld/xyz")
    fullname = blocks.CharBlock(max_length=255)
    name = blocks.CharBlock(max_length=255)

    graphql_fields = [
        GraphQLString("avatar_url"),
        GraphQLString("url"),
        GraphQLString("fullname"),
        GraphQLString("name"),
    ]


@register_streamfield_block
class _Person_Project(blocks.StructBlock):
    avatar_url = blocks.URLBlock(
        help_text="Important! Format https://www.domain.tld/xyz"
    )
    url = blocks.URLBlock(help_text="Important! Format https://www.domain.tld/xyz")
    name = blocks.CharBlock(max_length=255)
    fullname = blocks.CharBlock(max_length=255)
    owner = _Person_Member()
    members = blocks.ListBlock(_Person_Member())
    languages = blocks.ListBlock(_Person_Language())

    graphql_fields = [
        GraphQLString("avatar_url"),
        GraphQLString("url"),
        GraphQLString("name"),
        GraphQLString("fullname"),
        GraphQLString("owner_avatar_url"),
        GraphQLString("owner_url"),
        GraphQLString("owner_fullname"),
        GraphQLString("owner_name"),
        GraphQLStreamfield("owner", is_list=False),
        GraphQLStreamfield("members"),
        GraphQLStreamfield("languages"),
    ]


@register_streamfield_block
class _Person_Organisation(blocks.StructBlock):
    profile_name = blocks.CharBlock(max_length=255)
    avatar_url = blocks.URLBlock(
        help_text="Important! Format https://www.domain.tld/xyz"
    )
    url = blocks.URLBlock(help_text="Important! Format https://www.domain.tld/xyz")
    name = blocks.CharBlock(max_length=255)
    fullname = blocks.CharBlock(max_length=255)
    description = blocks.TextBlock(null=True, blank=True)
    members = blocks.ListBlock(_Person_Member())
    projects = blocks.ListBlock(_Person_Project())

    graphql_fields = [
        GraphQLString("profile_name"),
        GraphQLString("avatar_url"),
        GraphQLString("url"),
        GraphQLString("name"),
        GraphQLString("fullname"),
        GraphQLString("description"),
        GraphQLStreamfield("members"),
        GraphQLStreamfield("projects"),
    ]


@register_streamfield_block
class _Person_Statistic_Streak(blocks.StructBlock):
    start_date = blocks.DateBlock()
    end_date = blocks.DateBlock()
    total_days = blocks.IntegerBlock()
    total_contributions = blocks.IntegerBlock()

    graphql_fields = [
        GraphQLString("start_date"),
        GraphQLString("end_date"),
        GraphQLInt("total_days"),
        GraphQLInt("total_contributions"),
    ]


@register_streamfield_block
class Statistic(blocks.StructBlock):
    calendar_3d = ImageChooserBlock()
    calendar_2d = blocks.TextBlock()
    contribution_type_2d = blocks.TextBlock()
    total_issue_contributions = blocks.IntegerBlock()
    total_commit_contributions = blocks.IntegerBlock()
    total_repository_contributions = blocks.IntegerBlock()
    total_pull_request_contributions = blocks.IntegerBlock()
    total_pull_request_review_contributions = blocks.IntegerBlock()
    total_repositories_with_contributed_issues = blocks.IntegerBlock()
    total_repositories_with_contributed_commits = blocks.IntegerBlock()
    total_repositories_with_contributed_pull_requests = blocks.IntegerBlock()
    current_streak = _Person_Statistic_Streak()
    longest_streak = _Person_Statistic_Streak()

    graphql_fields = [
        GraphQLImage("calendar_3d"),
        GraphQLString("calendar_2d"),
        GraphQLString("contribution_type_2d"),
        GraphQLInt("total_issue_contributions"),
        GraphQLInt("total_commit_contributions"),
        GraphQLInt("total_repository_contributions"),
        GraphQLInt("total_pull_request_contributions"),
        GraphQLInt("total_pull_request_review_contributions"),
        GraphQLInt("total_repositories_with_contributed_issues"),
        GraphQLInt("total_repositories_with_contributed_commits"),
        GraphQLInt("total_repositories_with_contributed_pull_requests"),
        GraphQLStreamfield("current_streak", is_list=False),
        GraphQLStreamfield("longest_streak", is_list=False),
    ]


class Person(ClusterableModel):
    user = ParentalKey("user.SNEKUser", on_delete=models.CASCADE, related_name="person")

    current_statistic = StreamField(
        blocks.StreamBlock(
            [("statistic_year", _Person_Statistic_Streak()),], max_num=1
        ),
        null=True,
        blank=True,
    )
    years_statistic = StreamField(
        blocks.StreamBlock([("statistic_year", _Person_Statistic_Streak()),],),
        null=True,
        blank=True,
    )

    projects = StreamField([("project", _Person_Project())], null=True, blank=True)
    organisations = StreamField(
        [("organisation", _Person_Organisation())], null=True, blank=True
    )
    languages = StreamField([("language", _Person_Language())], null=True, blank=True)

    # Panels/fields to fill in the Add enterprise form
    panels = [
        FieldPanel("user"),
        MultiFieldPanel(
            [
                StreamFieldPanel("projects"),
                StreamFieldPanel("organisations"),
                StreamFieldPanel("languages"),
            ]
        ),
        StreamFieldPanel("current_statistic"),
        StreamFieldPanel("years_statistic"),
    ]

    graphql_fields = [
        # GraphQLString("user"),
        GraphQLStreamfield("projects"),
        GraphQLStreamfield("organisations"),
        GraphQLStreamfield("languages"),
        GraphQLStreamfield("current_statistic"),
        GraphQLStreamfield("years_statistic"),
    ]

    def __str__(self):
        return self.user.username
