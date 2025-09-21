from fastapi.testclient import TestClient
from backend.src.api.main import app
from backend.src.vectorstore import get_default_store

client = TestClient(app)
text = "Line one\nLine two\nLine three with unique-token-abc123"
files = {"file": ("sample_debug.txt", text.encode('utf-8'))}
r = client.post('/upload', files=files)
print('upload status', r.status_code, r.text)
if r.status_code == 200:
    task_id = r.json().get('task_id')
    print('task_id', task_id)
store = get_default_store()
print('store entries:')
for k, (emb, meta) in store._store.items():
    print(k, meta)
