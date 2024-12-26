def test_valid_registartion(test_client, init_database): #function to test registration with valid data
    response = test_client.post("/users/", json={"username": "test_username", "password": "test_password"}) #sending post request to /user/ endpoint with valid data

    assert response.status_code == 201 #checking if status code is 201
    assert "id" in response.json['user'] #checking if id is in response
    assert "username" in response.json['user'] #checking if username is in response
    assert "password" not in response.json['user'] #checking if password is not in response
    assert "message" in response.json #checking if message is in response

def test_invalid_registration_pass(test_client, init_database): #function to test registration with invalid data
    response = test_client.post("/users/", json={"username": "test_user", "password": "123"}) #sending post request to /user/ endpoint with invalid data

    assert response.status_code == 422 #checking if status code is 422
    assert "password" in response.json #checking if password is in response
    assert response.json["password"] == ["Shorter than minimum length 4."] #checking if password error message is correct

def test_invalid_registration_user(test_client, init_database): #function to test registration with invalid data 
    response = test_client.post("/users/", json={"username": "te", "password": "test_password"}) #sending post request to /user/ endpoint with invalid data

    assert response.status_code == 422 #checking if status code is 422
    assert "username" in response.json #checking if password is in response
    assert response.json["username"] == ["Length must be between 3 and 50."] #checking if password error message is correct

def test_duplicate_registration(test_client, init_database):
    test_client.post(
        "/users/",
        json={
            "username": "test_username",
            "password": "test_password",
        },
    )

    response = test_client.post(
        "/users/",
        json={
            "username": "test_username",
            "password": "test_password",
        },
    )

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Username already exists"


def test_valid_login(test_client, init_database):
    response = test_client.post(
        "/users/login",
        json={
            "username": "def_user",
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json


def test_invalid_login_user(test_client, init_database):
    response = test_client.post(
        "/users/login",
        json={
            "username": "wrong_user",
            "password": "test_password",
        },
    )
    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Invalid username or password"

def test_invalid_login_pwd(test_client, init_database):
    response = test_client.post(
        "/users/login",
        json={
            "username": "second_user",
            "password": "wrong_password",
        },
    )
    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Invalid username or password"


    