from marshmallow import Schema, fields

def test():
    class UserSchema(Schema):
        # `Method` takes a method name (str), Function takes a callable
        balance = fields.Method('get_balance', deserialize='load_balance')

        def get_balance(self, obj):
            print(obj)
            return obj.income - obj.debt

        def load_balance(self, value):
            print(value)
            return float(value)


    schema = UserSchema()
    result = schema.load({'balance': '100.00'})
# pass
# result['balance']  # => 100.0

