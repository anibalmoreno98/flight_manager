# Flight Manager – Sistema Distribuido de Gestión de Vuelos

Flight Manager es un sistema distribuido diseñado para gestionar pilotos, aeronaves, misiones, vuelos y telemetría en un entorno modular y escalable.  
Construido con **FastAPI**, **SQLModel**, **PostgreSQL** y **Docker**, el proyecto implementa una arquitectura limpia basada en **Modelos + Repositorios + Servicios + Routers**, permitiendo reglas de negocio avanzadas y un flujo de trabajo profesional.

El sistema soporta validaciones de negocio reales, estados de misión, relaciones entre entidades y restricciones que garantizan la integridad del dominio aeronáutico.


Reglas de Negocio
A continuación se describen las reglas de negocio implementadas en el sistema. Estas reglas están soportadas por los modelos, relaciones y restricciones definidas en la base de datos.

1. Reglas Generales
Todas las misiones deben tener un estado que controle su ciclo de vida: CREADA, PLANIFICADA, EN_CURSO, FINALIZADA, CANCELADA.

No se pueden modificar ni reabrir misiones en estado FINALIZADA o CANCELADA.

No se pueden eliminar recursos que tengan dependencias activas, como misiones, vuelos o telemetría asociada.

2. Reglas para Pilotos
Un piloto no puede estar asignado simultáneamente a más de una misión activa. Se consideran activas las misiones en estado CREADA, PLANIFICADA o EN_CURSO.

No se puede eliminar un piloto que tenga misiones o vuelos asociados.

3. Reglas para Aeronaves
Una aeronave marcada como en mantenimiento no puede asignarse a misiones ni vuelos.

Una aeronave no puede estar asignada a más de una misión activa al mismo tiempo.

No se puede eliminar una aeronave que tenga vuelos o misiones asociadas.

4. Reglas para Misiones
Una misión no puede iniciarse (EN_CURSO) sin piloto y aeronave asignados.

Una misión no puede finalizarse sin al menos un vuelo asociado.

No se permite retroceder en el flujo de estados. Por ejemplo, no es posible pasar de EN_CURSO a PLANIFICADA.

No se pueden eliminar misiones en estado EN_CURSO o FINALIZADA.

5. Reglas para Vuelos
Todo vuelo debe pertenecer a una misión.

No se pueden crear vuelos en misiones que estén en estado FINALIZADA o CANCELADA.

Un vuelo debe tener un piloto y una aeronave válidos.

No se puede eliminar un vuelo que tenga telemetría asociada.

6. Reglas para Telemetría
Toda telemetría debe pertenecer a un vuelo.

No se puede registrar telemetría si la misión asociada está en estado FINALIZADA o CANCELADA.

Los valores de telemetría deben ser válidos (por ejemplo, altitud y velocidad no pueden ser negativas).

7. Reglas para Usuarios
Cada misión debe registrar el usuario que la creó mediante el campo creado_por.

No se puede eliminar un usuario que tenga misiones creadas asociadas.

8. Flujo de Estados de una Misión
El sistema define un flujo de estados coherente que regula la evolución de una misión:

CREADA → PLANIFICADA → EN_CURSO → FINALIZADA
CREADA → CANCELADA
PLANIFICADA → CANCELADA
EN_CURSO → CANCELADA (solo si no existen vuelos asociados)

