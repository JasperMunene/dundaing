from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self):
        # Example response data
        user_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
            "image": "https://example.com/image.jpg",
            "role": "admin",
            "verified": True
        }
        return user_data, 200

api.add_resource(User, '/user')

if __name__ == '__main__':
    app.run(debug=True)