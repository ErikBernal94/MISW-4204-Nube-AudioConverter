
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

# Migración a la nube pública 

Como parte del proyecto se realiza una migración de la aplicación Convertidor de Audio a la nube pública, en este caso se usará como proveedor de servicios a Google Cloud platform

## 1. Aprovisionamiento de insfraestructura en la nube

Teniendo en cuenta la arquitectura planteada (https://github.com/ErikBernal94/MISW-4204-Nube-AudioConverter/wiki/Arquitectura-Nube-P%C3%BAblica), se deben aprovisionar 3 maquinas virtuales (Compute engine) y una base de datos en la nube (Cloud SQL) de la siguiente manera:

### 1. AudioConverterWebServer (Compute Engine API)

Es el punto de entrada a la aplicación, en esta maquina se despliega la API (AudioConverterAPI) usando flask y las librerias anteriormente mencionadas.

#### Configuración de despliegue:

- Serie: N1
- Tipo de maquina: g1-small (Un nucleo compartido - Memoria de 1.7GB)
- Almacenamiento: 10GB
- Sistema operativo: Debian/Linux 

#### Instalaciones adicionales requeridas

- NGINX
- nfs-common
- ffmpeg

#### Configuraciones adicionales

- Permitir acceso desde las reglas del firewall
- Configurar NFS como cliente (https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04-es)

### 2. AudioConverterWorker (Compute Engine Procesamiento Asincrono Redis)

En esta maquina se ejecuta el servicio asincrono (Redis), encargado de realizar la conversión de los archivos y enviar los correos electronicos hacuendo uso de un servicio SMTP de nube publica, en este caso Outlook SMTP

#### Configuración de despliegue:

- Serie: N1
- Tipo de maquina : f1-micro (Un nucleo compartido - Memoria de 614MB ) 
- Almacenamiento: 10GB
- Sistema operativo: Debian/Linux 

#### Instalaciones adicionales requeridas

- NGINX
- nfs-common
- redis-server
- ffmpeg

#### Configuraciones adicionales

- Permitir acceso desde las reglas del firewall
- Configurar NFS como cliente (https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04-es)

### 3. AudioConverterFileServer (Compute Engine Almacenamiento Archivos NFS)

En esta maquina se almacenan los archivos enviados por el usuario, para posteriormente ser consultadosy procesados desde el worker

#### Configuración de despliegue:

- Serie: N1
- Tipo de maquina : f1-micro (Un nucleo compartido - Memoria de 614MB ) 
- Almacenamiento: 10GB
- Sistema operativo: Debian/Linux 

#### Instalaciones adicionales requeridas

- nfs-kernel-server

#### Configuraciones adicionales

- Configurar NFS como host (https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04-es)

### 4. AudioConverter DB (Cloud SQL DB)

Para la persistencia de datos, se usa una instancia de base de datos PostgreSQL en la nube.

#### Configuración de despliegue:

- vCPU : 2
- Memoria: 8GB
- Almacennamiento (SSD): 100GB 

#### Configuraciones adicionales

- Permitir acceso a las maquinas virtuales (AudioConverterWebServer y AudioConverterWebServer) en las reglas del firewall
- Ejecutar scripts para creación de las tablas (https://github.com/ErikBernal94/MISW-4204-Nube-AudioConverter/blob/main/Scripts/2.%20create%20tables.sql)

## 2. Escalabilidad servidor web

Como parte de la integración a la nube se propone una nueva arquitectura con el fin de aumentar la escalabilidad en la capa web. Arquitectura: https://github.com/ErikBernal94/MISW-4204-Nube-AudioConverter/files/9993946/Documento1.3.pdf

### 1. Instance template web

Se crea un template para que sea usado en escalamiento horizontal en los servidores web dentro de un grupo de instancias.

#### Configuraciones

- Serie: N1
- Tipo de maquina : f1-micro (Un nucleo compartido - Memoria de 614MB ) 
- Almacenamiento: 10GB
- Sistema operativo: Debian/Linux 
- Script de arranque:

#! /bin/bash
apt-get update 	
apt-get -y install git
apt-get -y install pip
apt-get -y install ffmpeg
apt-get -y install nginx
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
bash add-google-cloud-ops-agent-repo.sh --also-install -y
systemctl status google-cloud-ops-agent"*"
apt-get update
git clone https://github.com/ErikBernal94/MISW-4204-Nube-AudioConverter.git
cd MISW-4204-Nube-AudioConverter/AudioConverterAPI/
git checkout realease/balanceador-storage
sudo pip install -r requirements.txt
gunicorn --bind 0.0.0.0:5000 wsgi:app

- El script de arranque configura un agente en cada maquina virtual desplegada para activar el sistema de monitoreo.

### 2. Instance group

Como parte de la estrategia de escalamiento, se crea un grupo de instancias con las siguientes configuraciones:

- Número mínimo de instancias 1
- Número máximo de instancias 3
- Tipo de métrica: Utilización de CPU
- Utilización permitoda de CPU: 80% 
- Periodo de arranque: 600s 

### 3. Load Balancer

Se configura un balanceador de carga como punto de entrada al grupo de instacias, el balanceador de carga incluye un health check.

### 4. Cloud Storage

### 5. Cloud Monitoring

