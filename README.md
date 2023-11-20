# WT Django HTML Tools
Waldron Technologies, LLC

## Overview

This project represents the first step at collecting tools I use with Django forms handling html content.

The project extends the functionality of the bleach and bs4 packages.

## Decorators
Implement by decorating a Django form field's clean method. The decorators accept the following arguments:
* @sanitize
  * bleach_all=False: If True, all html tags will be striped/escaped,
  * strip=True: Determines whether to strip or escape,
  * include_defaults=False: Determines whether the default sets in tags.py should be used as a starting point for determining allowed tags, and
  * **k: Pass any custom tag sets as kwargs and postfix the variables with "_TAGS" so it's know these should be considered as tags.
* @set_attribute_defaults
  * bleach_all=False: see above,
  * include_defaults: see above, and
  * **k: see above.
* @sanitize_and_set_attribute_defaults
  * (incorporates the previous two decorators)

## Use
```
from wt-django-html-tools.decorators import sanitize_and_set_attribute_defaults
from django import forms

ALLOWED_TAGS = {
    'CONTENT_TAGS': {
        'p': {'class': 'my-class'}
    }
}

class MyForm(forms.Form):
    my_field = forms.TextField()  # html
    
    @sanitize_and_set_attribute_defaults(**CONTENT_TAGS)
    def clean_my_field(self):
        return self.cleaned_data['my_field']
```
In this block, we define a tag-set containing the paragraph (p) tag. Any html submitted to this field will be sanitized of anything that's not a paragraph tag. Additionally, the attribute 'class' was provided a default value of 'my-class.' Any paragraph tags discovered will be provided this class if the tag doesn't already contain it. Additional values already contained by the class will be preserved.

## License

This project is licensed under the BSD 3-Clause license.