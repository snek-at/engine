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
    me = graphene.Field(
        registry.models[get_user_model()], token=graphene.String(required=False)
    )
    users = graphene.List(
        registry.models[get_user_model()], token=graphene.String(required=False)
    )

    @superuser_required
    def resolve_users(self, info, **_kwargs):

        return get_user_model().objects.all()

    @login_required
    def resolve_me(self, info, **_kwargs):
        user = info.context.user

        return user


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
