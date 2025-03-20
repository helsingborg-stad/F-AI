PYTHONPATH=./ poetry run pytest --cov=src/ -v -m "not mongo"
