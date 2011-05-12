# Note: this is required:
#
# TEMPLATE_CONTEXT_PROCESSORS += (
#     'django.core.context_processors.request',
# )


from django import template
register = template.Library()

@register.tag
def url_with(parser, token):
    row = token.split_contents()
    row.pop(0)
    d = dict( zip( row[0::2], row[1::2] ) )
    return UrlWithNode(d)

class UrlWithNode(template.Node):
    def __init__(self, data):
        self.data = {}
        for k,v in data.items():
            self.data[k] = template.Variable(v)

    def render(self, context):
        path = context['request'].path
        get  = context['request'].GET.copy()
        for k, v in self.data.items():
            try:
                get[k] = v.resolve(context)
            except:
                get[k] = str(v)
        return path + '?' + get.urlencode()
