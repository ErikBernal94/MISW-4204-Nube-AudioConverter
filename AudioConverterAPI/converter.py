
import base64
import zipfile
from datetime import datetime

from models import db, Tasks
from helpers.mail import sendMail
from celery import Celery
from flask import Flask, send_from_directory
from pydub import AudioSegment
app = Celery( 'tasks' , broker = 'redis://localhost:6379/0' )


@app.task
def convertFile(receiver, subject, message, fileLocation, fileName, fileExtension, newFormat, taskId):
    print ('\n->Converting file : {}'.format(fileName))
    ## converting file to new format
    oldFileLocation = fileLocation + '/' + fileName
    given_audio = AudioSegment.from_file(oldFileLocation, format=fileExtension)
    ## new file name with new format
    newFileLocation = fileLocation + "/" + fileName.rsplit('.', 1)[0].lower() + "." + newFormat                                           
    given_audio.export(newFileLocation, format=newFormat)

    ## getting file in order to send in the  email
    fileStream = open(newFileLocation,'rb')
    newFile = fileStream.read()
    fileStream.close()
    # task = Tasks.query.get_or_404(taskId)
    # task.status = 'processed'
    # db.session.commit()
    ## enviar email
    sendMail(receiver, subject, message, newFile, fileName, fileExtension)
    print ('\n-> The file was processed and sent : {}'.format(fileName))
