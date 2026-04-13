import http.server
import socketserver
import webbrowser
import os
import json
from urllib.parse import urlparse, parse_qs
from checker.strategy_factory import StrategyFactory

DIRECTORY="."
STATIC_DIR=os.path.dirname(os.path.abspath(__file__))

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=DIRECTORY,**kwargs)

    def do_POST(self):
        content_length=int(self.headers['Content-Length'])
        post_data=self.rfile.read(content_length)
        data=json.loads(post_data.decode('utf-8'))
        
        if data.get('action')=='evaluate_password':
            password=data.get('password')
            
            strength_checker=StrategyFactory.get_strategy("strength")
            strength_level=strength_checker.evaluate(password)
            
            time_to_crack_calculator=StrategyFactory.get_strategy("time_to_crack")
            time_to_crack=time_to_crack_calculator.evaluate(password)
            
            response_data={
                'strength':strength_level,
                'time_to_crack':time_to_crack,
                'properties':{
                    'length':len(password),
                    'has_numbers':any(char.isdigit()for char in password),
                    'has_lowercase':any(char.islower()for char in password),
                    'has_uppercase':any(char.isupper()for char in password),
                    'has_special':any(not char.isalnum()for char in password)
                }
            }
            
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

def run_server(port=8008):
    handler=MyRequestHandler
    with socketserver.TCPServer(("",port),handler) as httpd:
        print(f"Serving HTTP at http://localhost:{port}")
        webbrowser.open(f"http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
