from flask import Flask
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_caching import Cache
from dotenv import load_dotenv
from flask_cors import CORS
import redis
import os
from models import db
from flask_jwt_extended import JWTManager
from resources.auth_resource import (
    SignupResource, VerifyOTPResource, LoginResource, GoogleLogin,
    GoogleAuthorize, GoogleOAuth, ResendOTPResource,
    ForgotPasswordResource, ResetPasswordResource
)
from datetime import timedelta
from authlib.integrations.flask_client import OAuth
from extensions import bcrypt

from resources.user_resource import UserResource

# Load environment variables
load_dotenv()

def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        RESEND_API_KEY=os.getenv("RESEND_API_KEY"),
        SQLALCHEMY_DATABASE_URI=os.getenv("CONNECTION_STRING"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key"),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        FRONTEND_URL=os.getenv("FRONTEND_URL", "http://localhost:3000"),
        CACHE_TYPE="RedisCache",
        CACHE_REDIS_URL=os.getenv("UPSTASH_REDIS_URL", "redis://localhost:6379/0")
    )

    # Extensions
    bcrypt.init_app(app)
    db.init_app(app)
    jwt = JWTManager(app)
    cache = Cache(app)
    app.cache = cache
    app.redis = redis.Redis.from_url(app.config["CACHE_REDIS_URL"], decode_responses=True)
    migrate = Migrate(app, db)
    CORS(app)

    # OAuth setup
    oauth = OAuth(app)
    google_oauth = GoogleOAuth(oauth, app.config['FRONTEND_URL'])

    # API setup
    api = Api(app)

    # Health check endpoint
    class HealthCheck(Resource):
        def get(self):
            try:
                app.redis.ping()
                return {"status": "healthy", "redis": "connected"}, 200
            except redis.ConnectionError:
                return {"status": "healthy", "redis": "disconnected"}, 200

    api.add_resource(HealthCheck, '/health')

    # Auth routes
    api.add_resource(SignupResource, '/api/v1/auth/signup')
    api.add_resource(VerifyOTPResource, '/api/v1/auth/verify-otp')
    api.add_resource(LoginResource, '/api/v1/auth/login')
    api.add_resource(GoogleLogin, '/api/v1/auth/login/google', resource_class_args=[google_oauth])
    api.add_resource(GoogleAuthorize, '/api/v1/auth/authorize/google', endpoint='authorize_google',
                     resource_class_args=[google_oauth])
    api.add_resource(ResendOTPResource, '/api/v1/auth/resend-otp')
    api.add_resource(ForgotPasswordResource, '/api/v1/auth/forgot-password')
    api.add_resource(ResetPasswordResource, '/api/v1/auth/reset-password')

    api.add_resource(UserResource, '/api/v1/users/me')

    return app  # Important for WSGI servers and testability


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
