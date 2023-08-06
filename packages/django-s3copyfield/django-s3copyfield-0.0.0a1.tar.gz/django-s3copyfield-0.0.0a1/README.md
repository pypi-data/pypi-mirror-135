# django-s3copyfield
A custom FileField for django models that allows copying from a source bucket in S3. This package allows for uploading a
local file to a S3 backend (as normally done with the build-in django FileField) and also allows for copying a file in 
an existing source S3 bucket to the destination S3 bucket/key as defined in the S3Boto3Storage setting. Additional, if 
there is a file in the destination S3 bucket that is not tracked in django, this will create the entry in django without
impacting the existing S3 file.


# Installation 
- pip install django-s3copyfield


# License
django-s3filefield is licensed under the MIT license (see the LICENSE file for details).


# Usage
```python

from s3filefields.fields import S3FileField

class MyModel(models.Model):
    file = S3FileField(max_length=64, blank=True, upload_to=some_file_path, unique=True,
                       storage=S3Boto3Storage(bucket_name=some_bucket_name))
```

In your code add the file via:

```python
MyModel.objects.create(file='s3://some_bucket_name/some_file')
```

