
# API Convertidor de audio

Esta aplicación permite a sus usuarios consumir servicios para la conversión entre distintos formatos de audio. Los usuarios crean una cuenta, y esto les da acceso a subir archivos de audio con el respectivo formato al cual desean sean convertidos. Una vez convertidos, se envía una notificación via email adjuntando el archivo procesado.

Este repositorio contiene el BackEnd de la aplicación, el cual permite conversiones entre los formatos MP3, ACC, OGG, WAV y WMA. 

> **_NOTA:_** Este proyecto se realiza para la asignatura **Desarrollo de software en la nube** de la Maestría en Ingeniería de Software (MISO) de la Universidad de los andes.

A continuación, se explica: <br>

1. [Instalación](#1-instalación)
2. [Servicios: configuración y documentación](#2-servicios-configuración-y-documentación)
3. [Instalación con imagen de máquina virtual](#3-instalación-con-imagen-de-máquina-virtual)


## 1. Instalación
La aplicación está desarrollada en el lenguaje de programación python con el framework Flask. Adicional, se incluyen librerías para el trabajo con JWT, configuración de tareas asíncronas, envío de correos, entre otros:

Siga los siguientes pasos: <br>
1. Clone el repositorio `git clone url`
2. Desde su terminal, ubiquese en la carpeta del proyecto `AudioConverterAPI` y ejecute:
  * `python3 -m pip install --user virtualenv`
  * `python3 -m venv venv`
  * `source venv/bin/activate`
  * Instalación de los requerimientos del proyecto `pip install -r /path/to/requirements.txt`
3. Inicie el servidor con `flask run`
4. Modificar los servicios en postman con la ip y puerto correspondientes

> **_NOTA:_** Adicional debe instalar postgres y ejecutar los [scripts](https://github.com/ErikBernal94/MISW-4204-Nube-AudioConverter/tree/main/Scripts) para la creación de la base de datos y tablas utilizadas por la aplicación para llevar registro de las tareas realizadas.

## 2. Servicios: configuración y documentación
Puede obtener la colección con los servicios [aquí](https://github.com/ErikBernal94/MISW-4204-Nube-AudioConverter/tree/main/Documentation/PostmanCollections). Una vez descargado, puede dirigirse a su aplicación `Postman > File > Import > Cargar archivo JSON`.

Se han creado 8 servicios para las categorías: 
* Auth: Servicios de autenticación
  * Signup: Registro de usuario
  * Login: Autenticación de usuario
* Tasks: Servicios relacionados con las tareas de conversión
  * Get tasks: Obtener un listado de todas las tareas
  * Post tasks: Crear una nueva tarea de procesamiento
  * Get tasks by id: Obtener el detalle de una tarea específica
  * Delete task by id: Eliminar una tarea de conversión
  * Update task by id: Actualizar la información de una tarea de conversión
* Files: Servicios para acceder a archivos
  * Get file: Recuperación dearchivos existentes en el servidor (cargados o procesados).

Puede acceder a una documentación completa de los [servicios en postman](https://documenter.getpostman.com/view/3917953/2s847MpqDa). Recomendamos acceder al link de postman en el cual podrá encontrar el detalle de cada servicio, descripción de parámetros, ejemplos de respuestas exitosas y/o con error.

> **_NOTAS:_** <br>
> * La ip que encontrará en las peticiones de postman (Ej: http://127.0.0.1:5000 o {{domain}}) corresponden a la dirección ip en la cual esté corriendo el servicio, por lo cual es importante que los cambie por el correspondiente a su servidor.
> * Las peticiones requieren que se envíe el header `Authorization = Bearer mi_token`. En donde, `mi_token` corresponde al token de autorización proporcionado como respuesta del servicio de login.

## 3. Instalación con imagen de máquina virtual

Con el fin de evaluar el rendimiento de la aplicación, se ha dispuesto de una máquina virtual con unas condiciones específicas.

Las principales características de la máquina virtual son:
* Máquina virtual en Oracle Virtual Box
* SO Linux: Dsitribución Debian
* RAM: 2 Gb
* Disco duro: 10 Gb

Se realizó la instalación de las aplicaciones y paquetes necesarios para utilizar el proyecto.

Con el fin de facilitar la instalación y configuración de la máquina virtual, se ha dispuesto una imagen en formato `.ova` en el [sharepoint Uniandes](https://uniandes-my.sharepoint.com/:u:/g/personal/ja_vegar1_uniandes_edu_co/EQm-IGTIYjFHk8nrJn0dBIUB980moc4LDVAZiPGGf3dyUg?e=o8pkz2). Una vez descargada puede abrir su aplicación `VirtualBox > File > Import appliance > Cargar archivo .ova`. (El usuario y contraseña es **miso**)
