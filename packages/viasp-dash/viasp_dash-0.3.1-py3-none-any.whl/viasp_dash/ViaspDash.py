# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ViaspDash(Component):
    """A ViaspDash component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- colors (dict; optional):
    Colors to be used in the application."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, colors=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'colors']
        self._type = 'ViaspDash'
        self._namespace = 'viasp_dash'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'colors']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ViaspDash, self).__init__(**args)
