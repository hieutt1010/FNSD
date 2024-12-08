from flask import Flask, abort, request, jsonify
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path)
        
    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")

        return response

    @app.route('/',methods=['GET'])
    def hello():
        return "hello"

    # region Movie
    
    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def get_movies(payload):
        if payload is None: 
            abort(401)
        if payload in [400,403]: 
            abort(payload)
        try:
            movies = Movie.query.all()
            format_movie = [movie.format() for movie in movies]
            return jsonify({
                'movies': format_movie,
                'totalMovies': len(format_movie)
            })
        except:
            abort(404)
            
    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('read:movies')
    def get_movie(payload,id):
        if payload is None: 
            abort(401)
        if payload in [400,403]: 
            abort(payload)
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if not movie:
                return jsonify({"message": "Movie not found"}), 404
            
            return jsonify({
                'movies': movie.format(),
                'message': True
            })
        except:
            abort(404)
    
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def add_movie(payload):
        if payload is None: 
            abort(401)
        if payload in [400,403]: 
            abort(payload)
        try: 
            body = request.get_json()
            movie = Movie(
                title = body['title'],
                release_date = body['release_date']
            )
            movie.insert()
            
            return jsonify({
                'movie': movie.format(),
                'success': True
            })
        except:
            abort(400)
            
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('modify:movies')
    def update_movie(payload, id):
        if payload is None: 
            abort(401)
        if payload in [400,403]: 
            abort(payload)
        try:            
            data = request.get_json()
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            
            if not movie:
                return jsonify({"message": "Movie not found"}), 404

            # Update movie fields based on provided data
            if 'title' in data:
                movie.title = data['title']
            if 'release_date' in data:
                movie.release_date = data['release_date']
            
            movie.update()
            
            return jsonify({
                'movie': movie.format(),
                'message': True
            })
        except:
            return jsonify({"message": "create movie fail"})

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        if payload is None: 
            abort(401)
        if payload in [400,403]: 
            abort(payload)
        try:   
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            
            if not movie:
                return jsonify({"message": "Movie not found"}), 404
            
            movie_remove = movie
            movie.delete()

            return jsonify({
                'movie': movie_remove.format(),
                "success": True
                })
        except Exception as e:
            return jsonify({f"Error occurred: {e}"})

    # endregion
    
    #region Actors
    
    @app.route('/actors', methods=['GET'])
    @requires_auth('read:actors')
    def get_actors(payload):
        if payload is None: 
            abort(401)
        if payload in [400,403]: 
            abort(payload)
            
        try:
            actors = Actor.query.order_by(Actor.id).all()
            format_actors = [actor.format() for actor in actors]
            return jsonify({
                'actors': format_actors,
                'totalActors': len(format_actors)
            })
        except:
            abort(404)
            
    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('read:actors')
    def get_actor(payload, id):
        if payload is None: 
            abort(401)
        if payload in [400,403]: 
            abort(payload)
            
        try:
            actors = Actor.query.filter(Actor.id == id).one_or_none()
            if not actors:
                return jsonify({"message": "Actor not found"}), 404
            
            return jsonify({
                'actors': actors.format(),
                'message': True
            })
        except:
            abort(404)
    
    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def add_actor(payload):
        if payload is None: 
            abort(401)
        if payload in [400,403]: 
            abort(payload)
        try:     
            body = request.get_json()
            movie_id = body['movie_id']
            if movie_id is not None:
                movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
                if movie is None:
                    return jsonify({"message": "movie not found"}), 404
                
                actor = Actor(
                    name = body['name'], 
                    age = body['age'], 
                    gender = body['gender'],
                    movie_id = movie_id,
                    movie = movie
                )
                actor.insert()
                return jsonify({
                    'actor': actor.format(),
                    'success': True
                })
            else:
                return jsonify({"message": "movie_id not found"}), 404
        except Exception as e:
            return jsonify({f"Error occurred: {e}"})
    
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('modify:actors')
    def update_actor(payload,id):
        if payload is None: 
            abort(401)
        if payload in [400,403]: 
            abort(payload)
            
        try:
            data = request.get_json()
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            
            if not actor:
                return jsonify({"message": "Actor not found"}), 404

            # Update actor fields based on provided data
            if 'name' in data:
                actor.name = data['name']
            if 'age' in data:
                actor.age = data['age']
            if 'gender' in data:
                actor.gender = data['gender']
            
            actor.update()
            return jsonify({
                    'actor': actor.format(),
                    'success': True
                })
        except:
            abort(404)
            
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        if payload is None: 
            abort(401)
        if payload in [400,403]: 
            abort(payload)
        try: 
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            
            if actor is None :
                return jsonify({"message": "Actor not found"}), 404
            actor.delete()
            
            return jsonify({
                'actors_deleted_id': actor.id,
                "message": True
                })
        except Exception as e:
            return jsonify({f"Error occurred: {e}"})
            
            
            
    #region ErrorHandler
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request."}),
            400,
        )
        
    @app.errorhandler(401)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 401, "message": "Unauthorized"}),
            401,
        )
            
    @app.errorhandler(403)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 403, "403": "Forbidden"}),
            403,
        )
        
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    #end region
    
    return app

app = create_app()
if __name__ == '__main__':
    app.run()