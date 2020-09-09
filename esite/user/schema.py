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

from esite.bifrost.registry import registry

# Create your registration related graphql schemes here.


class CreateUser(graphene.Mutation):
    user = graphene.Field(registry.models[get_user_model()])

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, username, password, email):
        user = get_user_model()(username=username, email=email,)

        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    user_exists = graphene.Boolean(
        token=graphene.String(required=True), username=graphene.String(required=True),
    )

    me = graphene.Field(
        registry.models[get_user_model()], token=graphene.String(required=False)
    )
    # user = graphene.Field(
    #     registry.models[get_user_model()],
    #     username=graphene.String(required=False),
    #     token=graphene.String(required=False),
    # )
    # users = graphene.List(
    #     registry.models[get_user_model()], token=graphene.String(required=False)
    # )

    @login_required
    def resolve_user_exists(self, info, token, username, **kwargs):
        try:
            user = get_user_model().objects.get(username=username)
            return True
        except get_user_model().DoesNotExist:
            return False

    # @superuser_required
    # def resolve_users(self, info, **_kwargs):

    #     return get_user_model().objects.all()

    # @login_required
    # def resolve_user(self, info, username, **_kwargs):
    #     print(username)
    #     user = get_user_model().objects.get(username=username)
    #     print(user.__dict__)

    #     return user

    @login_required
    def resolve_me(self, info, **_kwargs):
        user = info.context.user

        return user


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
