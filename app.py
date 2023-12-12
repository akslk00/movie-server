from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required
from flask_restful import Api
from config import Config
from resources.movie import MovieReResources, MovieReviewResources, MoviesResources
from resources.review import MyReviewResources, ReviewResources
from resources.user import UserListResoyrces, UserLoginResource, UserLogoutResource

from resources.user import jwt_blocklist


app = Flask(__name__)



app.config.from_object(Config)

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header,jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist


api = Api(app)


api.add_resource(UserListResoyrces,'/movie/user')

api.add_resource(UserLoginResource,'/user/login')

api.add_resource(UserLogoutResource,'/user/logout')

api.add_resource(MoviesResources,'/movie/<int:move_Id>')

api.add_resource(MovieReResources,'/movie/re')

api.add_resource(MovieReviewResources,'/movie/review/<int:move_Id>')

api.add_resource(ReviewResources,'/movie/<int:moveId>/review')

api.add_resource(MyReviewResources,'/review/me')

if __name__ == '__main__':
    app.run()