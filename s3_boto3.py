import boto3
import sys

# Setup Connection
s3 = boto3.resource('s3')

#####################################
# List Bucket Contents
#####################################
for bucket in s3.buckets.all():
    print (bucket.name)
    print ("---")
    for item in bucket.objects.all():
        print("\t%s" % item.key)


#####################################
# Create a Bucket
#####################################
for bucket_name in sys.argv[1:]:
    try:
        response = s3.create_bucket(Bucket=bucket_name)
        print(response)
    except Exception as e:
        print(e)


#####################################
# Put Object in bucket
#####################################
bucket_name = sys.argv[1]
object_name = sys.argv[2]
try:
    response = s3.Object(bucket_name, object_name).put(
        Body=open(object_name, 'rb'))
    print(response)
except Exception as e:
    print(e)

#####################################
# Delete Items in bucket
#####################################
for bucket_name in sys.argv[1:]:
    bucket = s3.Bucket(bucket_name)
    for key in bucket.objects.all():
        try:
            response = key.delete()
            print(response)
        except Exception as e:
            print(e)


#####################################
# Delete Bucket
#####################################
for bucket_name in sys.argv[1:]:
    bucket = s3.Bucket(bucket_name)
try:
    response = bucket.delete()
    print(response)
except Exception as error:
    print(error)
