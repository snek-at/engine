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

from esite.achievement.models import Achievement


class AchievementType(DjangoObjectType):
    class Meta:
        model = Achievement


class Query(graphene.ObjectType):
    achievements = graphene.List(AchievementType, token=graphene.String(required=False))

    @login_required
    def resolve_achievements(self, info, **_kwargs):

        return Achievement.objects.all()
