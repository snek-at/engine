from django.conf import settings

# django
from django.utils.text import camel_case_to_spaces

import graphene
import graphql_jwt
from graphql.validation.rules import NoUnusedFragments, specified_rules

# HACK: Remove NoUnusedFragments validator
# Due to the way previews work on the frontend, we need to pass all
# fragments into the query even if they're not used.
# This would usually cause a validation error. There doesn't appear
# to be a nice way to disable this validator so we monkey-patch it instead.


# We need to update specified_rules in-place so the change appears
# everywhere it's been imported

specified_rules[:] = [rule for rule in specified_rules if rule is not NoUnusedFragments]


def create_schema():
    """
    Root schema object that graphene is pointed at.
    It inherits its queries from each of the specific type mixins.
    """
    from .registry import registry
    from .types.documents import DocumentsQuery
    from .types.images import ImagesQuery
    from .types.pages import PagesQuery, PagesSubscription
    from .types.search import SearchQuery
    from .types.settings import SettingsQuery
    from .types.snippets import SnippetsQuery
    from .types.redirects import RedirectsQuery

    import esite.user.schema
    import esite.achievement.schema
    import esite.talk.schema
    import esite.profile.schema
    from .jwtauth.schema import ObtainJSONWebToken
    from esite.caching.schema import CacheUser, CacheUserByName
    from esite.people.schema import (
        Follow,
        Unfollow,
        Like,
        Unlike,
        UpdateSettings,
        VariableStore,
        AddPersonPageMetaLink,
        DeletePersonPageMetaLink,
    )

    class Query(
        # Custom queries start
        esite.user.schema.Query,
        esite.achievement.schema.Query,
        esite.talk.schema.Query,
        esite.profile.schema.Query,
        # Custom queries end
        graphene.ObjectType,
        PagesQuery(),
        ImagesQuery(),
        DocumentsQuery(),
        SnippetsQuery(),
        SettingsQuery(),
        SearchQuery(),
        RedirectsQuery,
        *registry.schema,
    ):
        pass

    class Subscription(PagesSubscription(), graphene.ObjectType):
        pass

    def mutation_parameters() -> dict:
        dict_params = {
            "token_auth": ObtainJSONWebToken.Field(),
            "verify_token": graphql_jwt.Verify.Field(),
            "refresh_token": graphql_jwt.Refresh.Field(),
            "revoke_token": graphql_jwt.Revoke.Field(),
            "cache_user": CacheUser.Field(),
            "cache_user_by_name": CacheUserByName.Field(),
            "follow_person": Follow.Field(),
            "unfollow_person": Unfollow.Field(),
            "like_person": Like.Field(),
            "unlike_person": Unlike.Field(),
            "update_person_setting": UpdateSettings.Field(),
            "variable_store": VariableStore.Field(),
            "add_person_page_meta_link": AddPersonPageMetaLink.Field(),
            "delete_person_page_meta_link": DeletePersonPageMetaLink.Field(),
            "add_profile": esite.profile.schema.AddProfile.Field(),
            "delete_profile": esite.profile.schema.DeleteProfile.Field(),
            "update_profile": esite.profile.schema.UpdateProfile.Field(),
            "update_profile": esite.profile.schema.UpdateProfile.Field(),
            "add_talk": esite.talk.schema.AddTalk.Field(),
            "delete_talk": esite.talk.schema.DeleteTalk.Field(),
            "update_talk": esite.talk.schema.UpdateTalk.Field(),
            "add_talk_comment": esite.talk.schema.AddTalkComment.Field(),
            "delete_talk_comment": esite.talk.schema.DeleteTalkComment.Field(),
            "update_talk_comment": esite.talk.schema.UpdateTalkComment.Field(),
        }

        dict_params.update(
            (camel_case_to_spaces(n).replace(" ", "_"), mut.Field())
            for n, mut in registry.forms.items()
        )
        return dict_params

    Mutations = type("Mutation", (graphene.ObjectType,), mutation_parameters())

    return graphene.Schema(
        query=Query,
        mutation=Mutations,
        subscription=Subscription,
        types=list(registry.models.values()),
        auto_camelcase=getattr(settings, "BIFROST_AUTO_CAMELCASE", True),
    )


schema = create_schema()
