from django import template

register = template.Library()

@register.filter(name='br_len')
def br_len(member):
    lines = [member.name, member.title, member.department, member.year]
    return range(sum(map(lambda x: 0 if x else 1 ,lines)))