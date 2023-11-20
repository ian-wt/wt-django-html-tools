import functools

from .functions import get_tags, sanitize_html, set_html_attribute_defaults


def sanitize(bleach_all=False, strip=True, include_defaults=False, **k):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # func should be a field's clean method of class Django Form
            # start by sanitizing
            value = sanitize_html(
                func(*args, **kwargs),  # the html part
                bleach_all=bleach_all,
                strip=strip,
                include_defaults=include_defaults,
                **k
            )
            return value
        return wrapper
    return decorator


def set_attribute_defaults(bleach_all=False, include_defaults=False, **k):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # now set defaults
            value = set_html_attribute_defaults(
                func(*args, **kwargs),
                bleach_all=bleach_all,
                include_defaults=include_defaults,
                **k
            )
            return value
        return wrapper
    return decorator


def sanitize_and_set_attribute_defaults(bleach_all=False, strip=True, include_defaults=False, **k):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tags = get_tags(bleach_all=bleach_all, include_defaults=include_defaults, **k)
            value = sanitize_html(
                func(*args, **kwargs),
                tags=tags,
                bleach_all=bleach_all,
                strip=strip,
                include_defaults=include_defaults,
                **k
            )
            # now set defaults
            value = set_html_attribute_defaults(
                value,
                tags=tags,
                bleach_all=bleach_all,
                include_defaults=include_defaults,
                **k
            )
            return value
        return wrapper
    return decorator
