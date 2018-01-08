# WORK IN PROGRESS

import requests
import keychain
import json
import os
import hashlib
from risfile import import_ris_from_file
ZOTERO_HEADERS = {"Zotero-API-Key": keychain.get_password("zotero", "apikey"), "Zotero-API-Version": 3}
ZOTERO_USERID = keychain.get_password("zotero", "userid")
ZOTERO_URL = "https://api.zotero.org"


def apicall(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result.ok:
            try:
                return result.json()
            except:
                return result
        else:
            raise Exception(str(result.status_code) + "\n" + result.reason)
    return inner

def call(url, method="GET", extraheaders={}, **kwargs):
    return requests.request(method, url, headers={**ZOTERO_HEADERS, **extraheaders}, **kwargs)

@apicall
def list_items():
    url = ZOTERO_URL + "/users/" + ZOTERO_USERID + "/items"
    return call(url)

@apicall
def list_item_types():
    url = ZOTERO_URL + "/itemTypes"
    return call(url)

@apicall
def get_template(itemtype):
    url = ZOTERO_URL + f"/items/new?itemType={itemtype}"
    return call(url)

def get_or_load_template(itemtype):
    filename = f"zotero_{itemtype}_template.json"
    try:
        with open(filename) as f:
            return json.load(f)
    except:
        template = get_template(itemtype)
        with open(filename, "w") as f:
            json.dump(template, f)
        return template

def make_template(itemtype, indict):
    item = get_or_load_template(itemtype)
    item.update(indict)
    return item

def parse_creator(creator, creatortype):
    tsplit = creator.split(", ")
    if len(tsplit) == 2:
        return {"creatorType": creatortype, "firstName": tsplit[1], "lastName": tsplit[0]}
    return {"creatorType": creatortype, "firstName": "", "lastName": creator}

def article_from_ris(risdata):
    deets = {"creators": [],
            "date": risdata.get("Y1", ""),
            "issue": risdata.get("IS", ""),
            "pages": risdata.get("SP", "") + "-" + risdata.get("EP", ""),
            "publicationTitle": risdata.get("JO", ""),
            "title": risdata.get("T1", ""),
            "volume": risdata.get("VL", "")}
    for au in risdata.get("A1", []):
        deets["creators"].append(parse_creator(au, "author"))
    return make_template("journalArticle", deets)

# TODO: add book

@apicall
def add_article(article_template):
    headers = {"Content-Type": "application/json"}
    url= ZOTERO_URL + "/users/" + ZOTERO_USERID + "/items"
    return call(url, "POST", headers, json=[article_template])

# here's a bunch of attachment code, it's really terribly convoluted

@apicall
def get_attachment_template():
    url = ZOTERO_URL + "/items/new?itemType=attachment&linkMode=imported_file"
    return call(url)

@apicall
def create_child_attachment_item(parent_item, file_path):
    url = f"{ZOTERO_URL}/users/{ZOTERO_USERID}/items"
    template = get_attachment_template()
    headers = {"Content-Type": "application/json"}
    template.update({"parentItem": parent_item,
                    "title": "PDF attachment from ios",
                    "contentType": "application/pdf",
                    "filename": os.path.basename(file_path)})
    return call(url, "POST", headers, json=[template])
    

@apicall
def get_upload_authorization(attachment_id, file_path):
    hash = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hash.update(buf)
    md5 = hash.hexdigest()
    filesize = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    mtime = str(int(os.path.getmtime(file_path) * 1000))
    url = f"{ZOTERO_URL}/users/{ZOTERO_USERID}/items/{attachment_id}/file"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "If-None-Match": "*"}
    data = {"md5": md5, "filename": filename, "filesize": filesize, "mtime": mtime, "params": 1}
    return call(url, "POST", headers, data=data)

@apicall
def register_uploaded_attachment(authdata, attachment_id):
    url = f"{ZOTERO_URL}/users/{ZOTERO_USERID}/items/{attachment_id}/file"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "If-None-Match": "*"}
    data = {"upload": authdata["uploadKey"]}
    return call(url, "POST", headers, data=data)

@apicall
def upload_attachment(attachment_id, file_path):
    auth = get_upload_authorization(attachment_id, file_path)
    params = auth["params"]
    paramslist = [("key", params["key"])]  # following pyzotero code here, since there seems to be a bunch of undocumented stuff in this api
    for k in params:
        if k != "key":
            paramslist.append((k, params[k]))
    with open(file_path, "rb") as f:
        paramslist.append(("file", f.read()))
    data = tuple(paramslist)
    url = auth["url"]
    result = call(url, "POST", files=data)
    if result.ok:
        return register_uploaded_attachment(auth, attachment_id)
    else:
        return False

# bringing it together, this function is untested.    
def upload_file(parent_item, file_path):
    childitem = create_child_attachment_item(parent_item, file_path)
    attachment_id = childitem["successful"]["0"]["key"]
    return upload_attachment(attachment_id, file_path)
    
