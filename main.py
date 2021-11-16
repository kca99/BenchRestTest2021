from flask import Flask, jsonify
import requests
import json
import os.path
from collections import OrderedDict 

app = Flask(__name__)

# Function:  get_api_data(pageNum)
# Use:       loads data from given api
# Input:     PageNumber
# Output:    Response Data as Dictionary or 404 if no value
def get_api_data(pageNum):
    app.logger.info(f"Running get_api_data. Page = {pageNum}")
    r = requests.get(f'https://resttest.bench.co/transactions/{pageNum}.json')
    #app.logger.info(r.status_code)   
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return 404
    return json.loads(r.content)

# Function:  import_balances_file(fileName)
# Use:       Imports dictionary from a file created from last run
# Input:     FileName
# Output:    Dictionary variable as dictVar      
def import_balances_file(fileName):
    app.logger.info("Running import_balances_file")
    with open(fileName, 'r') as file:
        dictVar = eval(file.read())
    return dictVar

# Function:  calculateBalance()
# Use:       Creates a dict object of balances from the Bench API, exports a copy of the balance variable as a file. 
#            If the Balances.txt exists already, it will pull from the file instead. In the future, can set a time comparison to fetch new data in case 
#            new data is available.
# Input:     None
# Output:    balances as a dict object 
# Depend.:   import_balances_file(), get_api_data()
def calculateBalance():
    app.logger.info("Running calculateBalance")
    #if ran before, i load the results of the last run as a form of caching mechanism. To create a new result, simply move/delete balances.txt from the root.
    if(os.path.isfile("balances.txt")):
        balances = import_balances_file("balances.txt")
        ordered = OrderedDict(sorted(balances.items(), key=lambda t:t[0]))
        app.logger.info(ordered)
        return ordered
    else:
        balances = {}
        page = 1
        exitVal = False 
        while (exitVal == False): #Using exit condition instead of another api call
            data = get_api_data(page)
            if(data != 404):
                for k in data["transactions"]: #load dictionary based on whether the key already exists
                    if k["Date"] in balances:
                        balances[k["Date"]] = float(balances[k["Date"]]) + float(k["Amount"])
                    else:
                        balances[k["Date"]] = float(k["Amount"])
                page = page+1
            else:
                exitVal = True
        

        #Dump balances dict as balances.txt
        ordered = OrderedDict(sorted(balances.items(), key=lambda t:t[0]))
        with open('balances.txt','w') as file:
            file.write(json.dumps(ordered))
        app.logger.info(ordered)
        return ordered

@app.route('/')
def index():
    app.logger.info("Initializing index page")
    response = calculateBalance()
    return response

#http://localhost:5000/
if __name__== '__main__':
    app.run(host='0.0.0.0', debug=True)