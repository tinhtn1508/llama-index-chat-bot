import gdown
import shutil

url = 'https://drive.google.com/uc?id=1veCIV0szc3zDvkEL1EfJYFrMH-Zkz3hN'
output = 'chroma_storage.zip'
gdown.download(url, output, quiet=False)
shutil.unpack_archive("chroma_storage.zip", ".")