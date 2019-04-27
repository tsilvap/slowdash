from flask import Flask, render_template, send_from_directory
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__, template_folder="./client/dist")
api = Api(app)


@app.route("/")
def index():
    return render_template("index.html")


##
## Blog API
##


def getDate():
    from datetime import datetime

    return datetime.today().isoformat()


POSTS = {
    1: {
        "title": "My First Blog Post",
        "description": "Hey, I can post whatever I want",
        "timestamp": getDate(),
    }
}

COUNT = 2


def abort_if_post_doesnt_exist(post_id):
    if post_id not in POSTS:
        abort(404, message=f"Post {post_id} doesn't exist")


parser = reqparse.RequestParser()
parser.add_argument("title", type=str, help="Post title")
parser.add_argument("description", type=str, help="Post description")


class PostList(Resource):
    def get(self):
        return POSTS

    def post(self):
        args = parser.parse_args()

        global COUNT
        post_id = COUNT
        COUNT += 1
        post = {
            "title": args["title"],
            "description": args["description"],
            "timestamp": getDate(),
        }
        POSTS[post_id] = post
        return post, 201


class Post(Resource):
    def get(self, post_id):
        abort_if_post_doesnt_exist(post_id)
        return POSTS[post_id]

    def put(self, post_id):
        abort_if_post_doesnt_exist(post_id)
        args = parser.parse_args()
        post = {
            "title": args["title"],
            "description": args["description"],
            "timestamp": getDate(),
        }
        POSTS[post_id] = post
        return post, 201

    def delete(self, post_id):
        abort_if_post_doesnt_exist(post_id)
        del POSTS[post_id]
        return "", 204


api.add_resource(PostList, "/api/blog/posts")
api.add_resource(Post, "/api/blog/posts/<int:post_id>")


@app.route("/<path:path>")
def send_static(path):
    return send_from_directory("./client/dist", path)


if __name__ == "__main__":
    app.run(debug=True)
