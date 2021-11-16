try:
    from main import app, get_api_data, import_balances_file, calculateBalance
    import os
    import unittest
    import json
except Exception as e:
    print(f"Error: check imported modules: {e}")

class FlaskUnitTests(unittest.TestCase):

    #check index route successfully returns 200
    def test_index_route(self):
        #print("test_index_route")
        test = app.test_client(self)
        response = test.get('/')
        status = response.status_code
        self.assertEqual(status, 200)
    
    #check index route returns a json object
    def test_return_json(self):
        #print("test_return_json")
        test = app.test_client(self)
        response = test.get('/')
        type = response.content_type
        self.assertEqual(type, "application/json")

class ApiTests(unittest.TestCase):

    #check that the data from api correctly outputs a dict
    def test_api_data(self):
        #print("test_api_data")
        response = get_api_data(1)
        self.assertIsInstance(response, dict)
    
    #check if the exception is working for the get_api_data function, current api spec only yields 404 response as non-200 
    def test_api_exception(self):
        #print("test_api_exception")
        response = get_api_data(99999999)
        self.assertEqual(response, 404)
    
    #check that the number of transactions is returned correctly
    #i am assuming it will always be 10 here. If "totalCount" is less than 10, this test will break.
    def test_api_num(self):
        #print("test_api_num")
        response = get_api_data(1)
        self.assertEqual(len(response["transactions"]),10)

    #check if calculateBalance outputs or creates a dict, removes balances.txt afterwards
    def test_check_balances_dict(self):
        #print("test_check_balances_dict")
        response = calculateBalance()
        self.assertIsInstance(response, dict)
        os.remove("balances.txt")

    #check if calculateBalance correctly presents transactions ordered by date
    def test_ordered_balances(self):
        #print("test_ordered_balances")
        testDict = {"2013-12-12": -227.35, "2013-12-15": -5.39, "2013-12-13": -1229.5800000000008}
        with open('balances.txt','w') as file:
            file.write(json.dumps(testDict))
        response = calculateBalance()
        self.assertEqual(dict(response), {'2013-12-12': -227.35, '2013-12-13': -1229.5800000000008, '2013-12-15': -5.39})
        os.remove("balances.txt")

    #check if test_import_file_Dict creates a dict correctly
    def test_import_file_Dict(self):
        #print("test_import_file_Dict")
        if(os.path.isfile("balances.txt")):
            dir = import_balances_file("balances.txt")
            self.assertIsInstance(dir, dict)
            os.remove("balances.txt")

    #check if test_import_file_Dict deals with invalid files correctly
    def test_invalid_file(self):
        #print("test_invalid_file")
        dir = import_balances_file("invalid_file.txt")
        self.assertEqual(dir, FileNotFoundError)

if __name__== '__main__':
    unittest.main()