import boto3
'''Utilizamos um banco de dados para guardar os atributos da imagem com o dyamodb'''
dynamodb_resource = boto3.resource('dynamodb')

table = dynamodb_resource.create_table (
    TableName = 'images',
       KeySchema = [
           {
                'AttributeName': 'name',
                'KeyType': 'HASH'
           },
           {
                'AttributeName': 'width',
                'KeyType': 'HASH'
           },
           {
                'AttributeName': 'heigth',
                'KeyType': 'HASH'
           },
           {
                'AttributeName': 'size',
                'KeyType': 'HASH'
           },
           {
                'AttributeName': 'format',
                'KeyType': 'HASH'
           },
           ],
           AttributeDefinitions = [
               {
                   'AttributeName': 'name',
                   'AttributeType': 'S'
               },
               {
                   'AttributeName':'width',
                   'AttributeType': 'S'
               },
               {
                   'AttributeName':'heigth',
                   'AttributeType': 'S'
               },
               {
                   'AttributeName': 'size',
                   'AttributeType': 'I'
               },
               {
                'AttributeName': 'format',
                'AttributeType': 'S'
           },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits':1,
                'WriteCapacityUnits':1
            }
          
    )
print(table)