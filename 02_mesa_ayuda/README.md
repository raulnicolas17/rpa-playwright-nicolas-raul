# Laboratorio 2: sesiones y roles en una mesa de ayuda

Proyecto guiado para explorar autenticación, persistencia de sesión, aislamiento mediante `BrowserContext` y autorización por roles con Playwright y Python.

El laboratorio utiliza un portal local y datos completamente sintéticos. No se conecta a sistemas institucionales ni requiere credenciales reales.

## Situación

Nova Services utiliza una mesa de ayuda para atender incidencias tecnológicas. El portal presenta dos perfiles:

- **Solicitante:** consulta únicamente los tickets registrados a su nombre.
- **Agente:** consulta todos los tickets y puede modificar prioridad, grupo y estado.

Se construirá un bot que inicia sesión, conserva el estado autenticado, lo reutiliza y mantiene simultáneamente dos perfiles aislados.

## Resultado de aprendizaje

Al terminar, el estudiante podrá:

1. automatizar un formulario de autenticación;
2. distinguir credenciales rechazadas de un error técnico;
3. explicar la relación entre `Browser`, `BrowserContext` y `Page`;
4. guardar y reutilizar cookies y almacenamiento local;
5. mantener dos sesiones independientes en un navegador;
6. verificar permisos visibles para distintos roles;
7. modificar y validar el estado de un ticket;
8. proteger archivos que contienen estado autenticado.

## Modelo de objetos

```text
Playwright
└── Browser: proceso de Chromium
    ├── BrowserContext: sesión del solicitante
    │   └── Page: panel del solicitante
    └── BrowserContext: sesión del agente
        └── Page: panel del agente
```

Un `BrowserContext` funciona como un perfil de navegador aislado. Tiene sus propias cookies, permisos y almacenamiento web. Dos páginas del mismo contexto comparten sesión; páginas de contextos diferentes no la comparten.

## Credenciales sintéticas

| Perfil | Usuario | Contraseña |
|---|---|---|
| Solicitante | `maria.solicitante` | `rpa123` |
| Agente | `ana.agente` | `soporte123` |

Estas credenciales existen únicamente dentro del portal local.

## Duración sugerida

Entre 90 y 120 minutos:

| Momento | Actividad | Tiempo |
|---|---|---:|
| Apertura | Recuperación del laboratorio anterior y presentación del caso | 10 min |
| Demostración | Login, contexto y almacenamiento del navegador | 20 min |
| Práctica guiada | Prácticas 1 a 4 | 45 min |
| Profundización | Dos contextos y autorización por roles | 20 min |
| Reto y cierre | Gestión de INC-1001 y reflexión | 25 min |

Si se dispone de 90 minutos, la práctica 6 puede completarse después de la sesión.

## Estructura

```text
02_mesa_ayuda/
├── .auth/                  Estados de sesión, excluidos de Git
├── .vscode/                Tareas y configuración de VS Code
├── app/                    Portal local sintético
├── evidencias/             Capturas producidas por el reto
├── practicas/              Archivos que completa el estudiante
├── reflexion.txt
├── requirements.txt
├── server.py
└── README.md
```

## Preparación

### 1. Abrir el proyecto

En VS Code seleccione **Archivo > Abrir carpeta** y abra `02_mesa_ayuda`.

### 2. Crear el entorno virtual

macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar Playwright y Chromium

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

### 4. Seleccionar el intérprete

Abra la paleta de comandos de VS Code, ejecute `Python: Select Interpreter` y seleccione el intérprete de `.venv`.

### 5. Verificar el entorno

Terminal 1:

```bash
python server.py
```

Terminal 2:

```bash
python practicas/00_verificar_entorno.py
```

El portal debe estar disponible en <http://127.0.0.1:8010/login.html>.

`server.py` no abre una ventana. Su función es servir la aplicación. Cada script de Playwright inicia su propia instancia de Chromium cuando `headless=False`.

## Convenciones

- `PORTAL`: dirección del formulario de acceso.
- `context`: sesión aislada del navegador.
- `page`: pestaña dentro de un contexto.
- `ESTADO`: archivo JSON con cookies y almacenamiento web.
- `TODO`: instrucción que debe completar el estudiante.
- `HEADLESS`: se activa automáticamente dentro de GitHub Codespaces.

Mantenga `server.py` activo durante toda la sesión. Ejecute las prácticas desde otra terminal.

## Secuencia de prácticas

### Práctica 0. Verificar el entorno

Archivo: `practicas/00_verificar_entorno.py`.

Es una comprobación técnica y no debe modificarse. Abre el portal y verifica que el encabezado **Iniciar sesión** sea visible.

### Práctica 1. Iniciar sesión

Archivo: `practicas/01_iniciar_sesion.py`.

Complete los localizadores semánticos para:

1. escribir usuario y contraseña;
2. pulsar **Iniciar sesión**;
3. esperar el panel protegido;
4. recuperar el rol mediante `data-testid="session-role"`.

Los localizadores centrales son:

```python
page.get_by_label("Usuario")
page.get_by_label("Contraseña")
page.get_by_role("button", name="Iniciar sesión")
```

Resultado esperado:

```text
Perfil autenticado: Solicitante
```

### Práctica 2. Validar credenciales

Archivo: `practicas/02_validar_credenciales.py`.

Utilice una contraseña incorrecta y recupere el elemento con `role="alert"`.

La aplicación funciona correctamente cuando rechaza credenciales inválidas. Esto es una **excepción de negocio**: el sistema y el bot operaron, pero la entrada no cumple la regla de autenticación.

Un error técnico sería, por ejemplo:

- el servidor no responde;
- Chromium no puede iniciarse;
- el selector no encuentra el campo;
- el script contiene un error de programación.

### Práctica 3. Guardar la sesión

Archivo: `practicas/03_guardar_sesion.py`.

Después de autenticar al solicitante, ejecute:

```python
context.storage_state(path=ESTADO)
```

El archivo contiene una instantánea de cookies y almacenamiento local. En este portal, la identidad se conserva en `localStorage` y el rol también se representa mediante una cookie.

> Un archivo de estado de un sistema real podría permitir que otra persona suplante al usuario. Nunca lo publique, aunque el repositorio sea privado. La carpeta `.auth/` está incluida en `.gitignore`.

### Práctica 4. Reutilizar la sesión

Archivo: `practicas/04_reutilizar_sesion.py`.

Cree el contexto con:

```python
context = browser.new_context(storage_state=ESTADO)
```

Después visite directamente `dashboard.html`. Si el estado fue restaurado, el portal no redirigirá al formulario.

Esta práctica demuestra que:

- el formulario de login no es la sesión;
- la sesión reside en el estado del navegador;
- una automatización puede autenticar una vez y reutilizar el resultado.

### Práctica 5. Contextos y roles

Archivo: `practicas/05_contextos_y_roles.py`.

Cree dos contextos dentro del mismo navegador:

```python
contexto_solicitante = browser.new_context()
contexto_agente = browser.new_context()
```

Inicie sesión con un usuario distinto en cada uno y compare:

| Comprobación | Solicitante | Agente |
|---|---:|---:|
| Tickets visibles | 2 | 3 |
| Puede abrir INC-1001 | Sí | Sí |
| Ve herramientas de agente | No | Sí |

La ausencia de controles en el perfil solicitante representa autorización por rol. No debe confundirse autenticación —saber quién es el usuario— con autorización —determinar qué puede hacer—.

### Práctica 6. Reto: gestionar INC-1001

Archivo: `practicas/06_reto_gestionar_ticket.py`.

Como agente:

1. abra `INC-1001`;
2. cambie la prioridad a **Alta**;
3. asigne el grupo **Seguridad**;
4. cambie el estado a **En proceso**;
5. guarde los cambios;
6. valide los valores mostrados;
7. capture solamente el panel del ticket;
8. imprima un resumen.

Resultado esperado:

```text
INC-1001 -> Alta -> Seguridad -> En proceso -> evidencias/INC-1001-actualizado.png
```

El bloque `try/except/finally` conserva evidencia ante un error técnico y garantiza el cierre del navegador.

## Ejecución

```bash
python practicas/01_iniciar_sesion.py
python practicas/02_validar_credenciales.py
python practicas/03_guardar_sesion.py
python practicas/04_reutilizar_sesion.py
python practicas/05_contextos_y_roles.py
python practicas/06_reto_gestionar_ticket.py
```

Las soluciones docentes no forman parte de este repositorio. Antes de solicitar una referencia, intente cada `TODO` y analice el mensaje de error.

## Depuración

### El portal no está disponible

Compruebe que la Terminal 1 continúe ejecutando:

```bash
python server.py
```

### Chromium no inicia

Ejecute:

```bash
python -m playwright install chromium
```

### La práctica 4 informa que falta el estado

Ejecute primero:

```bash
python practicas/03_guardar_sesion.py
```

### La sesión abre un usuario inesperado

Elimine solamente los archivos sintéticos dentro de `.auth/` y genere nuevamente el estado. No reutilice estados creados por otra persona.

### Un selector encuentra más de un elemento

Revise su intención. Prefiera roles, etiquetas y nombres accesibles. Use `data-testid` cuando el elemento no tenga un nombre semántico suficientemente distintivo.

## Cierre

Complete `reflexion.txt`. La evidencia principal del laboratorio es:

- código funcional;
- `evidencias/INC-1001-actualizado.png`;
- explicación de sesión y contexto;
- tratamiento seguro de `.auth/`.

No entregue ni publique el contenido de `.auth/`.
