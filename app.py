from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

from auth import requires_auth, AuthError
from models import setup_db
from models import Movie, Actor


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return jsonify({'Nice to meet you healthy': 'OLIVETIC INCHALLAH!!'}), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):

        try:
            selection = Movie.query.all()
            response = [movie.format() for movie in selection]

            return jsonify({
                'success': True,
                'movies': response
            }), 200
        except SQLAlchemyError:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        if not body:
            abort(400)
        try:
            title = body['title']
            release_date = body['release_date']
            if not title or not release_date:
                abort(400)
            db_movie = Movie.query.filter(Movie.title == title).one_or_none()
            if db_movie:
                abort(409)
            movie = Movie(title, release_date)
            movie.insert()
            print(movie)
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 201
        except (TypeError, KeyError):
            abort(400)
        except SQLAlchemyError:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie_id, payload):
        body = request.get_json()
        if not body:
            abort(400)
        try:
            title = body['title']
            release_date = body['release_date']
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if not movie:
                abort(404)
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200
        except (TypeError, KeyError):
            abort(400)
        except SQLAlchemyError:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id, payload):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if not movie:
                abort(404)
            movie.delete()
            return jsonify({
                'success': True,
                'deleted': movie.id
            }), 200
        except SQLAlchemyError:
            abort(422)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.all()
            response = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'actors': response
            }), 200
        except SQLAlchemyError:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        if not body:
            abort(400)
        try:
            name = body['name']
            age = body['age']
            gender = body['gender']
            if not name or not age or not gender:
                abort(400)
            db_actor = Actor.query.filter(Actor.name == name).one_or_none()

            if db_actor:
                abort(409)
            actor = Actor(name, age, gender)
            print(actor)
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201
        except (TypeError, KeyError):
            abort(400)
        except SQLAlchemyError:
            abort(422)


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(actor_id, payload):
        body = request.get_json()
        if not body:
            abort(400)
        try:
            name = body['name']
            age = body['age']
            gender = body['gender']
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if not actor:
                abort(404)
            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender
            actor.update()
            return jsonify({
                'success': True,
                'movie': actor.format()
            }), 200
        except (TypeError, KeyError):
            abort(400)
        except SQLAlchemyError:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id, payload):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if not actor:
                abort(404)
            actor.delete()
            return jsonify({
                'success': True,
                'deleted': actor.id
            }), 200
        except SQLAlchemyError:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            "success": False,
            "error": 409,
            "message": "Conflicting with other entity"
        }), 409

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run()
