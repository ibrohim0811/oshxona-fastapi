# BASE_DIR (repo root) dan ishga tushadi.
# backend.* importlari uchun PYTHONPATH root ga qo'yiladi.
PY := venv/bin/python
export PYTHONPATH := $(CURDIR)

run:
	$(PY) -m uvicorn backend.main:app --reload

mig:
	venv/bin/alembic -c backend/alembic.ini upgrade head

rev:
	venv/bin/alembic -c backend/alembic.ini revision --autogenerate -m "$(m)"