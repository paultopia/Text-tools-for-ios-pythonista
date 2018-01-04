import requests, appex, uuid, os, console
from buttonbox import make_view

docverter = "http://c.docverter.com/convert"

def share_binary(bytes, extension):
    if bytes:
        filename = uuid.uuid1().hex + "." + extension
        with open(filename, "wb") as f:
            f.write(bytes)
        console.open_in(filename)
        os.remove(filename)
        print('success!')
    else:
        print("no file found")
    
def convert_file(file_object, extension):
    r = requests.post(docverter, data={'to':extension,'from':'markdown'},files={'input_files[]':file_object})
    if r.ok:
        return r.content
    else:
        print('request failed: ' + r.status_code)
        return None

filename = appex.get_file_path()

def docx(button):
    with open(filename, "rb") as f:
        docfile = convert_file(f, "docx")
        share_binary(docfile, "docx")
    button.superview.close()

def pdf(button):
    with open(filename, "rb") as f:
        pdffile = convert_file(f, "pdf")
        share_binary(pdffile, "pdf")
    button.superview.close()

view = make_view([('convert to word', docx), ('convert to pdf', pdf)])
view.present('sheet')
