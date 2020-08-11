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

from esite.enterprises.models import Enterprise

# Create your registration related graphql schemes here.


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude_fields = ["password"]


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(username=username, email=email,)

        if info.context.user.is_anonymous:
            raise GraphQLError("You must be logged to create a user")

        if not info.context.user.is_superuser:
            raise GraphQLError("You must be superuser to create a user")

        user.set_password(password)
        user.save()
        # saved to our user objects as a wagtail user

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType, token=graphene.String(required=False))
    users = graphene.List(UserType, token=graphene.String(required=False))
    enterprises = graphene.List(UserType, token=graphene.String(required=False))

    @superuser_required
    def resolve_users(self, info, **_kwargs):
        # session authentication
        # user = info.context.user
        # session authentication
        # if user.is_anonymous:
        #    raise GraphQLError('You must be logged to list a user')
        # if not user.is_superuser:
        #    raise Exception('You must be superuser to list a user')
        return get_user_model().objects.all()

    @superuser_required
    def resolve_enterprisemers(self, info, **_kwargs):
        # session authentication
        # user = info.context.user
        # if user.is_anonymous:
        #    raise GraphQLError('You must be logged to list enterprise')
        # if not user.is_superuser:
        #    raise Exception(f'You must be superuser to list enterprise {user.is_superuser}')
        return Enterprise.objects.all()

    @login_required
    def resolve_me(self, info, **_kwargs):
        user = info.context.user
        # session authentication
        # user = info.context.user
        # if user.is_anonymous:
        #    raise Exception('You must be logged')
        return user
