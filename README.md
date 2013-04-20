Game server using Tornado and websockets for hosting turn-based play between two players.

##Usage
pip install -r requires.txt 
python server.py

Open browser, etc




Marek's Code Review - 4/15/13
- fix up README, usage
- brief description of the architecture (mention explicitly entry point)
- separate out html js css python directories
- document the protocol/ msg types between client and server side
- serve index.html (content type)
- remove all trailing whitespace 
- pep8 - 80chars per line for js and py html

- get jquery min js and download itself - option (google cdn)
- specify version for jquery
- localhost (now in index.html) to be set to docs current url 
- onclose in websocket.js to notify / popup with a msg 
- create a websocket on page load 
- simpler way to get radio button clicked

- USE JQUERY not document.elementbyId blablabla
- be consistent about spaces in js around functions and variable assignments
- use jquery to replace text (not use inner html)
- create classes of the games with same api (drawboard())
- document allgames as an object
- make encoding consistent both directions (dont need to use ast in messages)
- index html button in form should be a submit
- update onclose method to notify clients from server.py
- always specify an error in a try except block
- if client is sending rubbish, write to logs and kill the connection (instead of sending a msg back)
requires.txt (contain tornado=xx.xx)

- clean up handleMove in gameshandler uggggly
- use uuid for game id also (not a global ID) 
