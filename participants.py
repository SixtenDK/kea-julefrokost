import gzip
import base64

# Open templates/index.html in read mode
with open('templates/index.html', 'r') as f:
    teststring = f.read()

gzipped = gzip.compress(teststring.encode('utf-8'))
gzipped2 = gzip.compress(gzipped)
gzipped3 = gzip.compress(gzipped2)
print(gzipped3)

# open output file in write-binary mode
with open('file', 'wb') as f:
    f.write(gzipped)

# open output file in read-binary mode
with open('file', 'rb') as f:
    gzipped = f.read()

decompressed = gzip.decompress(gzipped)



