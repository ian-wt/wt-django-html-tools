import bleach
from bs4 import BeautifulSoup

from django.utils.safestring import mark_safe
from django.conf import settings

from .tags import (
    CONTENT_SECTIONING_TAGS, TEXT_CONTENT_TAGS, INLINE_TEXT_SEMANTICS_TAGS, IMAGE_AND_MULTIMEDIA_TAGS, SCRIPTING_TAGS
)

DEFAULT_TAGS = {
    'CONTENT_SECTIONING_TAGS': CONTENT_SECTIONING_TAGS,
    'TEXT_CONTENT_TAGS': TEXT_CONTENT_TAGS,
    'INLINE_TEXT_SEMANTICS_TAGS': INLINE_TEXT_SEMANTICS_TAGS,
    'IMAGE_AND_MULTIMEDIA_TAGS': IMAGE_AND_MULTIMEDIA_TAGS,
    'SCRIPTING_TAGS': SCRIPTING_TAGS
}


def get_tags(bleach_all=False, include_defaults=False, **kwargs):
    """
    Where to look for tags:
        (1) tags provided locally,
        (2) tags provided in settings.py, and
        (3) fall back to the defaults
    """
    if bleach_all:
        return ()  # don't allow any tags

    tag_set = {}

    for k, v in kwargs.items():
        if k.endswith('_TAGS'):
            if isinstance(v, dict):
                tag_set.update(**{k: v})
            else:
                raise TypeError(f"Provided tag set {k} must be a dictionary.")

    if not tag_set:
        # the user didn't pass any tag sets directly, so check if in settings
        tag_set = getattr(settings, 'WT_DJANGO_BLEACH_TAGS', {})

    if include_defaults:
        # include defaults
        # prefer custom over default where overlap exists
        DEFAULT_TAGS.update(**tag_set)
        tag_set = DEFAULT_TAGS

    # dictionary needs to be 'flattened
    flat_dict = {}
    for _, v in tag_set.items():
        # lose the key name
        if isinstance(v, dict):
            flat_dict.update(**v)
    return flat_dict

def sanitize_html(html, tags=None, bleach_all=False, strip=True, include_defaults=False, **kwargs):

    if not isinstance(html, str):
        raise TypeError("Expected type 'str' for provided html.")

    # build a dictionary of allowed tags, if one hasn't been provided explicitly
    tags = get_tags(bleach_all=bleach_all, include_defaults=include_defaults, **kwargs) if not tags else tags

    # bleach the html
    html = mark_safe(
        bleach.clean(
            html,
            tags=tags.keys(),
            attributes=dict([(key, value.keys()) for key, value in tags.items()]),
            strip=strip  # if not true, tags will be escaped and not removed
        )
    )

    return html

def set_html_attribute_defaults(html, tags=None, bleach_all=False, include_defaults=False, **kwargs):

    def _add_attr(content, tag, attr, new_value):
        soup = BeautifulSoup(content, 'html.parser')
        for element in soup.find_all(tag):
            attr_values = element.get(attr, [])
            if new_value not in attr_values:
                attr_values.append(new_value)
                element[attr] = " ".join(attr_values)
        return str(soup)

    tags = get_tags(bleach_all=bleach_all, include_defaults=include_defaults, **kwargs) if not tags else tags

    # add any desired default attributes
    for tgt_tag, attr_dict in tags.items():
        if not isinstance(attr_dict, dict):
            raise TypeError(f"Provided attrs for tag {tgt_tag} must be a dictionary.")
        for attr_key, attr_value in attr_dict.items():
            if isinstance(attr_value, (set, list, tuple)):
                for item in attr_value:
                    html = _add_attr(html, tgt_tag, attr_key, item)
            else:
                if attr_value:
                    html = _add_attr(html, tgt_tag, attr_key, attr_value)
