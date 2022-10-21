
import base64
import zipfile
from datetime import datetime

from models import db, Tasks
from helpers.mail import sendMail
from celery import Celery
from flask import Flask, send_from_directory

app = Celery( 'tasks' , broker = 'redis://localhost:6379/0' )

@app.task
def convertFile(receiver, subject, message, fileString, fileName, fileExtension, newFormat):
    print ('\n-> Se va a convertir el archivo: {}'.format(fileName))
    ## codificar a base64 y a bytes
    base64FileBytes = fileString.encode('utf-8')
    decoded_data = base64.decodebytes(base64FileBytes)
    print(type(decoded_data))
    sendMail(receiver, subject, message, decoded_data, fileName, fileExtension)
    print ('\n-> El convirtio y se envio por correo el archivo : {}'.format(fileName))
