from django.db import models
import graphene
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    StreamFieldPanel,
    InlinePanel,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField

from esite.bifrost.helpers import register_streamfield_block, register_query_field
from esite.bifrost.models import (
    GraphQLString,
    GraphQLInt,
    GraphQLFloat,
    GraphQLStreamfield,
    GraphQLForeignKey,
    GraphQLEmbed,
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


class Person(ClusterableModel):
    user = ParentalKey("user.SNEKUser", on_delete=models.CASCADE, related_name="person")

    projects = StreamField([("project", _Person_Project())], null=True, blank=True)
    organisations = StreamField(
        [("organisation", _Person_Organisation())], null=True, blank=True
    )

    # Panels/fields to fill in the Add enterprise form
    panels = [
        FieldPanel("user"),
        MultiFieldPanel(
            [StreamFieldPanel("projects"), StreamFieldPanel("organisations")]
        ),
    ]

    graphql_fields = [
        # GraphQLString("user"),
        GraphQLStreamfield("projects"),
        GraphQLStreamfield("organisations"),
    ]

    def __str__(self):
        return self.user.username
