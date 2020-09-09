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

from esite.comment.models import Comment
from esite.people.models import PersonPage
from esite.talk.models import Talk

# Create your registration related graphql schemes here.


class TalkType(DjangoObjectType):
    class Meta:
        model = Talk


class AddTalk(graphene.Mutation):
    talk = graphene.Field(TalkType)

    class Arguments:
        token = graphene.String(required=True)
        person_name = graphene.String(required=True)
        title = graphene.String(required=True)
        description = graphene.String(required=False)
        path = graphene.String(required=False)
        url = graphene.String(required=False)
        display_url = graphene.String(required=False)
        download_url = graphene.String(required=False)

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

        talk = Talk.objects.create(owner=person_page, **kwargs)

        return AddTalk(talk=talk)


class DeleteTalk(graphene.Mutation):
    talks = graphene.List(TalkType)

    class Arguments:
        token = graphene.String(required=True)
        talk_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, token, talk_id, **kwargs):
        user = info.context.user

        if user.is_superuser:
            talks = Talk.objects.filter(id=talk_id)
        else:
            talks = Talk.objects.filter(id=talk_id, owner__person__user=user)

        talk = talks.first()

        if not talk:
            raise GraphQLError("talk_id not valid for user")

        talk.delete()

        return DeleteTalk(talks=Talk.objects.filter(owner__person__user=user))


class UpdateTalk(graphene.Mutation):
    talk = graphene.Field(TalkType)

    class Arguments:
        token = graphene.String(required=True)
        talk_id = graphene.ID(required=True)
        title = graphene.String(required=False)
        description = graphene.String(required=False)
        path = graphene.String(required=False)
        url = graphene.String(required=False)
        display_url = graphene.String(required=False)
        download_url = graphene.String(required=False)

    @login_required
    def mutate(self, info, token, talk_id, **kwargs):
        user = info.context.user

        if user.is_superuser:
            talks = Talk.objects.filter(id=talk_id)
        else:
            talks = Talk.objects.filter(id=talk_id, owner__person__user=user)

        if not talks.first():
            raise GraphQLError("profile_id not valid")

        talks.update(**kwargs)

        return UpdateTalk(talk=talks.first())


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        # Exclude all keys which are not realted to a talk
        exclude_fields = []


class AddTalkComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        token = graphene.String(required=True)
        person_name = graphene.String(required=True)
        talk_id = graphene.ID(required=True)
        reply_to_id = graphene.ID(required=False)
        text = graphene.String(required=False)

    def mutate(self, info, token, person_name, talk_id, reply_to_id, **kwargs):
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

        talk = Talk.objects.get(id=talk_id)

        if not talk:
            raise GraphQLError("Talk not found")

        reply_to_comment = Comment.objects.get(id=reply_to_id, talk=talk)

        if not reply_to_comment:
            raise GraphQLError("Comment to be replied not found")

        comment = Comment.objects.create(
            reply_to=reply_to_comment, talk=talk, author=person_page, **kwargs
        )

        return AddTalkComment(comment=comment)


class DeleteTalkComment(graphene.Mutation):
    comments = graphene.List(CommentType)

    class Arguments:
        token = graphene.String(required=True)
        comment_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, token, talk_id, comment_id, **kwargs):
        user = info.context.user

        if user.is_superuser:
            comments = Comment.objects.filter(id=comment_id)
        else:
            comments = Comment.objects.filter(id=comment_id, author__person__user=user)

        comment = comments.first()

        if not comment:
            raise GraphQLError("comment_id not valid for user")

        talk = comment.talk

        comment.delete()

        return DeleteTalkComment(
            comments=talk.talk_comments.filter(author__person__user=user)
        )


class UpdateTalkComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        token = graphene.String(required=True)
        comment_id = graphene.ID(required=True)
        text = graphene.String(required=False)

    @login_required
    def mutate(self, info, token, talk_id, comment_id, **kwargs):
        user = info.context.user

        if user.is_superuser:
            comments = Comment.objects.filter(id=comment_id)
        else:
            comments = Comment.objects.filter(id=comment_id, author__person__user=user)

        comment = comments.first()

        if not comment:
            raise GraphQLError("comment_id not valid for user")

        comments.update(**kwargs)

        return UpdateTalkComment(comment=comment)


class Mutation(graphene.ObjectType):
    add_talk = AddTalk.Field()
    delete_talk = DeleteTalk.Field()
    update_talk = UpdateTalk.Field()
    add_talk_comment = AddTalkComment.Field()
    delete_talk_comment = DeleteTalkComment.Field()
    update_talk_comment = UpdateTalkComment.Field()


class Query(graphene.ObjectType):
    talk = graphene.Field(
        TalkType, token=graphene.String(required=True), id=graphene.Int(required=True)
    )
    talks = graphene.List(
        TalkType,
        token=graphene.String(required=True),
        person_name=graphene.String(required=False),
    )

    @login_required
    def resolve_talk(self, info, token, id, **kwargs):
        try:
            return Talk.objects.get(id=id)
        except Talk.DoesNotExist:
            raise GraphQLError("Id not valid")

    @login_required
    def resolve_talks(self, info, token, person_name=None, **kwargs):
        try:
            person_page = PersonPage.objects.get(slug=f"p-{person_name}")

            return Talk.objects.filter(owner=person_page)
        except PersonPage.DoesNotExist:
            return Talk.objects.all()

