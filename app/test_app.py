import os
import unittest
import json
from flask import request
from flask_sqlalchemy import SQLAlchemy
from models import Movie, Actor, db as database
from __init__ import create_app
from dotenv import load_dotenv
    
class FlaskAppTestCase(unittest.TestCase):
    
    load_dotenv()
    database_path = os.getenv('DATABASE_URL_TEST')
    # this token is full permission
    bearer_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhKSkUzMXVCYmVrbFpnMDdxOVQxZyJ9.eyJpc3MiOiJodHRwczovL2hpZXV0dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8Njc0YmZjZjQ1ZWM4NGQzNzJhZDU2Zjg2IiwiYXVkIjoiRlNORF9JbWFnZSIsImlhdCI6MTczMzU1MjI0OCwiZXhwIjoxNzMzNTg4MjQ4LCJzY29wZSI6IiIsImF6cCI6ImF0V3JIODZXMHlOdFhlOEk0c0d5d016elRuOERFR3VNIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsIm1vZGlmeTphY3RvcnMiLCJtb2RpZnk6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.25UMFFj8GrthRgCHxvlYFgguyL4wwFS_orUgzoqoJDUeaPaV1Z48xoTuOtLf5YmGTXmSKOiMwRrbIpuQh66_c3S0R318C5xIum6iydalHXmDBjF3MKjs0jq-893WB8f2pLx-VB_9oXtoMUw62sqpqtUvFf72mUQud43ZTsNFlnB5jd4WbHsRtNnjQk6sldtaULYoPI-A1qqu6KJVe7Zl9pwxlr7wZB7lB7W5xfBMGO8qIm-9c7q8dX8UNkwmChoFj_zGdyA8CoU3naknne9GnU7YnpM_LsdIbDHa_Ax5h2poP_9sKkV95k2ohRagCJpjoq6_LFVOv2JWLTCNhTE_fA'
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })
        
        # setup for RBAC testing
        self.tokens = {
            "casting_assistant": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhKSkUzMXVCYmVrbFpnMDdxOVQxZyJ9.eyJpc3MiOiJodHRwczovL2hpZXV0dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjZmYTRiOGM3YjIyZGM3ZGM0ODAxN2M4IiwiYXVkIjoiRlNORF9JbWFnZSIsImlhdCI6MTczMzU1OTgxMSwiZXhwIjoxNzMzNTk1ODExLCJzY29wZSI6IiIsImF6cCI6ImF0V3JIODZXMHlOdFhlOEk0c0d5d016elRuOERFR3VNIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.XEWL1ovEftV2Q_mShMgqULa944eOJu4RWtNHZSXKJ3ybiTXSEr07VQRz78oJYwpSb3nBgmEWn0H8ts6Jf753MXEfCeKM1sMZY1fFedMMq_Lk8RRMNaZKDwthI28kAPxB0ztNozjnWQHdssRJEZWSXF6iTAYAUe99cInQ9r_XvbX1RBShC32fHTuRzn9AP4yBh8mGRc1WmQvzuPNp2JN7BaQn07SBjQ3Dv76oxM4NeMdoMy5Yj19DEE2AlcTuxavCoSKZxKwNE2417a-4pz2CkZWA_qH5E4321KjtQSBQlKlbd8C79baR6tgfLx_LnjrS_7hVMA3J_A14rpZhemhb4Q",
            "casting_director": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhKSkUzMXVCYmVrbFpnMDdxOVQxZyJ9.eyJpc3MiOiJodHRwczovL2hpZXV0dC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTYzMTUxNjcwNDQ4MDUyNDYxNDgiLCJhdWQiOiJGU05EX0ltYWdlIiwiaWF0IjoxNzMzNTU5ODc1LCJleHAiOjE3MzM1OTU4NzUsInNjb3BlIjoiIiwiYXpwIjoiYXRXckg4NlcweU50WGU4STRzR3l3TXp6VG44REVHdU0iLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsIm1vZGlmeTphY3RvcnMiLCJtb2RpZnk6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.NgtD4-g0oHA35w7I_Y69c4FVp8G-c3zicqGNbZLWMW9De64-J1b7C788vvLzez6rfi_KyWCOGelK-OqJ_zgr8TURaepnhlc3PIbtG5kWH3twZT-UmcYJQePGZ_0Tmrfr3hj56KLUtd0RHjQpqTxCyXfLpTTT3LIEgZop1gm4oozwdBZpapS55zw9CyZEx5QIhjrKNuMCd51Z1XdnWq89eQihn1LCJQPQOgvwPesCZ0UekwLdVa_zEBdGgzXt2D5BxV4GngJERfnRHwpr91AP0EVawyJgxM_siHdZ4sC8seTXgN3A0mLFY7ZewPMNK3VGvFg6dhNfdG7nP1K2f7wquw",
            "executive_producer": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhKSkUzMXVCYmVrbFpnMDdxOVQxZyJ9.eyJpc3MiOiJodHRwczovL2hpZXV0dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8Njc0YmZjZjQ1ZWM4NGQzNzJhZDU2Zjg2IiwiYXVkIjoiRlNORF9JbWFnZSIsImlhdCI6MTczMzU1OTkzMywiZXhwIjoxNzMzNTk1OTMzLCJzY29wZSI6IiIsImF6cCI6ImF0V3JIODZXMHlOdFhlOEk0c0d5d016elRuOERFR3VNIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsIm1vZGlmeTphY3RvcnMiLCJtb2RpZnk6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.eDhUPuahunYTdT_lRhy3wkPA3mpatC55OLV10jxf6ggIrsCgC_uaz2QjNrHpN2ZdFps61-l_rfvk34qS7UV84_pfrO6Ilt6XVbqWb8pV2jtuzQ8igMcjxXeBUUeZ0mwpWrC3EMBolb2n3b5QUQdgka5lD4kgk10dTFxtoKlksyDGNB5LJ4EjQzGHx5p1HpIrLOoB3KBaZLm5xpcyPzPu-vYhxqsovJQwYm3bh5pqVqh4_Y-zlNjRhsir4nbieBT6QWWlMZ7jpsDW4nhFZEKeyR32OYYXk2mCFVhygdU9WGSIELj7fGiI73J6oB1GcGQoHiRahvyFi9Oob6vt0GQDRw",
        }
        
        with self.app.app_context():
            self.client = self.app.test_client()
            self.connection = database.engine.connect()
            self.trans = self.connection.begin()
            database.session.bind = self.connection
            
    def tearDown(self):
        with self.app.app_context():
            self.trans.rollback()
            self.connection.close()
            database.session.rollback()
            database.session.remove()
            
    #region MOVIES
    # Success Test for the 'GET /movies' route
    def test_get_movies_success(self):
        # Create a movie in the test database
        with self.app.app_context():
            movie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(movie)
            database.session.commit()
            
        # Simulate a GET request to the /movies endpoint
        response = self.client.get('/movies', headers={'Authorization':  self.bearer_token} )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('movies', data)
        self.assertIn('totalMovies', data)

    # Failure Test for the 'GET /movies' route (when no movies are found)
    def test_get_movies_failure(self):
        # Ensure that the database is empty before testing
        with self.app.app_context():
            database.session.remove()
            database.drop_all()

        # Simulate a GET request to the /movies endpoint
        response = self.client.get('/movies', headers={'Authorization':  self.bearer_token} )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], "resource not found")

    # Success Test for 'GET /movies/<int:id>'
    def test_get_movie_success(self):
        # Create a movie
        with self.app.app_context():
            movie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(movie)
            database.session.commit()
            id = movie.id
        # Simulate GET request to the /movies/{id} endpoint
        response = self.client.get(f'/movies/{id}', headers={'Authorization': self.bearer_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('movies', data)
        self.assertEqual(data['movies']['id'], id)
        self.assertEqual(data['movies']['title'], "Test Movie")

    # Failure Test for 'GET /movies/<int:id>' (movie not found)
    def test_get_movie_failure(self):
        # Simulate GET request to a non-existing movie
        response = self.client.get('/movies/999', headers={'Authorization': self.bearer_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertIn('message', data)
        self.assertEqual(data['message'], "Movie not found")

    # Success Test for 'POST /movies'
    def test_add_movie_success(self):
        movie_data = {
            "title": "New Movie",
            "release_date": "2025-01-01"
        }

        # Simulate POST request to add a movie
        response = self.client.post('/movies', headers={'Authorization': self.bearer_token}, json=movie_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('movie', data)
        self.assertEqual(data['movie']['title'], "New Movie")
        self.assertEqual(data['movie']['release_date'], "Wed, 01 Jan 2025 00:00:00 GMT")

    # Failure Test for 'POST /movies' (missing data)
    def test_add_movie_failure(self):
        movie_data = {
            "release_date": "2025-01-01"
        }

        # Simulate POST request with missing title
        response = self.client.post('/movies', headers={'Authorization': self.bearer_token}, json=movie_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "bad request.")
        
    # Success Test for 'DELETE /movies/<int:id>'
    def test_delete_movie_success(self):
        # Create a movie
        with self.app.app_context():
            movie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(movie)
            database.session.commit()
            id = movie.id
            
        # Simulate DELETE request to delete the movie
        response = self.client.delete(f'/movies/{id}', headers={'Authorization': self.bearer_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('movie', data)
        self.assertEqual(data['movie']['id'], id)

    # Failure Test for 'DELETE /movies/<int:id>' (movie not found)
    def test_delete_movie_failure(self):
        # Simulate DELETE request to a non-existing movie
        response = self.client.delete('/movies/999', headers={'Authorization': self.bearer_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertIn('message', data)
        self.assertEqual(data['message'], "Movie not found")
    # # end region 
    
    # region Actors
    # Test: GET /actors
    def test_get_actors_success(self):
        with self.app.app_context():
            #create movie first
            movie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(movie)
            database.session.commit()
            #create actor
            actor = Actor(name='hieutt', age= 24, gender='male', movie_id=movie.id, movie=movie)
            database.session.add(actor)
            database.session.commit()
            
        response = self.client.get("/actors", headers={'Authorization': self.bearer_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("actors", data)

    def test_get_actors_failure(self):
        response = self.client.get("/actorssss", headers={'Authorization': self.bearer_token})
        self.assertEqual(response.status_code, 404)

    # Test: GET /actors/<id>
    def test_get_actor_success(self):
        with self.app.app_context():
            #create movie first
            movie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(movie)
            database.session.commit()
            #create actor
            actor = Actor(name='hieutt', age= 24, gender='male', movie_id=movie.id, movie=movie)
            database.session.add(actor)
            database.session.commit()
            id = actor.id
            
            
        response = self.client.get(f"/actors/{id}", headers={'Authorization': self.bearer_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["actors"]["id"], id)

    def test_get_actor_failure(self):
        response = self.client.get("/actors/999", headers={'Authorization': self.bearer_token})
        self.assertEqual(response.status_code, 404)

    # Test: POST /actors
    def test_add_actor_success(self):
        with self.app.app_context():
            #create movie first
            movie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(movie)
            database.session.commit()
            movie_id = movie.id
            #build actor json
        response = self.client.post(
            "/actors",
            headers={'Authorization': self.bearer_token},
            json={
                "name": "New Actor",
                "age": 28,
                "gender": "male",
                "movie_id": movie_id,
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["actor"]["name"], "New Actor")

    def test_add_actor_failure(self):
        response = self.client.post(
            "/actors",
            headers={'Authorization': self.bearer_token},
            json={"name": "New Actor", "age": 28, "gender": "Female", "movie_id": 999},
        )
        self.assertEqual(response.status_code, 404)

    # Test: PATCH /actors/<id>
    def test_update_actor_success(self):
        with self.app.app_context():
            #create movie first
            movie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(movie)
            database.session.commit()
            #create actor
            actor = Actor(name='hieutt', age= 24, gender='male', movie_id=movie.id, movie=movie)
            database.session.add(actor)
            database.session.commit()
            id = actor.id
            
        response = self.client.patch(
            f"/actors/{id}",
            headers={'Authorization': self.bearer_token},
            json={"name": "Updated Actor"},
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["actor"]["name"], "Updated Actor")

    def test_update_actor_failure(self):
        response = self.client.patch(
            "/actors/999", headers={'Authorization': self.bearer_token}, json={"name": "Nonexistent Actor"}
        )
        self.assertEqual(response.status_code, 404)

    # Test: DELETE /actors/<id>
    def test_delete_actor_success(self):
        with self.app.app_context():
            #create movie first
            movie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(movie)
            database.session.commit()
            #create actor
            actor = Actor(name='hieutt', age= 24, gender='male', movie_id=movie.id, movie=movie)
            database.session.add(actor)
            database.session.commit()
            actor_id = actor.id
            
        response = self.client.delete(f"/actors/{actor_id}", headers={'Authorization': self.bearer_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["actors_deleted_id"], actor_id)

    def test_delete_actor_failure(self):
        response = self.client.delete("/actors/999", headers={'Authorization': self.bearer_token})
        self.assertEqual(response.status_code, 404)
    # # endregion
    
    # region test for RBAC
    def test_casting_assistant_get_actors_success(self):
        # Create a movie
        with self.app.app_context():
            myMovie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(myMovie)
            database.session.commit()
            #create actor
            actor = Actor(name='hieutt', age= 24, gender='male', movie_id=myMovie.id, movie=myMovie)
            database.session.add(actor)
            database.session.commit()
            
        response = self.client.get("/actors", headers={"Authorization": self.tokens["casting_assistant"]})
        self.assertEqual(response.status_code, 200)

    def test_casting_assistant_delete_actor_fail(self):
        """Casting Assistant: Failure case for delete:actors."""
        response = self.client.delete("/actors/1", headers={"Authorization": self.tokens["casting_assistant"]})
        self.assertEqual(response.status_code, 403)

    def test_casting_director_create_actor_success(self):
        with self.app.app_context():
            myMovie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(myMovie)
            database.session.commit()
            movie_id = myMovie.id
            #create actor
            actor = Actor(name='hieutt', age= 24, gender='male', movie_id=myMovie.id, movie=myMovie)
            database.session.add(actor)
            database.session.commit()
        
        response = self.client.post(
            "/actors",
            headers={"Authorization": self.tokens["casting_director"]},
            json={"name": "New Actor", "age": 28, "gender": "Female", "movie_id": movie_id},
        )
        self.assertEqual(response.status_code, 200)

    def test_casting_director_delete_actor_fail(self):
        """Casting Director: Failure case for delete:movies (not allowed)."""
        response = self.client.delete("/movies/1", headers={"Authorization": self.tokens["casting_director"]})
        self.assertEqual(response.status_code, 403)

    def test_executive_producer_delete_movie_success(self):
        """Executive Producer: Success case for delete:movies."""
        # Create a movie
        with self.app.app_context():
            movie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(movie)
            database.session.commit()
            movie_id = movie.id
            
        response = self.client.delete(f"/movies/{movie_id}", headers={"Authorization": self.tokens["executive_producer"]})
        self.assertEqual(response.status_code, 200)

    def test_executive_producer_create_actor_success(self):
        """Executive Producer: Success case for create:actors."""
        with self.app.app_context():
            myMovie = Movie(title="Test Movie", release_date="2024-12-01")
            database.session.add(myMovie)
            database.session.commit()
            movie_id = myMovie.id
            
        response = self.client.post(
            "/actors",
            headers={"Authorization": self.tokens["executive_producer"]},
            json={"name": "Producer Actor", "age": 40, "gender": "Male", "movie_id": movie_id},
        )
        self.assertEqual(response.status_code, 200)
    # end region
    
if __name__ == '__main__':
    unittest.main()
