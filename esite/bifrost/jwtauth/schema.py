from django.contrib.auth import get_user_model

from wagtail.core.models import Page as wagtailPage

import graphene
import graphql_jwt
from graphene.types.generic import GenericScalar

from esite.bifrost.permissions import with_page_permissions

from ..registry import registry
from ..types.pages import Page

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
            .first(),
        )


class ObtainPrivilegedJSONWebToken(graphene.Mutation):

    token = graphene.String()
    payload = GenericScalar(required=True)
    refresh_expires_in = graphene.Int(required=True)

    class Arguments:
        token = graphene.String(required=True)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update(
            {
                get_user_model().USERNAME_FIELD: graphene.String(required=True),
                "password": graphene.String(required=True),
            }
        )
        return super().Field(*args, **kwargs)

    @classmethod
    @graphql_jwt.decorators.staff_member_required
    @graphql_jwt.decorators.token_auth
    def mutate(cls, root, info, **kwargs):
        # print(root, info.context.token)
        return ObtainPrivilegedJSONWebToken()

    @classmethod
    def resolve(cls, root, info, **kwargs):
        cls()
