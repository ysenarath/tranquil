from tranquil import Tranquil

app = Tranquil()

print(app.state.input_1.val)

print(app.state.to_dict())
