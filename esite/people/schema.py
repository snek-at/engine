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

        if origin_person_page.person.user == user or user.is_superuser:
            """
            Allowed to set new follower for the page
            """
            destination_person_page = PersonFormPage.objects.get(
                slug=f"p-{person_to_follow}"
            )

            origin_person_page.follows.add(destination_person_page)
            origin_person_page.save()

        else:
            raise GraphQLError("Permission denied")

        return Follow(total_followers=origin_person_page.follows.count())


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

        if origin_person_page.person.user == user or user.is_superuser:
            """
            Allowed to unfollow
            """
            destination_person_page = PersonFormPage.objects.get(
                slug=f"p-{person_to_unfollow}"
            )

            origin_person_page.follows.remove(destination_person_page)
            origin_person_page.save()

        else:
            raise GraphQLError("Permission denied")

        return Follow(total_followers=origin_person_page.follows.count())


class Like(graphene.Mutation):
    total_likes = graphene.Int()

    class Arguments:
        token = graphene.String(required=True)
        person = graphene.String(required=True)
        person_to_like = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, person, person_to_like):
        user = info.context.user

        origin_person_page = PersonFormPage.objects.get(slug=f"p-{person}")

        if origin_person_page.person.user == user or user.is_superuser:
            """
            Allowed to like
            """
            destination_person_page = PersonFormPage.objects.get(
                slug=f"p-{person_to_like}"
            )

            origin_person_page.likes.add(destination_person_page)
            origin_person_page.save()

        else:
            raise GraphQLError("Permission denied")

        return Like(total_likes=origin_person_page.likes.count())


class Unlike(graphene.Mutation):
    total_likes = graphene.Int()

    class Arguments:
        token = graphene.String(required=True)
        person = graphene.String(required=True)
        person_to_unlike = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, person, person_to_unlike):
        user = info.context.user

        origin_person_page = PersonFormPage.objects.get(slug=f"p-{person}")

        if origin_person_page.person.user == user or user.is_superuser:
            """
            Allowed to unlike
            """
            destination_person_page = PersonFormPage.objects.get(
                slug=f"p-{person_to_unlike}"
            )

            origin_person_page.likes.remove(destination_person_page)
            origin_person_page.save()

        else:
            raise GraphQLError("Permission denied")

        return Unlike(total_likes=origin_person_page.likes.count())


class Mutation(graphene.ObjectType):
    follow = Follow.Field()
    unfollow = Unfollow.Field()
    like = Like.Field()
    unlike = Unlike.Field()


class Query(graphene.ObjectType):
    # get_followers = graphene.List(PersonPageType, token=graphene.String(required=False))
    pass
