from tranquil import html


def Navbar(brand='Navbar', items=None, is_fluid=True, theme='dark'):
    if items is None:
        items = []
    _fluid = ('-fluid' if is_fluid else '')
    brand_href = brand['href'] if isinstance(brand, dict) and ('href' in brand) else '#'
    return html.NAV(
        html.DIV(
            html.A(brand, href=brand_href, _class='navbar-brand'),
            html.BUTTON(
                html.SPAN(_class='navbar-toggler-icon'),
                type='button', _class='navbar-toggler',
                **{'data-bs-toggle': 'collapse', 'data-bs-target': '#navbarSupportedContent'},
                **{'aria-controls': 'navbarSupportedContent', 'aria-expanded': 'false',
                   'aria-label': 'Toggle navigation'}
            ),
            html.DIV(
                html.UL(
                    *(html.LI(
                        html.A(item['name'], href=item['href'],
                               _class='nav-link rounded-3 shadow ps-3 pe-3' +
                                      (' active' if ('active' in item) and item['active'] else ''),
                               **{'aria-current': 'page'}),
                        _class='nav-item me-1'
                    ) for item in items if ('align' not in item) or item['align'] == 'left'),
                    _class='navbar-nav me-auto mb-2 mb-lg-0'
                ),
                html.UL(
                    *(html.LI(
                        html.A(item['name'], href=item['href'],
                               _class='nav-link rounded-3 shadow ps-3 pe-3' +
                                      (' active' if ('active' in item) and item['active'] else ''),
                               **{'aria-current': 'page'}),
                        _class='nav-item ms-1'
                    ) for item in items if ('align' in item) and item['align'] == 'right'),
                    _class='navbar-nav mb-2 mb-lg-0 ms-auto'
                ),
                id='navbarSupportedContent',
                _class='collapse navbar-collapse'
            ),
            _class=f'container{_fluid}'
        ),
        _class=f'navbar navbar-expand-lg navbar-{theme} bg-{theme}'
    )
