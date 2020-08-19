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

from esite.people.models import PersonFormPage


class PersonPageType(DjangoObjectType):
    class Meta:
        model = PersonFormPage


class Follow(graphene.Mutation):
    total_followers = graphene.Int()

    class Arguments:
        token = graphene.String(required=True)
        person = graphene.String(required=True)
        person_to_follow = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, person, person_to_follow):
        user = info.context.user

        origin_person_page = PersonFormPage.objects.get(slug=f"p-{person}")

        if origin_person_page.user == user or user.is_superuser:
            """
            Allowed to set new follower for the page
            """
            destination_person_page = PersonFormPage.objects.get(
                slug=f"p-{person_to_follow}"
            )

            destination_person_page.follows.add(origin_person_page)

        else:
            raise GraphQLError("Permission denied")

        return Follow(total_followers=destination_person_page.follows.count())


class Unfollow(graphene.Mutation):
    total_followers = graphene.Int()

    class Arguments:
        token = graphene.String(required=True)
        person = graphene.String(required=True)
        person_to_unfollow = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, person, person_to_unfollow):
        user = info.context.user

        origin_person_page = PersonFormPage.objects.get(slug=f"p-{person}")

        if origin_person_page.user == user or user.is_superuser:
            """
            Allowed to unfollow
            """
            destination_person_page = PersonFormPage.objects.get(
                slug=f"p-{person_to_unfollow}"
            )

            destination_person_page.follows.remove(origin_person_page)

        else:
            raise GraphQLError("Permission denied")

        return Follow(total_followers=destination_person_page.follows.count())


class Mutation(graphene.ObjectType):
    follow = Follow.Field()
    unfollow = Unfollow.Field()


class Query(graphene.ObjectType):
    # get_followers = graphene.List(PersonPageType, token=graphene.String(required=False))
    pass
