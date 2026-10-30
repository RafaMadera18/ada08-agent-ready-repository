# Registro de Uso de Inteligencia Artificial (AI Usage Log)

**Herramientas utilizadas:** Claude Code (Claude 3.5 Sonnet) como asistente de desarrollo y orquestación por CLI, y dos subagentes independientes de Claude Code ejecutados en entornos aislados para simular los roles de agentes desarrolladores en las condiciones BEFORE y AFTER.

**Metodología general:**
Para el desarrollo de esta práctica (ADA-08: *Agent-Ready Repository*), utilicé Claude Code como herramienta principal para estructurar y ejecutar la transformación del repositorio, la auditoría de madurez y los experimentos comparativos. Mi rol consistió en definir las instrucciones de inicio a partir de la guía del curso, seleccionar el proyecto base, supervisar las propuestas de diseño y guardrails, validar la ejecución de pruebas y autorizar la publicación y versionado en GitHub.

---

## Entrada 1: Selección del repositorio base y congelamiento del baseline (29/10/2026)

- **Trabajo realizado con el asistente:** Indiqué a Claude que utilizáramos el repositorio de la práctica ADA-06 como base. Entre las carpetas disponibles (`ada06-github-mcp` que contenía únicamente documentación y `ada06-sample-repo` que contaba con código fuente y suite de pruebas), seleccionamos `ada06-sample-repo`. Se clonó el proyecto preservando el historial, se removió el remoto de origen para protegerlo y se creó la etiqueta `ada08-baseline`. Posteriormente se alineó la etiqueta con el commit que incorpora `TASK_UNDER_TEST.md`, asegurando que ambas corridas partieran del mismo requerimiento.
- **Decisión y supervisión:** Decidí usar `ada06-sample-repo` por ser el proyecto funcional con pruebas unitarias en `src/calculator.py` y verifiqué que la etiqueta `ada08-baseline` quedara fijada en el commit `53d91b6`.

## Entrada 2: Auditoría inicial de madurez (Condición BEFORE)

- **Trabajo realizado con el asistente:** Se realizó la auditoría inicial del repositorio base siguiendo las 8 dimensiones y ponderaciones de la rúbrica del curso. Claude analizó los archivos del baseline, corrió las 7 pruebas existentes y asignó la calificación inicial (30/100), fundamentando cada brecha con evidencia del código. Este reporte se registró en un commit antes de iniciar las corridas de prueba para aislar el contexto del agente.
- **Decisión y supervisión:** Revisé los criterios y acepté la calificación de 30/100, validando que el puntaje de 3/5 en *Build / Run / Test* era el adecuado dado que solo existía el comando de tests, sin linter ni comando unificado de verificación.

## Entrada 3: Diseño del Change Request de prueba (CR-001)

- **Trabajo realizado con el asistente:** Analizamos las opciones de tareas para medir la autonomía y fricción del agente. Descartamos "implementar descuento" porque la función `apply_discount` ya existía en el código (a pesar de que `SPEC.md` la marcaba como pendiente). Formulamos el Change Request CR-001 para añadir `calculate_order_total(prices, discount_percent=0.0, tax_rate=0.0)` en `src/calculator.py`, referenciando los requerimientos existentes REQ-001 a REQ-003 sin alterarlos. Claude comprobó previamente el resultado esperado (156.6) ejecutando las funciones existentes.
- **Decisión y supervisión:** Aprobé el diseño de CR-001 como una tarea representativa: no trivial, acotada, determinista y directamente verificable.

## Entrada 4: Estructuración de AGENTS.md y arquitectura documental

- **Trabajo realizado con el asistente:** Siguiendo los principios de reducción de contexto ambiguo, se diseñó `AGENTS.md` como contrato operativo central con enlaces directos a fuentes de verdad en lugar de duplicar especificaciones. Se implementó `CLAUDE.md` como adaptador delgado que solo redirige a `AGENTS.md`, `ARCHITECTURE.md` para delimitar límites de módulos y convenciones de pureza/redondeo, y `docs/REPO_MAP.md` como guía de navegación para evitar exploraciones ciegas.
- **Decisión y supervisión:** Establecí como regla que los agentes solo pueden incorporar nuevos criterios de aceptación (AC) en `SPEC.md`, reservando cualquier cambio o adición a `REQUIREMENTS.md` para aprobación humana obligatoria.

## Entrada 5: Conversión de reglas en guardrails ejecutables

- **Trabajo realizado con el asistente:** Para asegurar que las directrices no fueran meras sugerencias en texto, se convirtieron en scripts deterministas en Python estándar: `scripts/check_protected_paths.py` (bloquea cambios en `REQUIREMENTS.md`, `.github/` o commits con secretos/.env) y `scripts/check_repo_contract.py` (valida existencia de archivos requeridos, consistencia REQ/AC y rutas citadas en docs). Se añadieron 13 pruebas unitarias y se ejecutaron 8 casos de prueba demostrativos en `results/evidence/guardrail-demo.txt`.
- **Decisión y supervisión:** Durante las pruebas del guardrail se detectó que un archivo `.env` ignorado en `.gitignore` provocaba una discrepancia con la regla original. Respaldé el ajuste de la regla para permitir `.env` locales ignorados y concentrar el bloqueo en prevenir su commit o adición forzada (`git add -f`).

## Entrada 6: Ejecución experimental BEFORE vs. AFTER

- **Trabajo realizado con el asistente:** Se ejecutó el experimento comparativo empleando dos subagentes limpios e independientes en repositorios aislados (`ada08-runs/run-a` y `ada08-runs/run-b`), exponiendo únicamente el contexto autorizado para cada condición. Claude compiló las métricas de ejecución (número de turnos, archivos consultados, tokens) y verificó de forma independiente las salidas de ambos agentes.
- **Decisión y supervisión:** Revisé los resultados de ambas corridas: mientras el agente BEFORE requirió explorar el árbol y definir su propio método de validación, el agente AFTER siguió el orden de `AGENTS.md`, utilizó el comando unificado y actualizó de manera consistente `SPEC.md`, `TASKS.md` y `docs/REPO_MAP.md`. Validé además que la suite final pasara a 27 pruebas (7 nuevas pruebas añadidas para CR-001).

## Entrada 7: Identificación de conocimiento implícito

- **Trabajo realizado con el asistente:** Se sistematizaron en `results/implicit-knowledge.md` los 8 puntos de conocimiento implícito que el agente BEFORE tuvo que asumir o inferir (convenciones de error `ValueError`, redondeo monetario a 2 decimales, archivos que no debían modificarse, etc.), asociando cada punto a una mejora concreta implementada en el repositorio.
- **Decisión y supervisión:** Comprobé que los 8 elementos quedaran formalmente especificados en la documentación o respaldados por los scripts de verificación determinista.

## Entrada 8: Verificación compartida y CI/CD en GitHub

- **Trabajo realizado con el asistente:** Se configuró `scripts/verify_repo.sh` como único punto de entrada de verificación (tests, lint de sintaxis, contrato del repositorio y rutas protegidas), utilizado por desarrolladores, agentes y el workflow de GitHub Actions (`.github/workflows/verify.yml`). Claude preparó la estructura para el repositorio remoto.
- **Decisión y supervisión:** Autorice la creación del repositorio público en mi cuenta de GitHub (`RafaMadera18/ada08-agent-ready-repository`), ordené la publicación de las ramas de evidencia (`ada08/before`, `ada08/after`, `ada08/improve`, `main`), y verifiqué en la interfaz de GitHub Actions que todos los workflows terminaran en estado exitoso (verde).

## Entrada 9: Evaluación final y reflexiones

- **Trabajo realizado con el asistente:** Se completó la auditoría AFTER alcanzando un puntaje de 86/100 (+56 puntos sobre el baseline). Claude generó el borrador inicial del reporte comparativo y las respuestas base a las preguntas de reflexión.
- **Decisión y supervisión:** Acepté el puntaje de 86/100 reconociendo las amenazas a la validez documentadas en el reporte (evaluador compartido y una sola corrida por condición), ejecuté la verificación local completa (`VERIFY_REPO: PASS`) y revisé las respuestas de reflexión en `results/readiness-improvement-report.md`.
