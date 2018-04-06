import requests, zipfile, os, urllib, io, tarfile
url = input('url: ')
filename = os.path.basename(urllib.parse.urlparse(url).path)
dirname = filename.partition(".")[0]
extension = filename.rpartition(".")[-1]
try:
    os.makedirs(dirname)
except OSError as e:
    print('directory creation failed')
    raise

response = requests.get(url)

if filename.endswith('.tar.gz') or filename.endswith(".tgz"):
    with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tarred:
        tarred.extractall(dirname)
    print('file unzipped in '+ dirname)
elif filename.endswith("tar"):
    with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:") as tarred:
        tarred.extractall(dirname)
    print('file unzipped in '+ dirname)
elif filename.endswith('.zip'):
    with zipfile.ZipFile(io.BytesIO(response.content)) as zipped:
        zipped.extractall(dirname)
    print('file unzipped in '+ dirname)
else:
    print("can't recognize compressed file type'")
