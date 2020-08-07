from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Enterprise

# Create your enterprise related graphql schemes here.


class UserType(DjangoObjectType):
    class Meta:
        model = Enterprise


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(username=username, email=email,)
        # if info.context.user.is_anonymous:
        #    raise GraphQLError('You must be logged to create a user')

        # if not info.context.user.is_superuser:
        #    raise GraphQLError('You must be superuser to create a user')

        user.set_password(password)
        user.save()
        # saved to our user objects as a wagtail user

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        # To list all users
        return Enterprise.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged!")
        return user
