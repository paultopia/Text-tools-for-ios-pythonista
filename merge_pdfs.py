import os, appex, PyPDF2, shutil, glob, console, sys

DIRNAME = "pdf_merging_directory"
os.makedirs(DIRNAME, exist_ok=True)
os.chdir(DIRNAME)

def __extract_filenum(filename):
    try:
        return int(filename.partition(".")[0])
    except ValueError:
        raise ValueError("extraneous file slipped in, make sure DIRNAME is an empty or nonexistent directory")

def __get_next_counter():
    files = glob.glob("*.pdf")
    if len(files) == 0:
        return 0
    return max([__extract_filenum(x) for x in files]) + 1

def __add_file_to_queue(infilename):
    outfilename = str(__get_next_counter()) + ".pdf"
    with open(infilename, "rb") as infile:
        bytes = infile.read()
    with open(outfilename, "wb") as outfile:
        outfile.write(bytes)

def __merge_all_pdfs():
    dest = PyPDF2.PdfFileMerger()
    for count in range(__get_next_counter()):
        filename = str(count) + ".pdf"
        try:
            with open(filename, "rb") as pdf:
                dest.append(PyPDF2.PdfFileReader(pdf))
        except FileNotFoundError:
            raise FileNotFoundError("Somehow one of the files you queued up is missing!")
    with open("outfile.pdf", "wb") as outfile:
        dest.write(outfile)
    console.open_in("outfile.pdf")

def __cleanup():
    os.chdir("..")
    shutil.rmtree(DIRNAME)

def add_file():
    infile = appex.get_file_path()
    __add_file_to_queue(infile)

def finalize_pdf():
    infile = appex.get_file_path()
    __add_file_to_queue(infile)
    __merge_all_pdfs()
    __cleanup()

choice = console.alert("PDF Merge", "", "Add to queue", "Finalize PDF")
if choice == 1:
    add_file()

if choice == 2:
    finalize_pdf()