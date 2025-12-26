from main import app
from waitress import serve
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('waitress')

if __name__ == '__main__':
    print("--------------------------------------------------")
    print("UMU SmartCaf PRODUCTION SERVER")
    print("System is now running on the Local Network.")
    print("--------------------------------------------------")
    print("Checking for connections...")
    
    # host='0.0.0.0' allows access from any device on your Wi-Fi/Network
    # using port 8080 as a safe standard
    serve(app, host='0.0.0.0', port=8080, threads=4)
