pypi-upload:
	rm -rf dist/*
	rm -rf *.egg-info
	python3 -m build
	twine upload dist/*

install:
	rm -rf dist/*
	pip3 install build
	python3 -m build
	pip3 install dist/mdpeditor*.tar.gz

single-exec:
	pip3 install pyinstaller
	pyinstaller --onefile mdpeditor.spec
	echo "executable generated in dist/"

