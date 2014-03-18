from storages.backends.s3boto import S3BotoStorage

class CustomS3BotoStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        super(CustomS3BotoStorage, self).__init__(*args, **kwargs)

    def url(self, name):
        url = super(CustomS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url

StaticRootS3BotoStorage = lambda: CustomS3BotoStorage(location='static')
MediaRootS3BotoStorage  = lambda: CustomS3BotoStorage(location='media')