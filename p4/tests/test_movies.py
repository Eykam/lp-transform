import pytest

from types import SimpleNamespace
import random
import string

from flask_app.forms import SearchForm, MovieReviewForm
from flask_app.models import User, Review


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200

    search = SimpleNamespace(search_query="guardians", submit="Search")
    form = SearchForm(formdata=None, obj=search)
    response = client.post("/", data=form.data, follow_redirects=True)

    assert b"Guardians of the Galaxy" in response.data


@pytest.mark.parametrize(
    ("query", "message"), 
    ([
    ("", "This field is required"),
    ("a", "Too many results"),
    ("gibberish123", "Movie not found"),
    ("x" * 101, "Field must be between 1 and 100 characters long.")
])
    
)
def test_search_input_validation(client, query, message):
    search = SimpleNamespace(				
        search_query=query,
        submit="Search"
        )
    form = SearchForm(formdata=None, obj=search)

    response = client.post(				
    "/", data=form.data, follow_redirects=True	
    )
    
    message_bytes = message.encode('utf-8')
    assert message_bytes in response.data


def test_movie_review(client, auth):
    guardians_id = "tt2015381"
    url = f"/movies/{guardians_id}"
    resp = client.get(url)

    assert resp.status_code == 200

    #testing reg and login
    resp = client.get("/register")
    assert resp.status_code == 200   # good if we get status code 200 (OK)
    auth.register()
    response = auth.login()
    assert response.status_code == 200
    
    review = "lalallalalalalalalalalaalalalalalalalala"
    search = SimpleNamespace(				
        text=review,
        submit="Enter Comment"
        )
    form = MovieReviewForm(formdata=None, obj=search)
    
    response = client.post(				
    "/movies/tt2015381", data=form.data, follow_redirects=True	
    )
    assert response.status_code == 200
    assert review.encode('utf-8') in response.data
    
    
    



@pytest.mark.parametrize(
    ("movie_id", "message"), 
    (
    )
)
def test_movie_review_redirects(client, movie_id, message):
    response = client.get(f"/movies/{movie_id}")
    
    if not movie_id or len(movie_id) < 9 or len(movie_id) > 9:
        assert response.status_code == 404
        assert b"404 - Not Found" in response.data
    else:
        assert response.status_code == 200
        assert message.encode() in response.data


@pytest.mark.parametrize(
    ("comment", "message"), 
    (
    )
)
def test_movie_review_input_validation(client, auth, comment, message):
    assert False


    

    
