# mysite/api/graphene_wagtail.py
# Taken from https://github.com/patrick91/wagtail-ql/blob/master/backend/graphene_utils/converter.py and slightly adjusted

import string
import graphene
from wagtail.core.fields import StreamField
from graphene.types.generic import GenericScalar
from graphene.types import Scalar

from graphene_django.converter import convert_django_field
from wagtail.images.models import Image
from graphene_django import DjangoObjectType


class GenericStreamFieldType(Scalar):
    @staticmethod
    def serialize(stream_value):
        return stream_value.stream_data


@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return GenericStreamFieldType(description=field.help_text, required=not field.null)


# We're creating a fallback / default ObjectType at this point
class DefaultStreamBlock(graphene.ObjectType):
    block_type = graphene.String()
    value = GenericScalar()


# This is our factory function
# Pass in kwargs with the block's name as the
# keyword and the graphene type as its value
def create_stream_field_type(field_name, **kwargs):
    block_type_handlers = kwargs.copy()

    class Meta:
        types = (DefaultStreamBlock,) + tuple(block_type_handlers.values())

    # This is where we generate the UnionType from the kwargs
    # Different graphene types can't have the same name, so we're
    # generating this class dynamically
    StreamFieldType = type(
        f"{string.capwords(field_name, sep='_').replace('_', '')}Type",
        (graphene.Union,),
        dict(Meta=Meta),
    )

    def convert_block(block):
        block_type = block.get("type")
        value = block.get("value")
        if block_type in block_type_handlers:
            handler = block_type_handlers.get(block_type)
            if isinstance(value, dict):
                return handler(value=value, block_type=block_type, **value)
            else:
                return handler(value=value, block_type=block_type)
        else:
            return DefaultStreamBlock(value=value, block_type=block_type)

    # We also generate the resolver function for the field
    def resolve_field(self, info):
        field = getattr(self, field_name)
        return [convert_block(block) for block in field.stream_data]

    return (graphene.List(StreamFieldType), resolve_field)


class WagtailImageNode(DjangoObjectType):
    class Meta:
        model = Image
        exclude_fields = ["tags"]


@convert_django_field.register(Image)
def convert_img(field, registry=None):
    return WagtailImageNode(description=field.help_text, required=not field.null)
