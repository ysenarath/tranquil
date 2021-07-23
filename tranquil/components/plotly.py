from tranquil.core.component import Component


def ScatterPlot(id, data_url, ref, mounted='this.refresh();'):
    return Component('plotly-scatter-plot', dict(
        template='<div v-bind:id="id"></div>',
        props=['id', 'data_url'],
        data={
            'data': [
                {
                    'x': [],
                    'y': [],
                    'type': 'scatter',
                },
            ],
            'layout': {
                'title': 'Responsive to window\'s size!',
                'font': {'size': 18},
                'height': 'auto',
            },
            'config': {'responsive': True},
        },
        methods=[
            'refresh() {Plotly.react(this.id, this.$data.data, this.$data.layout, this.$data.config);}',
            'update(data) {this.__update__(this.data_url, data, this.refresh);}',
        ],
        mounted=mounted,
    ))(id=id, data_url=data_url, ref=ref)


def Treemap(id, data_url, ref, mounted='this.refresh();'):
    return Component('plotly-treemap', dict(
        template='<div v-bind:id="id"></div>',
        props=['id', 'data_url'],
        data={
            'data': [
                {
                    'type': "treemap",
                    'labels': [],
                    'parents': []
                }
            ],
            'layout': {
                'height': 'auto',
            },
            'config': {'responsive': True},
        },
        methods=[
            'refresh() {Plotly.react(this.id, this.$data.data, this.$data.layout, this.$data.config);}',
            'update(data) {this.__update__(this.data_url, data, this.refresh);}',
        ],
        mounted=mounted,
    ))(id=id, data_url=data_url, ref=ref)
