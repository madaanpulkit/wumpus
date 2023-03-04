from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from uuid import uuid4
from flask import session
from flask_session import Session
from flask import request
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)

@socketio.on('connect')
def connect():
    session['sid'] = request.sid

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['width'] = int(request.form['width'])
        session['height'] = int(request.form['height'])
        return generate_dungeon(session['width'], session['height'])
    return render_template('index.html')

@socketio.on('next_pos')
def next_pos(message):
    if message['action'] == 'left':
        if 0 <= session['curr_pos'][0] - 1 < session['width']:
            session['curr_pos'][0] -= 1
    elif message['action'] == 'right':
        if 0 <= session['curr_pos'][0] + 1 < session['width']:
            session['curr_pos'][0] += 1
    elif message['action'] == 'up':
        if 0 <= session['curr_pos'][1] - 1 < session['height']:
            session['curr_pos'][1] -= 1
    elif message['action'] == 'down':
        if 0 <= session['curr_pos'][1] + 1 < session['height']:
            session['curr_pos'][1] += 1
    elif message['action'] == 'arrow':
        pass

    pos = session['curr_pos']
    adj = []
    pit = 0
    wumpus = 0
    treasure = 0

    if session['dungeon'][pos[1]][pos[0]] == 1:
        pit = 2
        socketio.emit('lose', room=session['sid'])
    elif session['dungeon'][pos[1]][pos[0]] == 2:
        wumpus = 2
        socketio.emit('lose', room=session['sid'])
    elif session['dungeon'][pos[1]][pos[0]] == 3:
        treasure = 2
        socketio.emit('win', room=session['sid'])
    else:
        try:
            adj.append(session['dungeon'][pos[1]-1][pos[0]])
        except:
            pass

        try:
            adj.append(session['dungeon'][pos[1]+1][pos[0]])
        except:
            pass

        try:
            adj.append(session['dungeon'][pos[1]][pos[0]-1])
        except:
            pass

        try:
            adj.append(session['dungeon'][pos[1]][pos[0]+1])
        except:
            pass

        if 3 in adj:
            treasure = 1

        if 2 in adj:
            wumpus = 1
        
        if 1 in adj:
            pit = 1
        

    socketio.emit('update_status', 
                {"x": pos[0],
                "y": pos[1],
                "pit": pit,
                "wumpus": wumpus,
                "treasure": treasure}, 
                room=session['sid'])

def generate_dungeon(w, h):
    session['dungeon'] = []
    wumpus_x = random.randrange(2, w)
    wumpus_y = random.randrange(2, h)
    gold_x = random.randrange(2, w)
    gold_y = random.randrange(2, h)
    while (gold_x == wumpus_x and gold_y == wumpus_y):
        gold_x = random.randrange(2, w)
        gold_y = random.randrange(2, h)
    for i in range(h):
        line = []
        # 0 - free
        # 1 - pit
        # 2 - wumpus
        for j in range(w):
            if (i == 0 or i == 1) and (j == 0 or j == 1):
                # the beginning of the dungeon cannot have pits or wumpus
                line.append(0)
            elif i == wumpus_x and j == wumpus_y:
                # wumpus location
                line.append(2)
            elif i == gold_x and j == gold_y:
                # gold location
                line.append(3)
            elif ((i == wumpus_x - 1 or i == wumpus_x + 1) and (j == wumpus_y)) or ((j == wumpus_y - 1 or j == wumpus_y + 1) and (i == wumpus_x)):
                # nothing around the wumpus
                line.append(0)
            else:
                # random pits distributed
                if random.random() <= 0.15:
                    line.append(1)
                else:
                    line.append(0)
                
        session['dungeon'].append(line)
    session['curr_pos'] = [0, 0]
    return render_template('game.html', width=w, height=h)
