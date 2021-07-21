from tranquil.core import Component
from tranquil.html import html


# noinspection PyShadowingBuiltins
def Navbar(brand='Navbar', items=None, id='bootstrap-navbar'):
    if items is None:
        items = []
    template = html.NAV(
        html.DIV(
            html.A(
                brand,
                html.CLASS('navbar-brand'),
                href='/',
            ),
            html.BUTTON(
                html.SPAN(html.CLASS('navbar-toggler-icon')),
                html.CLASS('navbar-toggler'),
                **{
                    'type': 'button',
                    'data-bs-toggle': 'collapse',
                    'data-bs-target': '#navbarContent',
                }
            ),
            html.DIV(
                html.UL(
                    *[
                        html.LI(html.A(item['label'], html.CLASS('nav-link active'), href=item['url'], ),
                                html.CLASS('nav-item'))
                        for item in items
                    ],
                    html.CLASS('navbar-nav me-auto mb-2 mb-lg-0'),
                ),
                html.CLASS('collapse navbar-collapse'),
                id='navbarContent',
            ),
            html.CLASS('container-fluid'),
        ),
        html.CLASS('navbar navbar-expand-lg navbar-light bg-light'),
        html.V_BIND('id', 'id'),
    )
    return Component('bootstrap-navbar', dict(
        props={
            'id': {'default': 'bootstrapNavbar'},
        },
        template=template
    ))(id=id)
