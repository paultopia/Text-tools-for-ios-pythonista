import requests, zipfile, os, urllib, io, tarfile
url = input('url: ')
filename = os.path.basename(urllib.parse.urlparse(url).path)
dirname = filename.partition(".")[0]
try:
    os.makedirs(dirname)
except OSError as e:
    print('directory creation failed')
    raise

def extract_tgz(dirname, response):
    with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tarred:
        tarred.extractall(dirname)
    print('file unzipped in '+ dirname)
    
def extract_tar(dirname, response):
    with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:") as tarred:
        tarred.extractall(dirname)
    print('file unzipped in '+ dirname)

def extract_zip(dirname, response):
    with zipfile.ZipFile(io.BytesIO(response.content)) as zipped:
        zipped.extractall(dirname)
    print('file unzipped in '+ dirname)

response = requests.get(url)

if filename.endswith('.tar.gz') or filename.endswith(".tgz"):
    extract_tgz(dirname, response)
elif filename.endswith("tar"):
    extract_tar(dirname, response)
elif filename.endswith('.zip'):
    extract_zip(dirname, response)
else:
    try:
        extract_tgz(dirname, response)
    except:
        try:
            extract_tar(dirname, response)
        except:
            try:
                extract_zip(dirname, response)
            except:
                print("can't recognize compressed file type'")
