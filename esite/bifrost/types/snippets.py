import graphene

# graphql_jwt
from graphql_jwt.decorators import login_required

from ..registry import registry


def SnippetsQuery():
    if registry.snippets:

        class SnippetObjectType(graphene.Union):
            class Meta:
                """Can change over time."""

                types = registry.snippets.types

        class Mixin:
            snippets = graphene.List(graphene.NonNull(SnippetObjectType), required=True)
            # Return all snippets.

            @login_required
            def resolve_snippets(self, info, **kwargs):
                snippet_objects = []
                for snippet in registry.snippets:
                    for object in snippet._meta.model.objects.all():
                        snippet_objects.append(object)

                return snippet_objects

        return Mixin

    else:

        class Mixin:
            pass

        return Mixin
