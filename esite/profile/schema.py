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

from esite.people.models import PersonFormPage
from esite.profile.models import Profile


# Create your registration related graphql schemes here.


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class UpdateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    class Arguments:
        token = graphene.String(required=True)
        profile_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, token, profile_id, **kwargs):
        user = info.context.user

        if user.is_superuser:
            profiles = Profile.objects.filter(id=profile_id)
        else:
            profiles = Profile.objects.filter(
                id=profile_id, person_page__person__user=user
            )

        print(profiles)

        if not profiles.first():
            raise GraphQLError("profile_id not valid")

        profiles.update(**kwargs)

        print(profiles.first().id)

        return UpdateProfile(profile=profiles.first())


class Mutation(graphene.ObjectType):
    update_profile = UpdateProfile.Field()


class Query(graphene.ObjectType):
    person_profiles = graphene.List(
        ProfileType,
        token=graphene.String(required=False),
        person_name=graphene.String(required=False),
    )

    @login_required
    def resolve_person_profiles(self, info, token, person_name, **_kwargs):
        user = info.context.user

        person_page = PersonFormPage.objects.filter(slug=f"p-{person_name}").first()

        if not person_page:
            raise GraphQLError("Person not valid")
        if person_page.person.user == user or user.is_superuser:
            return person_page.profiles.all()

        raise GraphQLError("Something went wrong")
