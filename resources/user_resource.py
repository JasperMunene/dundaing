from flask import request, current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from models import db
from helpers import validate_phone, rate_limited
from serializers import UserSchema

# Initialize request parser for PATCH
user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=False, location='json')
user_parser.add_argument('phone', type=str, required=False, location='json',
                         help="Phone number must be in E.164 format")
user_parser.add_argument('image', type=str, required=False, location='json',
                         help="Valid URL required for profile image")


class UserResource(Resource):
    @jwt_required()
    @rate_limited(50, 300)  # 50 requests/5 minutes
    def get(self):
        """
        Get authenticated user's profile
        ---
        tags:
          - Users
        security:
          - JWT: []
        responses:
          200:
            description: User profile data
            schema:
              $ref: '#/definitions/User'
          401:
            description: Unauthorized
          404:
            description: User not found
        """
        try:
            user_id = get_jwt_identity()
            user = User.query.get_or_404(user_id)
            return UserSchema().dump(user), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error fetching user {user_id}: {str(e)}")
            return {"message": "Database error"}, 500

    @jwt_required()
    @rate_limited(10, 300)  # 10 requests/5 minutes
    def patch(self):
        """
        Update authenticated user's profile
        ---
        tags:
          - Users
        security:
          - JWT: []
        parameters:
          - in: body
            name: body
            schema:
              id: UserUpdate
              properties:
                name:
                  type: string
                  example: John Doe
                phone:
                  type: string
                  example: +1234567890
                image:
                  type: string
                  format: url
                  example: https://example.com/profile.jpg
        responses:
          200:
            description: Updated user data
            schema:
              $ref: '#/definitions/User'
          400:
            description: Invalid input data
          401:
            description: Unauthorized
          429:
            description: Too many requests
        """
        try:
            user_id = get_jwt_identity()
            user = User.query.get_or_404(user_id)
            args = user_parser.parse_args(strict=True)

            # Validate and update fields
            update_data = {}
            if args['name'] is not None:
                update_data['name'] = args['name'].strip()

            if args['phone'] is not None:
                if not validate_phone(args['phone']):
                    return {"message": "Invalid phone format. Use E.164 format"}, 400
                update_data['phone'] = args['phone']

            if args['image'] is not None:
                if not args['image'].startswith(('http://', 'https://')):
                    return {"message": "Invalid image URL format"}, 400
                update_data['image'] = args['image']

            # Perform update
            if update_data:
                for key, value in update_data.items():
                    setattr(user, key, value)
                db.session.commit()
                current_app.logger.info(f"User {user_id} updated profile")

            return UserSchema().dump(user), 200

        except ValueError as e:
            db.session.rollback()
            current_app.logger.warning(f"Validation error for user {user_id}: {str(e)}")
            return {"message": str(e)}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error updating user {user_id}: {str(e)}")
            return {"message": "Database error"}, 500