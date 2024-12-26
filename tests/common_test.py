def test_home_page(test_client): #function to test home page
    response = test_client.get("/") #sending get request to home page
    assert response.status_code ==  200 #checking if status code is 200
    assert "message" in response.json #checking if message is in response
    assert response.json == {"message": "Expense calculation app"} #checking if message is correct

def test_not_found(test_client): #function to test 404 error
    response = test_client.get("/not_existing_page") #sending get request to non-existing page
    assert response.status_code ==  404 #checking if status code is 404
    assert "error" in response.json #checking if error is in response
    assert response.json == {"error": "Could not find this expense :("} #checking if error message is correct