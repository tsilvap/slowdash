from datetime import datetime

from flask import Flask, render_template, send_from_directory
from flask_restful import Resource, Api, abort, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder="./client/dist")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://yura@/slowdash"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


##
## Blog Model
##


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User '{username}'>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post '{self.title}'>"


##
## Blog API
##

user_fields = {"username": fields.String, "email": fields.String}

post_fields = {
    "title": fields.String,
    "body": fields.String,
    "pub_date": fields.DateTime,
}


def abort_if_post_doesnt_exist(post_id):
    if not Post.query.filter_by(id=post_id).first():
        abort(404, message=f"Post {post_id} doesn't exist.")


parser = reqparse.RequestParser()
parser.add_argument("title", type=str, help="Post title")
parser.add_argument("body", type=str, help="Post content")


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


api.add_resource(PostList, "/api/blog/posts")
api.add_resource(PostInstance, "/api/blog/posts/<int:post_id>")


@app.route("/<path:path>")
def send_static(path):
    return send_from_directory("./client/dist", path)
