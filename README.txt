README - Proyecto Django

Requisitos de Instalacion:
	1. Instalar Python
	2. Instalar MongoDB
	3. Crear entorno virtual
	4. Instalar Django y otras librerias en el entorno virtual
	5. Migrar el proyecto y crear un superusuario

PASO 1: Instalar Python
	Se debe utilizar la version 3.6 o superior
	Enlace de descarga: https://www.python.org/downloads/
	
	En mi caso, he utilizado la version 3.6
	Enlace de descarga: https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe
	IMPORTANTE: Al instalar aceptar la opción "Añadir Python 3.6 al PATH"

PASO 2: Instalar MongoDB
	Se debe utilizar la version 3.6 o superior
	Enlace de descarga: https://www.mongodb.com/try/download/community
	IMPORTANTE: Al descargar escoger el tipo de paquete MSI (mejor que el ZIP)
	
	En mi caso, he utilizado la version 4.4.2 para Windows
	Enlace de descarga: https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.3-signed.msi
	
	Para instalar MongoDB en Windows, les dejo el siguiente enlace
	Manual de instalacion: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
	IMPORTANTE: Para hacer funcionar MongoDB es necesario crear un directorio "data/db"
		En mi caso lo he creado en C:\data\db

PASO 3: Crear entorno virtual
	Abrir un terminal y seguir los siguientes pasos:
		1. Instalar virtualenv
			Comando: python -m pip install virtualenv
		2. Comprobar que virtualenv se ha instalado
			Comando: python -m pip freeze
		3. Crear un entorno virtual llamado "django_venv"
			Comando: python -m venv django_venv
	En mi caso, al utilizar Windows, un terminal puede ser CMD o PowerShell

PASO 4: Instalar Django y otras librerias en el entorno virtual
	Se debe utilizar la version 2.1.2 de Django
	Abrir un terminal y seguir los siguientes pasos:
		1. Ir a la siguiente ruta del entorno virtual: django_venv\Scripts
			Comando: cd .\django_venv\Scripts
		2. Activar el entorno virtual
			Comando: activate
		3. Instalar Django (y otras librerias necesarias como Djongo y Networkx)
			Comandos:
				- pip install django==2.1.2
				- pip install djongo
				- pip install djangorestframework==3.7.2
				- pip install networkx
		4. Comprobar librerias instaladas
			Comando: pip freeze
			El resultado debe ser como este:
				dataclasses==0.8
				decorator==4.4.2
				Django==2.1.2
				djangorestframework==3.7.2
				djongo==1.3.3
				networkx==2.5
				pymongo==3.11.2
				pytz==2020.5
				sqlparse==0.2.4

PASO 5: Migrar el proyecto y crear un superusuario
	Abrir un terminal y seguir los siguientes pasos:
		1. Descargar el proyecto de Github
			Comando: git clone https://github.com/rubenamador/ProyectoDjango.git
		2. Activar el entorno virtual
			Comandos: 
				- cd .\django_venv\Scripts
				- activate
		3. Ir a la ruta del proyecto Django (contiene el fichero "manage.py")
			Comando: cd .\ProyectoDjango
		4. Ejecutar MongoDB
			Comandos:
				- cd C:\Program Files\MongoDB\Server\4.4\bin
				- mongod
				IMPORTANTE: Dejar la terminal abierta para configurar la aplicacion en Django
		5. Correr servidor de Django por primera vez
			Comandos:
				- cd .\ProyectoDjango
				- manage.py runserver
				IMPORTANTE: Generar grafo aleatorio en la siguiente URL
					URL: http://127.0.0.1:8000/listGraph
		6. Migrar el proyecto
			Comandos:
				- manage.py makemigrations
				- manage.py migrate
		7. Crear un superusuario
			Comandos:
				- manage.py createsuperuser
				- manage.py runserver
				IMPORTANTE: Introducir credenciales en la siguiente URL
					URL: http://127.0.0.1:8000/admin/
		8. Desactivar el entorno virtual
			Comandos: 
				- cd .\django_venv\Scripts
				- deactivate

Pasos de Uso:
	1. Ejecutar MongoDB
	2. Correr servidor de Django

PASO 1: Ejecutar MongoDB
	Abrir un terminal y seguir los siguientes pasos:
		1. Ir a la ruta donde se instalo MongoDB
			Ejemplo: C:\Program Files\MongoDB\Server\4.4
		2. Ir al directorio "bin" de MongoDB 
			Comando: cd C:\Program Files\MongoDB\Server\4.4\bin
		3. Ejecutar MongoDB
			Comando: mongod
			IMPORTANTE: Dejar la terminal abierta para levantar la aplicacion en Django

PASO 2: Correr servidor de Django
	Abrir un terminal y seguir los siguientes pasos:
		1. Activar el entorno virtual
			Comandos: 
				- cd .\django_venv\Scripts
				- activate
		2. Ir a la ruta del proyecto Django (contiene el fichero "manage.py")
			Comando: cd .\ProyectoDjango
		3. Correr el servidor de Django
			Comando: manage.py runserver
			Por defecto, te devuelve una URL (http://127.0.0.1:8000/)
		4. Abrir un navegador web (como Google Chrome)
		5. Introducir las credenciales del superusuario
			URL: http://127.0.0.1:8000/admin/
		6. Navegar por la aplicacion
			URL: http://127.0.0.1:8000/
