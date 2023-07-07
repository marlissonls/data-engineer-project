import sys
from os.path import dirname
SOURCE = dirname(dirname(__file__))
sys.path.append(SOURCE)
from dashboard.br_nz_views import app

if __name__ == "__main__":
    app.run_server(debug=False, port=8051)