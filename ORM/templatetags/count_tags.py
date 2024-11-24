from django import template
from django.apps import apps

register = template.Library()


@register.simple_tag
def count_records(model_name):
    Model = apps.get_model("ORM", model_name)
    return Model.objects.count()
