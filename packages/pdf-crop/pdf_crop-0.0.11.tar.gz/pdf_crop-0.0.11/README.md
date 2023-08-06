# Usages

## Crop all the pages in the PDF

`pdf_crop -i <str: input PDF file> [--threshold <float: default 0.008>] [--space <int: default 5>]`

e.g.

`pdf_crop -i ~/Downloads/test.pdf`

or specify the space and threshold:

`pdf_crop -i ~/Downloads/test.pdf --threshold 0.01 --space 3`

## Crop selected pages in the PDF

`python ./pdf_crop -i <str: input PDF file> --page <number left top right bottom output> [--page <number left top right bottom output>] [--threshold <float: default 0.008>] [--space <int: default 5>]`

e.g.

`pdf_crop -i ~/Downloads/test.pdf --page 0 0 0 200 200 "~/Downloads/test - page 0.pdf"`

or specify multiple pages:

`pdf_crop -i ~/Downloads/test.pdf --page 0 0 0 200 200 "~/Downloads/test - page 0.pdf" --page 1 0 0 200 200 "~/Downloads/test - page 1.pdf"`


# Upload to PyPi
1. python3 setup.py sdist bdist_wheel
2. twine upload -u <username> -p "<password>" dist/*