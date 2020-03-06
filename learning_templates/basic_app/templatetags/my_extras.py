from django import template

register = template.Library()

#another way to register the filter

@register.filter(name = 'cut')
def cut(value,arg):
    """
    This cuts out all the values of "arg" from the string!
    """

    return value.replace(arg,'')

#register.filter('cut',cut)