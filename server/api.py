from flask_restful import Resource, abort, fields, marshal_with, reqparse

from slowdash.app import api
from slowdash.server.models import User, Post


# Fields
user_fields = {"username": fields.String, "email": fields.String}
post_fields = {
    "title": fields.String,
    "body": fields.String,
    "pub_date": fields.DateTime,
}


# Middleware
def abort_if_post_doesnt_exist(post_id):
    if not Post.query.filter_by(id=post_id).first():
        abort(404, message=f"Post {post_id} doesn't exist.")


# Parser
parser = reqparse.RequestParser()
parser.add_argument("title", type=str, help="Post title")
parser.add_argument("body", type=str, help="Post content")


# Endpoints
class PostList(Resource):
    @marshal_with(post_fields)
    def get(self):
        return Post.query.all()

    @marshal_with(post_fields)
    def post(self):
        args = parser.parse_args()
        post = Post(title=args["title"], body=args["body"])
        db.session.add(post)
        db.session.commit()
        return post, 201


class PostInstance(Resource):
    @marshal_with(post_fields)
    def get(self, post_id):
        abort_if_post_doesnt_exist(post_id)
        return Post.query.filter_by(id=post_id).first()

    @marshal_with(post_fields)
    def put(self, post_id):
        abort_if_post_doesnt_exist(post_id)
        args = parser.parse_args()
        post = Post.query.filter_by(id=post_id).first()
        post.title = args["title"]
        post.body = args["body"]
        db.session.add(post)
        db.session.commit()
        return post, 201

    def delete(self, post_id):
        abort_if_post_doesnt_exist(post_id)
        post = Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return "", 204


# Endpoint registration
api.add_resource(PostList, "/api/blog/posts")
api.add_resource(PostInstance, "/api/blog/posts/<int:post_id>")
