import json
import os
import boto3
import uuid

dynamodb = boto3.resource('dynamodb', endpoint_url="http://dynamodb.sa-east-1.amazonaws.com")

def lambda_handler(event, context):

    company = json.loads(event['body'])

    err = []
    err = checkEmployees(company['employees'], err)
    err = checkName(company['name'], err)
    
    if(len(err) > 0):
        return messageCallBack(400, err)
    else:
        #se nao existir UUID, entao e um novo cadastro
        statusCode = 200
        if 'company_id'not in company or company['company_id'] is "":
            company['company_id'] = str(uuid.uuid4())
            statusCode = 201

        response = put_item(company)
        
        return messageCallBack(statusCode, response)

def put_item(item):

    if 'test' in item:
        print("Payload de teste:")
        item['company_id'] = "uuid-testing"
        return item

    try:
        table = dynamodb.Table(os.environ['TABLE'])
        print("Adicionando o item na tabela: "+os.environ['TABLE'])
        print(item)
        table.put_item(Item=item)
        return item
    except Exception as e:
        print (e)
        raise Exception('Failed to put_item in dynamodb')


def checkEmployees(employees, err):
    if type(employees) != int:
        err.append("Valor informado de empregados invalido")
    return err

def checkName(name, err):
    if name is None or name is "":
        err.append("Nome obrigatorio")
    return err
    

def messageCallBack(status, message):
    return {
        'statusCode': status,
        'body': json.dumps(message)
    }