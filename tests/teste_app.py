from fastapi.testclient import TestClient

from prev_prob_fogo.app import app

client = TestClient(app)
