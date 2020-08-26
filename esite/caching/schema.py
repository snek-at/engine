from django.contrib.auth import get_user_model

from wagtail.core.models import Page

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import (
    login_required,
    permission_required,
    staff_member_required,
    superuser_required,
)

from esite.enterprises.models import Enterprise
from esite.people.models import PersonFormPage
from esite.registration.schema import UserType

# Create your registration related graphql schemes here.


class PersonType(DjangoObjectType):
    class Meta:
        model = PersonFormPage


class CacheUser(graphene.Mutation):
    user = graphene.Field(PersonType)

    class Arguments:
        token = graphene.String(required=True)
        person_name = graphene.String(required=True)
        cache = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, person_name, cache, **kwargs):
        user = info.context.user

        if user.is_superuser:
            person_page = PersonFormPage.objects.get(slug=f"p-{person_name}")
        else:
            person_page = PersonFormPage.objects.filter(
                slug=f"p-{person_name}", person__user=user
            ).first()

        if not person_page:
            raise GraphQLError("Something went wrong!")

        person_page.person.cache = cache
        person_page.save()

        return CacheUser(person_page=person_page)


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
