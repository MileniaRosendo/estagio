import exifread
import io
import boto3
from PIL import Image 
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
BUCKET_NAME = 'Instangrao'
#O boto3 é uma biblioteca que utilizamods para facilitar a integração com os serviços da AWS, como dynamodb e o s3
db = boto3.resource('dynamodb')

'''Essa função foi  criada para subir o arquivo da rede para o s3,
 nesse caso utilizamos o try and except: se  for possivél subir o arquivo
retorne true, senão , retorne false'''

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


uploaded = upload_to_aws('local_file', 'bucket_name', 's3_file_name')

#Esta função é utilizada para extrair a imagem do banco de dados chamado s3_image_object
def extract_metadata(image_path):
    s3 = boto3.resource('s3')
    s3_image_object = s3.Object(BUCKET_NAME, image_path)
    file_stream = s3_image_object['Body']
    image_size = s3_image_object.content_lenght
    image = Image.open(file_stream)
    #Image.Open é uma biblioteca que utilizamos para abrir a imagem 
    send_to_dynamodb(image, image_size)

dynamodb_client = boto3.client('dynamodb')
#Método criado para acessar o banco de dados e retornar os itens da imagem. 
def send_to_dynamodb(image, image_size):
   
    table = db.Table ("images")
    table.put_item(
        Item = {
            'name': image.filename,
            'width': image.width,
            'heigth': image.height,
            'size': image_size,
            'format': image.format
        }
    )
    #print("")
#Este método esta retornando os itens inseridos dentro da tabela referentes a imagem
def get_metadata(table_name):
    table = db.Table(table_name) 
    response = table.scan()
    print(response['Items'])
    return response['Items']
   
 #Este método foi criado para chamar os outros métodos que vão retornar o tamnanho, o tipo e quantidade das imagens.  
def info_images():
    image_list = get_metadata("images")
    show_image_sizes(image_list)
    show_image_types(image_list)
    show_type_quantity(image_list)

#Método criado para mostrar o maior e o menor tamanho da lista, através de uma chave criada dentro do parâmetro chamada 'size'. 
def show_image_sizes(image_list):
    image_list = sorted(image_list, key = lambda x: x['size'])
    print("Imagem com maior tamanho: " , image_list[-1])
    print("Imagem com menor tamanho: " , image_list[0])

'''Método que recebe como parâmetro a lista das imagens. 
Utilizando o loop para percorrer as imagens e uma condição que pede para que 
cada formato seja adicionado a essa lista dependendo do tipo de imagem  de imagens. '''

def show_image_types(image_list):   
    image_types = []
    for image in image_list:
        if image['format'] not in image_types: 
            image_types.append(image['format'])
    print("Tipos de imagens salvas: " , image_types)

'''Método que recebe como parâmetro a lista das imagens, nele foi criado uma lista vazia
 para retornar a quantidade de imagens a depender da posição delas'''
def show_type_quantity(image_list):
    image_type_quantity = {}
    for image in image_list:
        try:
            image_type_quantity[image['format']] += 1 
        except KeyError:
            image_type_quantity[image['format']] = 1  
    print("A quantidade de imagens salvas são: " , image_type_quantity)

#metodo criado para teste. 
def mock_image_list(image):
    return [
        
            {
            'name': image.filename,
            'width': image.width,
            'heigth': image.height,
            'size': 128,
            'format': 'gif'
            }
        ,
        
            {   
            'name': image.filename,
            'width': image.width,
            'heigth': image.height,
            'size': 140,
            'format': 'png'
            }
        ,
        
            {
            'name': image.filename,
            'width': image.width,
            'heigth': image.height,
            'size': 100,
            'format': image.format
            }
        ,
        
            {
            'name': image.filename,
            'width': image.width,
            'heigth': image.height,
            'size': 95,
            'format': image.format
            }
        ,
    ]

#metodo criado para teste:
#def main():
    #image = Image.open('teste.jpg')
    
    #image_list = mock_image_list(image)
    #print(image_list)
    #show_image_sizes(image_list)
    #show_image_types(image_list)
    #show_type_quantity(image_list)

#if __name__ == "__main__":
    #main()


    