import os
#Verifies credentials to access google cloud services
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="watchful-goods-338306-82526899e7b7.json"

def read_5(path, pages):
    """
    Detects document features in a PDF/TIFF/GIF file.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision_v1p4beta1 as vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as pdf_file:
        content = pdf_file.read()

    # Other supported mime_types: image/tiff' or 'image/gif'
    mime_type = 'application/pdf'
    input_config = vision.InputConfig(
        content=content, mime_type=mime_type)

    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    request = vision.AnnotateFileRequest(
        input_config=input_config,
        features=[feature],
        pages=pages)

    response = client.batch_annotate_files(requests=[request])

    words = ''

    #Read through each paragraph of the image
    for image_response in response.responses[0].responses:
      for page in image_response.full_text_annotation.pages:
        for block in page.blocks:
          for par in block.paragraphs:
            for word in par.words:
              symbol_texts = [symbol.text for symbol in word.symbols]
              word_text = ''.join(symbol_texts)
              words += (word_text + ' ')

    return words

def read(path):
    """
    Counts the number of pages of the PDF
    """
    import PyPDF2
    file = open(path, 'rb')
    readpdf = PyPDF2.PdfFileReader(file)
    totalpages = readpdf.numPages

    """
    Reads PDF files of up to 20 pages
    """
    words = ''

    if totalpages > 20:
      print('Too many pages')
    else:
      for i in range(1, totalpages + 1):
        words += read_5(path, [i])

    return words

def readTextFile(path):
  """
  Reads text files
  """ 
  with open(path, "r") as f: 
    return f.read()