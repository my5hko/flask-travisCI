def test_no_expenses_list(test_client, init_database, second_user_token): #function to test if there are no expenses
    response = test_client.get("/expenses/", headers={"Authorization": f"Bearer {second_user_token}"} ) 
    #sending get request to expenses page with token of second user in headers
    
    assert response.status_code == 200 #checking if status code is 200
    assert response.json == [] #checking if expenses list is empty

def test_expenses_list(test_client, init_database, default_user_token) : #function to test expenses list
    response = test_client.get("/expenses/", headers={"Authorization": f"Bearer {default_user_token}"})
    #sending get request to expenses page with token of default user in headers
    assert response.status_code == 200 #checking if status code is 200
    assert len(response.json) > 0 #checking if expenses list is not empty
    assert "id" in response.json[0] #checking if id is in response
    assert "amount" in response.json[0] #checking if amount is in response
    assert "title" in response.json[0] #checking if title is in response

def test_full_expense_flow(test_client, init_database, default_user_token): #function to test full expense flow
    created_expense_res = test_client.post( #sending post request to create expense
        "/expenses/", #url
        json={ #json data
            "title": "Expense", #title of expense
            "amount": 100, #amount of expense
        },
        headers={"Authorization": f"Bearer {default_user_token}"}, #token of default user in headers
    )
    assert created_expense_res.status_code == 201 #checking if status code is 201
    assert created_expense_res.json["title"] == "Expense" #checking if title is correct

    created_expense_res_id = created_expense_res.json["id"] #getting id of created expense

    received_expense_res = test_client.get( #sending get request to get expense
        f"/expenses/{created_expense_res_id}", #url with id of created expense
        headers={"Authorization": f"Bearer {default_user_token}"}, #token of default user in headers
    )
    assert received_expense_res.status_code == 200 #checking if status code is 200
    assert received_expense_res.json["title"] == "Expense" #checking if title is correct

    updated_expense_res = test_client.patch( #sending patch request to update expense
        f"/expenses/{created_expense_res_id}", #url with id of created expense
        json={
            "title": "Updated Expense", #new title of expense
        },
        headers={"Authorization": f"Bearer {default_user_token}"}, #token of default user in headers
    )
    assert updated_expense_res.status_code == 200 #checking if status code is 200
    assert updated_expense_res.json["title"] == "Updated Expense"  #checking if title is correct

    deleted_expense_res = test_client.delete( #sending delete request to delete expense
        f"/expenses/{created_expense_res_id}", #url with id of created expense
        headers={"Authorization": f"Bearer {default_user_token}"}, #token of default user in headers
    )
    assert deleted_expense_res.status_code == 204 #checking if status code is 204
    assert deleted_expense_res.json == None #checking if response is None