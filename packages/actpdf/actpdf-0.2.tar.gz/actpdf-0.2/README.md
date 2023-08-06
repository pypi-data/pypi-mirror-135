# actpdf

## installation

### for Windows operating system:

+ install python: https://www.python.org/downloads/windows/
+ create virtualenv: `python -m venv env`
+ activate it: `.\env\Scripts\activate`
+ install [GTK3](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases) to fix [libcairo-2.dll error](https://stackoverflow.com/q/59481394/2351696). see: [weasyprint installion guide](https://doc.courtbouillon.org/weasyprint/latest/first_steps.html).


### install

We use weasyprint 52.4, since [WeasyPrint 53 requires at least Pango 1.44](https://github.com/Kozea/WeasyPrint/issues/1384).


    $ pip install actpdf
    $ actpdf

## packaging: Update Version

Updating your distribution Down the road, after you’ve made updates to your distribution and wish to make a new release:

	pip install build
	pip install twine

* increment the version number in your `setup.cfg` file
* `$ python3 -m build`

First upload to TestPypi:

	$ twine upload --repository testpypi dist/*
	# to get password see https://test.pypi.org
	$ pip install --index-url https://test.pypi.org/simple/ --no-deps actpdf


Upload package to the Python Package Index:

	$ twine upload dist/*

	
see: https://packaging.python.org/tutorials/packaging-projects/



## completed templates:

1. allergy
1. nutrition
1. health
1. fitness_quanutrition
1. nutrition_quanutrition
1. fitness
1. detox
1. skin
1. pgx
1. personality
1. carrier
1. sleep



tools: pdf to html converter <https://idrsolutions.com/online-pdf-to-html-converter>