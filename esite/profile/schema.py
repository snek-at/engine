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


class AddProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    class Arguments:
        token = graphene.String(required=True)
        person_name = graphene.String(required=True)
        username = graphene.String(required=False)
        access_token = graphene.String(required=False)
        source_type = graphene.String(required=False)

    @login_required
    def mutate(self, info, token, person_name, **kwargs):
        user = info.context.user

        if user.is_superuser:
            person_pages = PersonFormPage.objects.filter(slug=f"p-{person_name}")
        else:
            person_pages = Profile.objects.filter(
                slug=f"p-{person_name}", person__user=user
            )

        person_page = person_pages.first()

        if not person_page:
            raise GraphQLError("person_name not valid on user")

        profile = Profile.objects.create(**kwargs)
        person_page.profiles.add(profile)
        person_page.save_revision().publish()

        return AddProfile(profile=profile)


class DeleteProfile(graphene.Mutation):
    profiles = graphene.List(ProfileType)

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

        profile = profiles.first()

        if not profile:
            raise GraphQLError("profile_id not valid")

        profile.delete()

        return DeleteProfile(
            profiles=Profile.objects.filter(person_page__person__user=user)
        )


class UpdateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    class Arguments:
        token = graphene.String(required=True)
        profile_id = graphene.ID(required=True)
        username = graphene.String(required=False)
        access_token = graphene.String(required=False)
        source_type = graphene.String(required=False)

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
    add_profile = AddProfile.Field()
    delete_profile = DeleteProfile.Field()
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
