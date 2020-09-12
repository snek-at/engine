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
from esite.people.models import PersonPage
from esite.achievement.models import Achievement


class AchievementType(DjangoObjectType):
    class Meta:
        model = Achievement
        exclude_fields = ["id"]


class RedeemAchievement(graphene.Mutation):
    ok = graphene.Boolean()
    achievement = graphene.Field(AchievementType)

    class Arguments:
        token = graphene.String(required=True)
        person_name = graphene.String(required=True)
        sequence = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, person_name, sequence, **kwargs):
        user = info.context.user

        if user.is_superuser:
            person_pages = PersonPage.objects.filter(slug=f"p-{person_name}")
        else:
            person_pages = PersonPage.objects.filter(
                slug=f"p-{person_name}", person__user=user
            )

        person_page = person_pages.first()

        if not person_page:
            raise GraphQLError("person_name not valid on user")

        try:
            achievement = Achievement.objects.get(id=sequence)
            achievement.collectors.add(person_page)
            achievement.save()

            return RedeemAchievement(achievement=achievement, ok=True)
        except:
            """
            - Minus karma for person
            - unlock achievement
            """
            return RedeemAchievement(ok=True)


class Mutation(graphene.ObjectType):
    redeem_achievement = RedeemAchievement.Field()


class Query(graphene.ObjectType):
    achievements = graphene.List(AchievementType, token=graphene.String(required=False))

    @login_required
    def resolve_achievements(self, info, **_kwargs):

        return Achievement.objects.all()
