from django.contrib.auth import get_user_model
from wagtail.core.models import Page as wagtailPage

import graphene
import graphql_jwt
from ..types.pages import Page
from ..registry import registry

from esite.bifrost.permissions import with_page_permissions

# Create your registration related graphql schemes here.


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):

    user = graphene.Field(registry.models[get_user_model()])
    profile = graphene.Field(Page)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user = info.context.user
        profilequery = wagtailPage.objects.filter(slug=f"{user.username}")
        return cls(
            user=info.context.user,
            profile=with_page_permissions(info.context, profilequery.specific())
            .live()
            .first()
        )
