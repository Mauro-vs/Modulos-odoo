# Modulos-odoo

Repositorio para alojar y gestionar módulos personalizados de Odoo junto con la configuración para correr Odoo mediante Docker Compose.

Descripción
-----------
Este repositorio contiene una configuración orientada a desplegar Odoo en contenedores y un directorio para almacenar volúmenes y módulos personalizados. Está pensado para facilitar el desarrollo local y la prueba de módulos personalizados de Odoo.

- Estructura mínima encontrada en el repositorio:
  - `docker-compose.yml` — configuración para levantar los contenedores (ver archivo en el repo).
  - `volumesOdoo/` — carpeta para volúmenes y/o módulos personalizados.

Requisitos
----------
- Docker (versión reciente)
- Docker Compose v2+ (o el plugin `docker compose`)
- (Opcional) Acceso a internet para descargar imágenes base y dependencias

Instalación y arranque (rápido)
-------------------------------
1. Clona el repositorio:
```bash
git clone https://github.com/Mauro-vs/Modulos-odoo.git
cd Modulos-odoo
```

2. Revisa el archivo de composición y ajústalo si es necesario:
- `docker-compose.yml`: https://github.com/Mauro-vs/Modulos-odoo/blob/main/docker-compose.yml

3. Levanta los servicios:
```bash
# Usando el plugin docker compose
docker compose up -d

# O con docker-compose si lo tienes disponible
docker-compose up -d
```

4. Verifica los logs y acceso:
```bash
docker compose logs -f
# o
docker logs -f <nombre_del_contenedor_odoo>
```

Cómo añadir y probar módulos personalizados
------------------------------------------
- Coloca tus módulos en la carpeta `volumesOdoo` (o en la ruta de addons configurada en el `docker-compose.yml`).
- Reinicia o recarga Odoo para que detecte los nuevos módulos.
- Desde la interfaz web de Odoo:
  - Ve a Aplicaciones → Actualizar lista de aplicaciones → busca e instala tu módulo.
- También puedes entrar al contenedor para pruebas:
```bash
docker compose exec <odoo_service_name> bash
# dentro del contenedor:
odoo -u all -d <tu_base_de_datos> --stop-after-init
```
(Ajusta los comandos según el servicio y la configuración en `docker-compose.yml`.)

Buenas prácticas
----------------
- Mantén cada módulo en su propio subdirectorio con el archivo `__manifest__.py`.
- Usa control de versiones para tus módulos y documenta cambios en el manifest.
- Para desarrollo, mapear el directorio de módulos desde el host al contenedor facilita el debug en caliente.

Estructura sugerida del repo
----------------------------
- docker-compose.yml — configuración principal (ya incluido en el repo).
- volumesOdoo/ — punto recomendado para almacenar módulos o montajes persistentes.
- README.md — documentación del proyecto (este archivo).
- .env (opcional) — variables de entorno para personalizar puertos, passwords y rutas.

Resolución de problemas comunes
-------------------------------
- Si Odoo no detecta módulos: revisa que la ruta de addons esté correctamente montada en el contenedor y que el `__manifest__.py` sea válido.
- Problemas de permisos: asegúrate de que los archivos montados tengan permisos adecuados para el usuario dentro del contenedor.
- Error al levantar con Docker: inspecciona `docker compose logs` y valida que las imágenes se descargaron correctamente.

Contribución
------------
Si quieres contribuir:
- Abre un fork y crea una rama por feature/fix.
- Añade pruebas o pasos de reproducción cuando sea posible.
- Crea un pull request describiendo los cambios y por qué son necesarios.

Licencia
--------
Indica aquí la licencia que desees aplicar (por ejemplo, MIT, GPL-3.0, etc.). Si no tienes preferencia, agrega un archivo `LICENSE` con la licencia deseada.

Contacto
--------
- Mauro (propietario del repo): (usa GitHub para abrir issues o PRs)

Archivos útiles
--------------
- docker-compose.yml: https://github.com/Mauro-vs/Modulos-odoo/blob/main/docker-compose.yml
- Volúmenes y módulos: `volumesOdoo/` (presente en el repo)

Notas finales
-------------
Ajusta las rutas y nombres de servicios en las instrucciones anteriores según el contenido exacto de `docker-compose.yml`. Si quieres, puedo adaptar el README con información específica extraída del contenido del `docker-compose.yml` (puedo revisar el archivo y actualizar el README con detalles exactos de servicios, nombres de contenedores y rutas).
