import boto3
import uuid
import os
import json

def log_json(tipo, log_datos):
    # Formato estandar de log: {"tipo": "INFO"/"ERROR", "log_datos": {...}}
    print(json.dumps({
        "tipo": tipo,
        "log_datos": log_datos
    }, ensure_ascii=False, default=str))

def lambda_handler(event, context):
    try:
        # Entrada (json)
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        # Log INFO (ejecucion correcta)
        log_json("INFO", pelicula)
        # Salida (json)
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    except Exception as e:
        # Log ERROR (ejecucion con error)
        body = event.get('body', {}) if isinstance(event, dict) else {}
        log_json("ERROR", {
            'tenant_id': body.get('tenant_id') if isinstance(body, dict) else None,
            'tipo_excepcion': type(e).__name__,
            'mensaje': str(e),
            'event': event
        })
        # Salida (json)
        return {
            'statusCode': 500,
            'error': str(e)
        }
