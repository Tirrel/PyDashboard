from dash_extensions.enrich import MultiplexerTransform, DashProxy

app = DashProxy(
    __name__,
    suppress_callback_exceptions=True,
    transforms=[MultiplexerTransform()],
    meta_tags=[
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        }
    ]
)

server = app.server
