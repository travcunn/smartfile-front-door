clean:
	find . -name *.pyc -delete

run:
	./run.py

install:
	pip install -r requirements.txt
