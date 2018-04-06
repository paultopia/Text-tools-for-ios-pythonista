import tarfile, io, appex, os, console, datetime

def make_images_data(in_images):
    return {str(idx) + ".jpg": img for idx, img in enumerate(set(in_images))}

def tar_images(images_data, tarfilename):
    with tarfile.open(tarfilename, 'w:gz') as outfile:
        for filename, image in images_data.items():
            newtarfile = tarfile.TarInfo(filename)
            fobj = io.BytesIO()
            fobj.write(image)
            newtarfile.size = fobj.tell()
            fobj.seek(0)
            outfile.addfile(newtarfile, fobj)
    return tarfilename

def get_and_tar_images():
    images_data = make_images_data(appex.get_images_data())
    tarfilename = str(datetime.datetime.now()) + ".tar.gz"
    outfile = tar_images(images_data, tarfilename)
    console.open_in(outfile)
    os.remove(outfile)

if __name__ == '__main__':
    get_and_tar_images()
    