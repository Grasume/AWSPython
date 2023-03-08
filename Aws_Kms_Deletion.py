import boto3
import openpyxl

aws_access_key = ''
aws_secret_key = ''

session = boto3.Session(aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

excel = openpyxl.load_workbook("./test_files/Kms keys targeted for cleanup.xlsx")
mainpage = excel.active


for row in mainpage.iter_rows(min_row=2):
    kmsclient = session.client('kms',region_name=str(row[3].value))

    print("Attempting to Delete Key with API delete_imported_key_material "+ row[5].value)
    response = kmsclient.delete_imported_key_material(KeyId=row[4].value)
    print(response)
    
