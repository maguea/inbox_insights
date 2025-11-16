# Inbox Insight
## Getting started
NOTE: you may need the python extension
1. if you have not, create the venv with "Python: Create Environment"
2. install flask with `pip install flask`

## options to run
1. run `python -m src.app` in terminal from `/` 
2. `ctrl+shift+p` and search for "Debug: Start Without Debugging". you can also press `ctrl+F5`
3. in the status bar, you can see "Run app.py (inbox_insights)" and can click on that to run. You can do this, but i prefer not to since it wont update html i work on and if you make changes to any py script while `debug=True` in [app.py](/src/app.py) you have to hot reload instead of it automatically reloading the service for you.
   
## view web page
you should see the IP:PORT in the terminal when you run the app. you can ctrl+click on it and it should take you to the browser.

currently: [localhost:5000](http://localhost:5000)