class VirusScan:
    def scan(self):
        print("scan")

class Decode:
    def decode(self):
        print("decode")

class CDN:
    def upload(self):
        print("Upload to cdn")


class UploadFacade:
    def __init__(self, virus, decode, cdn):
        self.virus = virus
        self.decode = decode
        self.cdn = cdn
    
    def upload(self):
        self.virus.scan()
        self.decode.decode()
        self.cdn.upload()


ul =  UploadFacade(VirusScan(), Decode(), CDN())
ul.upload()