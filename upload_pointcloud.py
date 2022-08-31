import requests
import json
import boto3

my_pointerra_api_key = "6a982cca1fb83998c2aac512f62ee7e8f32d724a "

with requests.Session() as s:
    s.headers['Authorization'] = f"Token {my_pointerra_api_key}"

   

    response = s.post("http://localhost/api/jobs/", json={"name":"output","source_job":None,"dataset_type":"not_specified","feature_coding_scheme_id":None,"description":"","attribution":"","extra":"","extra_args":None,"vertical_datum":"geoid","horizontal_to_meters":1,"vertical_to_meters":1,"map_coordinate":None,"process_scans_into_layers":False,"skip_deleted_points":True,"only_visible_points":True,"include_user_edits":True,"sub_model_size":7.5,"destination_collection_id":"rm76aCxD5eh8J42RGDXUsW","replaces_pointcloud":None,"remove_long_term_archive":True,"email_notification":True,"hidden":False,"source_data_uri":"","company_id":"","custom_srs":None,"custom_srs_name":None,"source_srs":None,"no_srs":True,"date_acquired":None,"layers":{"default":[]},"raw_data_size":0,"processing_resolution":0.0015})
    print (response.json())
    response_data = response.json()
    upload_response = s.post("http://localhost/api/jobs/upload_request", json={"job_id": response_data["job_id"] ,"file_manifest":{"files":["output.xyz"],"datasets":[]}})
    print (upload_response.json())
    upload_response_data = upload_response.json()
    cognito_auth_data = {"IdentityId":upload_response_data["credentials"]["IdentityId"],"Logins":{"cognito-identity.amazonaws.com": upload_response_data["credentials"]["Token"]}}
    del s.headers["Authorization"]
    s.headers['x-amz-target'] = "AWSCognitoIdentityService.GetCredentialsForIdentity"
    s.headers['content-type'] = "application/x-amz-json-1.1"
    cognito_id_response = s.post("https://cognito-identity.ap-southeast-2.amazonaws.com/", json = cognito_auth_data)
    print (cognito_id_response.json())
    cognito_id_response_data = cognito_id_response.json()

    REGION = upload_response_data['s3']['region']
    ACCESS_KEY_ID = cognito_id_response_data['Credentials']["AccessKeyId"]
    SECRET_ACCESS_KEY = cognito_id_response_data['Credentials']["SecretKey"]
    SESSION_TOKEN = cognito_id_response_data['Credentials']["SessionToken"]

    PATH_IN_COMPUTER = 'C:\\Users\\HaydenWong\\Desktop\\pointcloud_generator\\output.xyz'

    BUCKET_NAME = upload_response_data['s3']['bucket']
    KEY = upload_response_data['s3']['prefix'] # file path in S3 

    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        aws_session_token=SESSION_TOKEN,
        region_name=REGION
    )

    s3_resource = session.resource('s3')

    s3_resource.Bucket(BUCKET_NAME).put_object(Key = KEY +"/output.xyz", Body = open(PATH_IN_COMPUTER, 'rb'))
    s.headers['Authorization'] = f"Token {my_pointerra_api_key}"
    del s.headers['x-amz-target'] 
    del s.headers['content-type'] 
    job_posted_response = s.patch("http://localhost/api/jobs/" + response_data["job_id"], json={"status":"pending","deleted_files":[],"extra_args":None})
    job_posted_response_data = job_posted_response.json()
    print(job_posted_response_data)