# Bench - restTest Kevin Chung 

Application Function:<br />
This application can be run from the command line and:
- Connects to the API website (https://resttest.bench.co/) and fetches all pages of financial transactions
- Calculates running daily balances and prints them to the console, and on localhost:5000. There is a caching mechanism in place that will save the results to a balances.txt file. If this exists, it will automatically display the results from that file. To clear it, simply delete the balances.txt file.<br />

Dependencies: <br />
- Python3 
- Pip
- flask  - pip install Flask <br />
- requests  - python -m pip install requests <br />

API website:  https://resttest.bench.co/ 

# Instructions
To run the application, navigate to the file folder and run the following command:
```
python main.py
```
Open up a browser and use the url: http://localhost:5000/. The application uses port 5000 by default. <br /><br />


To run the tests scripts, navigate to the file folder and run the following command:
```
python test.py
```

