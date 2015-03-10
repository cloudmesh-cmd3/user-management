all:
	python setup.py install
	sphinx-apidoc -o docs/source cmd3_example
	cd docs; make -f Makefile html

view:
	open docs/build/html/index.html

clean:
	rm -rf docs/build
	rm -rf build
	rm -rf cmd3_example.egg-info
	rm -rf dist

requirements:
	pip install -r requirements-other.txt
