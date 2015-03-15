all:
	python setup.py install
	sphinx-apidoc -o docs/source cloudmesh_management
	cd docs; make -f Makefile html

view:
	open docs/build/html/index.html

clean:
	rm -rf docs/build
	rm -rf build
	rm -rf cloudmesh_management.egg-info
	rm -rf dist

requirements:
	pip install -r requirements.txt
