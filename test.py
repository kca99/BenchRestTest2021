try:
    from main import app, get_api_data, import_balances_file, calculateBalance
    import os.path
    import unittest
except Exception as e:
    print(f"Error: check imported modules: {e}")

class FlaskUnitTests(unittest.TestCase):

    #check index route successfully returns 200
    def test_index_route(self):
        test = app.test_client(self)
        response = test.get('/')
        status = response.status_code
        self.assertEqual(status, 200)
    
    #check index route returns a json object
    def test_return_json(self):
        test = app.test_client(self)
        response = test.get('/')
        type = response.content_type
        self.assertEqual(type, "application/json")

class ApiTests(unittest.TestCase):

    #check that the data from api correctly outputs a dict
    def test_api_data(self):
        response = get_api_data(1)
        self.assertIsInstance(response, dict)
    
    #check if the exception is working for the get_api_data function
    def test_api_except(self):
        response = get_api_data(99999999)
        self.assertEqual(response, "404 Error")
    
    #check if calculateBalance outputs a dict
    def test_check_balances_dict(self):
        response = calculateBalance()
        self.assertIsInstance(response, dict)

class IoTests(unittest.TestCase):

    def test_import_file_Dict(self):
        if(os.path.isfile("balances.txt")):
            dir = import_balances_file("balances.txt")
            self.assertIsInstance(dir, dict)

if __name__== '__main__':
    unittest.main()