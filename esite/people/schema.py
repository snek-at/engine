import json

from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from graphql_jwt.decorators import (
    login_required,
    permission_required,
    staff_member_required,
    superuser_required,
)

from esite.images.models import SNEKImage
from esite.people.models import Meta_Link, Person, PersonPage
from esite.utils.tools import camelcase_to_snake, get_image_from_data_url


class PersonPageType(DjangoObjectType):
    class Meta:
        model = PersonPage


class PersonType(DjangoObjectType):
    class Meta:
        model = Person
        exclude_fields = ["user"]


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


class UpdatePersonPage(graphene.Mutation):
    person_page = graphene.Field(PersonPageType)

    class Arguments:
        token = graphene.String(required=True)
        person_name = graphene.String(required=True)
        movable_pool = graphene.JSONString(required=False)
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
    def mutate(
        self, info, token, person_name, movable_pool=None, avatar_image=None, **kwargs
    ):
        print("KWARGS", kwargs)

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
            print(person_pages[0].first_name)

            print(person_pages[0].first_name)
            print("UPDATED")
            if movable_pool:
                try:
                    person_page.movable_pool = [
                        (e.field, e.rawValue) for e in json.loads(movable_pool)
                    ]
                except:
                    raise GraphQLError("Something went wrong with movable_pool")

            if avatar_image:
                """
                Set photo
                """
                print(avatar_image)
                if person_page.avatar_image:
                    person_page.avatar_image.delete()

                image = SNEKImage.objects.create(
                    file=avatar_image, title=f"Avatar of {person_name}", author=user
                )

                person_page.avatar_image = image

            person_page.save()
            person_pages.update(**kwargs)

        else:
            raise GraphQLError("Permission denied")

        return UpdatePersonPage(person_page=person_pages.first())


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
        raw_current_statistic_calendar_image = Upload(required=False)
        raw_years_statistic_calendar_images = Upload(required=False)

    @login_required
    def mutate(
        self,
        info,
        token,
        person_name,
        raw_current_statistic=None,
        raw_years_statistic=None,
        raw_organisations=None,
        raw_projects=None,
        raw_languages=None,
        raw_current_statistic_calendar_image=None,
        raw_years_statistic_calendar_images=None,
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

            if raw_projects:
                projects = process_raw_data(
                    "projects", raw_projects, for_streamfield=True
                )
                person.projects = json.dumps(projects)

            if raw_organisations:
                organisations = process_raw_data(
                    "organisations", raw_organisations, for_streamfield=True
                )
                person.organisations = json.dumps(organisations)

            if raw_languages:
                languages = process_raw_data(
                    "languages", raw_languages, for_streamfield=True
                )
                person.languages = json.dumps(languages)

            if raw_current_statistic:
                current_statistic = process_raw_data(
                    "statistic_year", raw_current_statistic, for_streamfield=True
                )
                person.current_statistic = json.dumps(current_statistic)

            if raw_years_statistic:
                years_statistic = process_raw_data(
                    "statistic_years", raw_years_statistic, for_streamfield=True
                )
                person.years_statistic = json.dumps(years_statistic)

            if raw_current_statistic_calendar_image:
                """
                Set photo
                """
                if current_statistic.calendar3d:
                    current_statistic.calendar3d.delete()

                image = SNEKImage.objects.create(
                    file=raw_current_statistic_calendar_image,
                    title=f"Current calendar of {person_name}",
                    author=user,
                )

                current_statistic.calendar3d = image

            if raw_years_statistic_calendar_images:
                for idx, val in enumerate(years_statistic):
                    try:
                        """
                        Set photo
                        """
                        if val.calendar3d:
                            val.calendar3d.delete()

                            image = SNEKImage.objects.create(
                                file=raw_years_statistic_calendar_images[idx],
                                title=f"Year calendar {idx} of {person_name}",
                                author=user,
                            )

                            val.calendar3d = image

                    except IndexError:
                        pass

            person.save()
        else:
            raise GraphQLError("Permission denied")

        return VariableStore(person=person)


class MetaLinkType(DjangoObjectType):
    class Meta:
        model = Meta_Link


class AddPersonPageMetaLink(graphene.Mutation):
    meta_link = graphene.Field(MetaLinkType)

    class Arguments:
        token = graphene.String(required=True)
        person_name = graphene.String(required=True)
        url = graphene.String(required=True)
        link_type = graphene.String(required=True)
        location = graphene.String(required=False)
        description = graphene.String(required=False)
        imgur_delete_hash = graphene.String(required=False)

    def mutate(self, info, token, person_name, **kwargs):
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

        meta_link = Meta_Link.objects.create(person_page=person_page, **kwargs)

        return AddPersonPageMetaLink(meta_link=meta_link)


class DeletePersonPageMetaLink(graphene.Mutation):
    meta_links = graphene.List(MetaLinkType)

    class Arguments:
        token = graphene.String(required=True)
        meta_link_id = graphene.String(required=True)

    def mutate(self, info, token, meta_link_id, **kwargs):
        user = info.context.user

        if user.is_superuser:
            meta_links = Meta_Link.objects.filter(id=meta_link_id)
        else:
            meta_links = Meta_Link.objects.filter(
                id=meta_link_id, person_page__person__user=user
            )

        meta_link = meta_links.first()

        if not meta_link:
            raise GraphQLError("meta_link_id not valid for user")

        meta_link.delete()

        return DeletePersonPageMetaLink(
            meta_link=Meta_Link.objects.filter(person_page__person__user=user)
        )


class CheckPersonPageMetaLink(graphene.Mutation):
    exists = graphene.Boolean()

    class Arguments:
        token = graphene.String(required=True)
        person_name = graphene.String(required=True)
        url = graphene.String(required=True)
        link_type = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, person_name, **kwargs):
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
            link = Meta_Link.objects.get(person_page=person_page, **kwargs)

            return CheckPersonPageMetaLink(exists=True)
        except Meta_Link.DoesNotExist:
            return CheckPersonPageMetaLink(exists=False)


class Mutation(graphene.ObjectType):
    follow = Follow.Field()
    unfollow = Unfollow.Field()
    like = Like.Field()
    unlike = Unlike.Field()
    update_person_page = UpdatePersonPage.Field()
    variable_store = VariableStore.Field()
    add_person_page_meta_link = AddPersonPageMetaLink.Field()
    delete_person_page_meta_link = DeletePersonPageMetaLink.Field()
    check_person_page_meta_link = CheckPersonPageMetaLink.Field()


class Query(graphene.ObjectType):
    # get_followers = graphene.List(PersonPageType, token=graphene.String(required=False))
    pass
