# sheatless - A python library for extracting parts from sheetmusic pdfs

Sheatless, a tool for The Beatless to become sheetless. Written and managed by the web-committee in the student orchestra The Beatless. Soon to be integrated in [taktlaus.no](https://taktlaus.no/).

# API

## PdfPredictor

```py
class PdfPredictor():
	def __init__(
        self,
        pdf : BytesIO | bytes,
        instruments=None,
        instruments_file=None,
        instruments_file_format="yaml",
        use_lstm=False,
        tessdata_dir=None,
        ):
		...
	
	def parts(self):
		for ...:
			yield  {
				"name": "<part name>",
				"instruments": ["<instrument name", ...],
				"fromPage": "<from page>",
				"toPage": "<to page>",
			}
```

### Arguments for `__init__`:
- `pdf`                                - PDF file object
- `instruments`             (optional) - Dictionary of instruments. Will override any provided instruments file.
- `instruments_file`        (optional) - Full path to instruments file or instruments file object. Accepted extensions: .yaml, .yml, .json
- `instruments_file_format` (optional) - Format of instruments_file if it is a file object. Accepted formats: yaml, json
  - If neither instruments_file nor instruments is provided a default instruments file will be used.
- `use_lstm`                (optional) - Use LSTM instead of legacy engine mode.
- `tessdata_dir`            (optional) - Full path to tessdata directory. If not provided, whatever the environment variable TESSDATA_DIR will be used.

## processUploadedPdf

```python
def processUploadedPdf(pdfPath, imagesDirPath, instruments_file=None, instruments=None, use_lstm=False, tessdata_dir=None):
    ...
	return parts, instrumentsDefaultParts
```

which will be available with

```python
from sheatless import processUploadedPdf
```

Arguments description here:

| Argument         | Optional   | Description                                                                                                      |
| ---------------- | ---------- | ---------------------------------------------------------------------------------------------------------------- |
| pdfPath          |            | Full path to PDF file.                                                                                           |
| imagesDirPath    |            | Full path to output images.                                                                                      |
| instruments_file | (optional) | Full path to instruments file. Accepted formats: YAML (.yaml, .yml), JSON (.json).                               |
| instruments      | (optional) | Dictionary of instruments. Will override any provided instruments file.                                          |
|                  |            | If neither instruments_file nor instruments is provided a default instruments file will be used.                 |
| use_lstm         | (optional) | Use LSTM instead of legacy engine mode.                                                                          |
| tessdata_dir     | (optional) | Full path to tessdata directory. If not provided, whatever the environment variable `TESSDATA_DIR` will be used. |

Returns description here:

| Return                  | Description                                                                                                                       |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| parts                   | A list of dictionaries `{ "name": "name", "instruments": ["instrument 1", "instrument 2"...] "fromPage": i, "toPage": j }` describing each part                                    |
| instrumentsDefaultParts | A dictionary `{ ..., "instrument_i": j, ... }`, where `j` is the index in the parts list for the default part for `instrument_i`. |

## predict_parts_in_pdf

```py
def predict_parts_in_pdf(
	pdf : BytesIO | bytes,
	instruments=None,
	instruments_file=None,
	instruments_file_format="yaml",
	use_lstm=False,
	tessdata_dir=None,
	):
    ...
    return parts, instrumentsDefaultParts
```

### Arguments:
- pdf                                - PDF file object
- instruments             (optional) - Dictionary of instruments. Will override any provided instruments file.
- instruments_file        (optional) - Full path to instruments file or instruments file object. Accepted extensions: .yaml, .yml, .json
- instruments_file_format (optional) - Format of instruments_file if it is a file object. Accepted formats: yaml, json
  - If neither instruments_file nor instruments is provided a default instruments file will be used.
- use_lstm                (optional) - Use LSTM instead of legacy engine mode.
- tessdata_dir            (optional) - Full path to tessdata directory. If not provided, whatever the environment variable TESSDATA_DIR will be used.

### Returns:
- parts                              - A list of dictionaries `{ "name": "name", "instruments": ["instrument 1", "instrument 2"...] "fromPage": i, "toPage": j }` describing each part
- instrumentsDefaultParts            - A dictionary `{ ..., "instrument_i": j, ... }`, where j is the index in the parts list for the default part for instrument_i.

## predict_parts_in_img

```py
def predict_parts_in_img(img : io.BytesIO | bytes | PIL.Image.Image, instruments, use_lstm=False, tessdata_dir=None) -> typing.Tuple[list, list]:
    ...
    return partNames, instrumentses
```

### Arguments:
- img                     - image object
- instruments             - dictionary of instruments
- use_lstm     (optional) - Use LSTM instead of legacy engine mode.
- tessdata_dir (optional) - Full path to tessdata directory. If not provided, whatever the environment variable TESSDATA_DIR will be used.

### Returns:
- partNames               - a list of part names
- instrumentses           - a list of lists of instruments for each part

# Example docker setup

Sheatless requires tesseract and poppler installed on the system to work. An example docker setup as well as integration of the library can be found in [sheatless-splitter](https://github.com/sigurdo/sheatless-splitter).
