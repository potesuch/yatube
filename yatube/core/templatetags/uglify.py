from django import template

register = template.Library()


@register.filter
def uglify(text):
    result_text = []
    for i in range(len(text)):
        if i % 2:
            result_text.append(text[i].upper())
        else:
            result_text.append(text[i].lower())
    return ''.join(result_text)
