from django import template
from menus.models import Menu


register = template.Library()

@register.inclusion_tag('menus/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path

    try:
        menu = Menu.objects.prefetch_related('items__children').get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_tree': []}

    all_items = menu.items.all()

    def build_tree(items, parent=None):
        return [
            {
                'item': item,
                'url': item.get_url(),
                'children': build_tree(items, parent=item),
                'active': item.get_url() == current_path,
                'show': True
            }
            for item in items if item.parent == parent
        ]

    tree = build_tree(all_items)
    return {'menu_tree': tree}