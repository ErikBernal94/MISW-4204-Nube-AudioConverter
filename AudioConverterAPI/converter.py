
import base64
import zipfile
from datetime import datetime

from models import db, Tasks
from helpers.mail import sendMail
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydub import AudioSegment
celery = Celery( 'tasks' , broker = 'redis://:admin@34.121.79.85/0' )

PASSWORD ="admin"
PUBLIC_IP_ADDRESS ="34.66.98.169"
DBNAME ="postgres"

some_engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}??host=/cloudsql/{}'.format('postgres', PASSWORD,PUBLIC_IP_ADDRESS, DBNAME, 'misw4204-desarrollo-nube:us-central1:audioconverter'))

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# create a Session
session = Session()

@celery.task
def convertFile(receiver, subject, message, fileLocation, fileName, fileExtension, newFormat, taskId):
    print ('\n->Converting file : {}'.format(fileName))
    ## converting file to new format
    oldFileLocation = fileLocation + '/' + fileName
    given_audio = AudioSegment.from_file(oldFileLocation, format=fileExtension)
    ## new file name with new format
    newFileName = fileName.rsplit('.', 1)[0].lower() + "." + newFormat 
    newFileLocation = fileLocation + "/" + newFileName                                         
    given_audio.export(newFileLocation, format=newFormat)

    ## getting file in order to send in the  email
    fileStream = open(newFileLocation,'rb')
    newFile = fileStream.read()
    fileStream.close()
    task = session.query(Tasks).get(taskId)
    task.status = 'processed'
    task.filename = newFileName
    session.commit()
    ## enviar email
    sendMail(receiver, subject, message, newFile, fileName, fileExtension)
    print ('\n-> The file was processed and sent : {}'.format(fileName))
