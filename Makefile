run:
	uvicorn main:app --reload
mig:
	alembic upgrade head