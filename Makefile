# BASE_DIR (repo root) dan ishga tushadi.
# backend.* importlari uchun PYTHONPATH root ga qo'yiladi.
PY := backend/venv/bin/python
export PYTHONPATH := $(CURDIR)

run:
	$(PY) -m uvicorn backend.main:app --reload

mig:
	$(PY) -m alembic -c backend/alembic.ini upgrade head
