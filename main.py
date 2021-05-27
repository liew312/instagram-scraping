from bs4 import BeautifulSoup
import requests
import urllib.request
import time

headers = {'User-Agent': 'Mozilla'}
sampleURLlist = ['https://www.instagram.com/p/CGpJWvan3ja/','https://www.instagram.com/p/CGtiQx9n0t6/','https://www.instagram.com/p/CGbuFLan62V/','https://www.instagram.com/p/CGJkzgPn6fD/','https://www.instagram.com/p/CHcftebHtpg/','https://www.instagram.com/p/CHO48Tfnrkg/']

for idx,urll in enumerate(sampleURLlist):
  print(idx)

  #append ?__a=1 after the url to access the data in json format
  r = requests.get(urll+"?__a=1", headers=headers)
  data = {}
  if r.status_code == 200:
    data = r.json()['graphql']['shortcode_media']
  else:
    exit("Error downloading JSON")

  #3 types of instagram post: GraphImage,GraphVideo,GraphSidecar
  if (data["__typename"]=="GraphImage"):
    urllib.request.urlretrieve(data['display_url'], f'{idx}-{0}.jpg')
  elif (data["__typename"]=="GraphVideo"):
    urllib.request.urlretrieve(data['video_url'], f'{idx}-{0}.mp4')
  elif (data["__typename"]=="GraphSidecar"):
    sideCarChildren = data['edge_sidecar_to_children']['edges']
    for childIdx,child in enumerate(sideCarChildren):
      if (child['node']["__typename"] == "GraphImage"):
        urllib.request.urlretrieve(child['node']['display_url'], f'{idx}-{childIdx}.jpg')
      elif (child['node']["__typename"] == "GraphVideo"):
        urllib.request.urlretrieve(child['node']['video_url'], f'{idx}-{childIdx}.mp4')
      else:
        print("Unknown child type",child['node']["__typename"])
  else:
    print("Unknown parent type",data["__typename"])
  print(data["__typename"])
  print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data["taken_at_timestamp"])))
  print("Count",data['edge_media_to_parent_comment']['count'])
  for node in data['edge_media_to_parent_comment']['edges']:
    print (node['node']['text'])
  print()