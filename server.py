import http.server
import json
import threading
import traceback
from typing import Dict

class Scoreboard:
    first_reward = [20, 20, 20, 40, 70]
    demon_cost = 50
    char_reward = 15
    photo_reward = 20
    riddle_reward = 40
    bird_reward = 10
    def __init__(self):
        self.main_quest_score = [0] * 5
        self.main_quest_first = [False] * 5
        self.main_quest_demon = [False] * 5
        self.side_quest_char = [False] * 7
        self.side_quest_photo = [False] * 7
        self.side_quest_bird = 0
        self.side_quest_riddle = False
        self.manual_score = 0
        self.remark = ''
    def get_total_score(self):
        total = 0
        for i in range(len(self.main_quest_score)):
            total += self.main_quest_score[i]
            if self.main_quest_first[i]:
                total += self.first_reward[i]
            if self.main_quest_demon[i]:
                total -= self.demon_cost
        for i in range(len(self.side_quest_char)):
            if self.side_quest_char[i]:
                total += self.char_reward
        for i in range(len(self.side_quest_photo)):
            if self.side_quest_photo[i]:
                total += self.photo_reward
        total += self.side_quest_bird * self.bird_reward
        if self.side_quest_riddle:
            total += self.riddle_reward
        total += self.manual_score
        return total

scoreboard: Dict[int, Scoreboard] = {}
scoreboard_lock = threading.Lock()

def get_scoreboard_by_id(id: int) -> Scoreboard:
    if id not in scoreboard:
        scoreboard[id] = Scoreboard()
    return scoreboard[id]

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body)
        response = self.handle_req(data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def handle_req(self, data):
        with scoreboard_lock:
            try:
                if data['type'] == 'query_main':
                    a = get_scoreboard_by_id(int(data['group']))
                    i = int(data['index'])
                    return {
                        'score': a.main_quest_score[i],
                        'first': a.main_quest_first[i],
                        'demon': a.main_quest_demon[i]
                    }
                if data['type'] == 'query_side':
                    a = get_scoreboard_by_id(int(data['group']))
                    return {
                        'bird': a.side_quest_bird,
                        'riddle': a.side_quest_riddle,
                        'char': a.side_quest_char,
                        'photo': a.side_quest_photo
                    }
                if data['type'] == 'query_manual':
                    a = get_scoreboard_by_id(int(data['group']))
                    return {
                        'score': a.manual_score,
                        'remark': a.remark
                    }
                if data['type'] == 'update_main':
                    a = get_scoreboard_by_id(int(data['group']))
                    i = int(data['index'])
                    a.main_quest_score[i] = int(data['score'])
                    a.main_quest_first[i] = bool(data['first'])
                    a.main_quest_demon[i] = bool(data['demon'])
                    return {'error': ''}
                if data['type'] == 'update_side':
                    a = get_scoreboard_by_id(int(data['group']))
                    a.side_quest_bird = int(data['bird'])
                    a.side_quest_riddle = bool(data['riddle'])
                    for i in range(len(a.side_quest_char)):
                        a.side_quest_char[i] = bool(data['char'][i])
                    for i in range(len(a.side_quest_photo)):
                        a.side_quest_photo[i] = bool(data['photo'][i])
                    return {'error': ''}
                if data['type'] == 'update_manual':
                    a = get_scoreboard_by_id(int(data['group']))
                    a.manual_score = int(data['score'])
                    a.remark = str(data['remark'])
                    return {'error': ''}
                if data['type'] == 'query_score':
                    return [(i, get_scoreboard_by_id(i).get_total_score()) for i in scoreboard]
                if data['type'] == 'delete':
                    del scoreboard[int(data['group'])]
                    return {'error': ''}
            except Exception as e:
                traceback.print_exc()
                return {'error': 'Invalid request'}
            

server = http.server.ThreadingHTTPServer(('', 7777), MyHandler)
server.serve_forever()
