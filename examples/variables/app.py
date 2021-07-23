import json

from tranquil import Tranquil

from tranquil.core import Var

app = Tranquil()

print(app.state.input_1.val)

print(app.state.to_dict())

print(json.dumps(Var('state.acv')))
