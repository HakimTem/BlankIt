

import os, io
import re
import json
from google.cloud import vision_v1 as vision
from google.cloud import storage
from google.protobuf import json_format
from google.cloud.vision_v1 import types


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

client = vision.ImageAnnotatorClient()

batch_size = 1
mime_type = 'application/pdf'
feature = vision.Feature(
    type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

gcs_source_uri = 'gs://blankit_pdfs/sample.pdf'
gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
input_config = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

gcs_destination_uri = 'gs://blankit_pdfs/pdf_result'
gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
output_config = vision.types.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)

async_request = vision.types.AsyncAnnotateFileRequest(
    features=[feature], input_config=input_config, output_config=output_config)

operation = client.async_batch_annotate_files(requests=[async_request])
operation.result(timeout=180)

storage_client = storage.Client()
match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
bucket_name = match.group(1)
prefix = match.group(2)
bucket = storage_client.get_bucket(bucket_name)

# List object with the given prefix
blob_list = list(bucket.list_blobs(prefix=prefix))
print('Output files:')
for blob in blob_list:
    print(blob.name)
blobs = 0
for i in blob_list:
  output = i
  json_string = output.download_as_string()
  response = json.loads(json_string)

  first_page_response = response['responses'][blobs]
  blobs += blobs
  annotation = first_page_response['fullTextAnnotation']

  print(annotation['text'])
