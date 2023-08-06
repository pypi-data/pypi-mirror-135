# README #

El propósito de este Readme es explicar los pasos que se deben seguir para actualizar la versión de esta librería y
además subirla a Pypi.org para que este disponible para usarla en los demás proyectos de Python.

## Instrucciones para subir

* Antes que nada, elimine la carpeta de `dist` y `common_structure_microservices.egg-info`, que se encuentran ubicadas
  en la raíz de este proyecto.

* Aumente la versión en el archivo setup.py.

* Ejecute los dos siguiente comando para crear el paquete a distribuir:

        python setup.py sdist
        twine upload dist/*

* Ejecute el siguiente comando para subir a Pypi, solicitará credenciales que fueron entregadas a el semillero Silux de
  Ingeniería de sistemas.

        twine upload --repository-url https://upload.pypi.org/legacy/ dist/*


* Actualice el repositorio subiendolo a su Control de versiones favorito, pero antes elimine la carpeta de dist y
  common_structure_microservices.egg-info