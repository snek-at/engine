import json

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

from esite.images.models import SNEKPersonAvatarImage
from esite.people.models import Person, PersonPage
from esite.utils.tools import camelcase_to_snake


class PersonPageType(DjangoObjectType):
    class Meta:
        model = PersonPage


class PersonType(DjangoObjectType):
    class Meta:
        model = Person
        exclude_fields = ["user"]


class Upload(graphene.Scalar):
    def serialize(self):
        pass


class Follow(graphene.Mutation):
    total_followers = graphene.Int()

    class Arguments:
        token = graphene.String(required=True)
        person = graphene.String(required=True)
        person_to_follow = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, person, person_to_follow):
        user = info.context.user

        origin_person_page = PersonPage.objects.get(slug=f"p-{person}")

        if origin_person_page.person.user == user or user.is_superuser:
            """
            Allowed to set new follower for the page
            """
            destination_person_page = PersonPage.objects.get(
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

        origin_person_page = PersonPage.objects.get(slug=f"p-{person}")

        if origin_person_page.person.user == user or user.is_superuser:
            """
            Allowed to unfollow
            """
            destination_person_page = PersonPage.objects.get(
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

        origin_person_page = PersonPage.objects.get(slug=f"p-{person}")

        if origin_person_page.person.user == user or user.is_superuser:
            """
            Allowed to like
            """
            destination_person_page = PersonPage.objects.get(slug=f"p-{person_to_like}")

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

        origin_person_page = PersonPage.objects.get(slug=f"p-{person}")

        if origin_person_page.person.user == user or user.is_superuser:
            """
            Allowed to unlike
            """
            destination_person_page = PersonPage.objects.get(
                slug=f"p-{person_to_unlike}"
            )

            origin_person_page.likes.remove(destination_person_page)
            origin_person_page.save()

        else:
            raise GraphQLError("Permission denied")

        return Unlike(total_likes=origin_person_page.likes.count())


class UpdateSettings(graphene.Mutation):
    person_page = graphene.Field(PersonPageType)

    class Arguments:
        token = graphene.String(required=True)
        person_name = graphene.String(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        status = graphene.String(required=False)
        bio = graphene.String(required=False)
        avatar_image = Upload(required=False)
        email = graphene.String(required=False)
        display_email = graphene.Boolean(required=False)
        workplace = graphene.String(required=False)
        display_workplace = graphene.Boolean(required=False)
        website_url = graphene.String(required=False)
        location = graphene.String(required=False)
        display_ranking = graphene.Boolean(required=False)
        display_programming_languages = graphene.Boolean(required=False)
        display_2d_calendar = graphene.Boolean(required=False)
        display_3d_calendar = graphene.Boolean(required=False)

    @login_required
    def mutate(self, info, token, person_name, **kwargs):
        user = info.context.user

        """
        person_pages must contain one entry due to the uniqueness of the slug
        """
        person_pages = PersonPage.objects.filter(slug=f"p-{person_name}")

        person_page = person_pages.first()
        if not person_page:
            """
            No page found
            """
            raise GraphQLError("No profile found")

        if person_page.person.user == user or user.is_superuser:
            """
            Allowed to update settings
            """
            person_pages.update(**kwargs)

            """
            Set photo
            """
            if info.context.FILES and info.context.method == "POST":
                avatar_image = info.context.FILES["avatar_image"]

                person_page.avatar_image.delete()

                person_page.avatar_image = SNEKPersonAvatarImage.objects.create(
                    file=avatar_image, title=f"Avatar of {person_name}"
                )

                person_page.save()

        else:
            raise GraphQLError("Permission denied")

        return UpdateSettings(person_page=person_pages.first())


class VariableStore(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        token = graphene.String(required=True)
        person_name = graphene.String(required=True)
        raw_current_statistic = graphene.JSONString(required=False)
        raw_years_statistic = graphene.JSONString(required=False)
        raw_organisations = graphene.JSONString(required=False)
        raw_projects = graphene.JSONString(required=False)
        raw_languages = graphene.JSONString(required=False)

    @login_required
    def mutate(
        self,
        info,
        token,
        person_name,
        raw_current_statistic=None,
        raw_years_statistic=[],
        raw_organisations=[],
        raw_projects=[],
        raw_languages=[],
        **kwargs,
    ):
        import esite.people.models

        user = info.context.user

        """
        person must contain one entry due to the uniqueness of the slug
        """
        person = Person.objects.filter(person_page__slug=f"p-{person_name}").first()

        if not person:
            """
            No person found
            """
            raise GraphQLError("No profile found")

        if person.user == user or user.is_superuser:
            """
            Allowed to update person data
            """

            def process_raw_data(obj_type: str, obj=None, for_streamfield=False):
                if isinstance(obj, dict):

                    if "repositories" in obj:
                        obj["projects"] = obj.pop("repositories")

                    obj = {
                        camelcase_to_snake(k): process_raw_data(
                            camelcase_to_snake(k), v
                        )
                        for (k, v) in obj.items()
                    }

                    if for_streamfield:
                        return [{"type": obj_type, "value": obj}]

                if isinstance(obj, list):
                    """
                    Get the singular of obj_type by removing s
                    which is the last character
                    """
                    obj = [process_raw_data(obj_type[:-1], e) for e in obj]

                    if for_streamfield:
                        return [{"type": obj_type[:-1], "value": e} for e in obj]

                return obj

            projects = process_raw_data("projects", raw_projects, for_streamfield=True)
            organisations = process_raw_data(
                "organisations", raw_organisations, for_streamfield=True
            )
            languages = process_raw_data(
                "languages", raw_languages, for_streamfield=True
            )
            current_statistic = process_raw_data(
                "statistic_year", raw_current_statistic, for_streamfield=True
            )
            years_statistic = process_raw_data(
                "statistic_years", raw_years_statistic, for_streamfield=True
            )

            person.projects = json.dumps(projects)
            person.organisations = json.dumps(organisations)
            person.languages = json.dumps(languages)
            person.current_statistic = json.dumps(current_statistic)
            person.years_statistic = json.dumps(years_statistic)

            person.save()
        else:
            raise GraphQLError("Permission denied")

        return VariableStore(person=person)


class Mutation(graphene.ObjectType):
    follow = Follow.Field()
    unfollow = Unfollow.Field()
    like = Like.Field()
    unlike = Unlike.Field()
    update_person_setting = UpdateSettings.Field()
    variable_store = VariableStore.Field()


class Query(graphene.ObjectType):
    # get_followers = graphene.List(PersonPageType, token=graphene.String(required=False))
    pass
