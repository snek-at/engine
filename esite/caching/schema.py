from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import (
    login_required,
    permission_required,
    staff_member_required,
    superuser_required,
)

from wagtail.core.models import Page

from esite.enterprise.models import Enterprise
from esite.registration.schema import UserType

# Create your registration related graphql schemes here.

# class UserType(DjangoObjectType):
#    class Meta:
#        model = User
#        exclude_fields = ['password']


class CacheUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        token = graphene.String(required=False)
        cache = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, cache):
        user = info.context.user

        user.cache = cache
        user.save()

        # profile_page = Page.objects.get(slug=f"user_{user.username}").specific

        # profile_page.platform_data = platform_data

        # profile_page.save_revision().publish()

        return CacheUser(user=user)


class CacheUserByName(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        token = graphene.String(required=False)
        username = graphene.String(required=False)
        cache = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, username, cache):
        user = info.context.user

        profile_page = Page.objects.get(slug=f"{username}").specific

        profile_page.cache = cache

        profile_page.save_revision().publish()

        return CacheUser(user=user)
