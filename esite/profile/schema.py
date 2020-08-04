from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required, permission_required, staff_member_required, superuser_required

from wagtail.core.models import Page

from esite.user.models import User
from esite.profile.models import ProfilePage
from esite.customer.models import Customer
from esite.registration.schema import UserType

# Create your registration related graphql schemes here.

#class UserType(DjangoObjectType):
#    class Meta:
#        model = User
#        exclude_fields = ['password']


class UpdateProfile(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        token = graphene.String(required=False)
        platform_data = graphene.String(required=True)
        telephone = graphene.String(required=False)
        address = graphene.String(required=False)
        city = graphene.String(required=False)
        postal_code = graphene.String(required=False)
        email = graphene.String(required=False)
        country = graphene.String(required=False)
        newsletter = graphene.String(required=False)
        platform_data = graphene.String(required=False)
        education_data = graphene.String(required=False)
        sources = graphene.String(required=False)
        verified = graphene.String(required=False)
        available_for_hire = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        website = graphene.String(required=False)
        company = graphene.String(required=False)

    @login_required
    def mutate(self, info, token, telephone, address, city, postal_code, email, country, newsletter, education_data, sources, verified, available_for_hire, first_name, last_name, website, company):
        user = info.context.user

        profile_page = Page.objects.get(slug=f"{user.username}").specific

        #profile_page.birthdate = birthdate
        profile_page.telephone = telephone
        profile_page.address = address
        profile_page.city = city
        profile_page.postal_code = postal_code
        profile_page.email = email
        profile_page.country = country
        profile_page.newsletter = newsletter
        profile_page.education_data = education_data
        profile_page.sources = sources
        profile_page.verified = verified
        profile_page.available_for_hire = available_for_hire
        profile_page.first_name = first_name
        profile_page.last_name = last_name
        profile_page.website = website
        profile_page.company = company

        profile_page.platform_data = platform_data

        profile_page.save_revision().publish()

        return UpdateProfile(user=user)

class Mutation(graphene.ObjectType):
    update_profile = UpdateProfile.Field()
