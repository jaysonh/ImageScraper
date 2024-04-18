import serpapi
import urllib.request
import os
from urllib.parse import urlparse
import requests
import shutil

def shorten_filename(filename, max_length):
    base_name, extension = os.path.splitext(filename)
    if len(base_name) > max_length:
        base_name = base_name[:max_length]
    return base_name + extension

max_filename_length = 25

params = {
  "q": "Chinese scholar stones",
  "engine": "google_images",
  "ijn": "0",
  "api_key": "bd95814ee2ad4c401c4bacf2cea639e2eae83348b0700586a6d93f278f80a7e2"
}
output_directory = "images/"

search = serpapi.search(params)

results = search.as_dict() #["image_results"]

os.makedirs(output_directory, exist_ok=True)

for item in results["images_results"]:

	img_url = item ["original"]
	parsed_url = urlparse(img_url)
	filename = parsed_url.path.split("/")[-1]
	if len(filename) > max_filename_length:
		filename = shorten_filename(filename, max_filename_length)

	save_path = output_directory + filename
	print(f"downloading: {img_url} saving to: {save_path}")

	r = requests.get(img_url,
                 stream=True, headers={'User-agent': 'Mozilla/5.0'})
	if r.status_code == 200:
		with open(save_path, 'wb') as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)
#	urllib.request.urlretrieve(img_url, save_path, headers={'User-Agent': 'Mozilla/5.0'} )
