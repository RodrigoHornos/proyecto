# 🎯 Guía Práctica: Gestión del Proyecto Calculadora

## 📋 Pasos Inmediatos para Organizar tu Proyecto

### 1️⃣ Crear Milestones en GitHub

Ve a tu repositorio: https://github.com/RodrigoHornos/proyecto

#### Paso a paso:
1. Click en **"Issues"** en la barra superior
2. Click en **"Milestones"** (al lado de Labels)
3. Click en **"New milestone"**

#### Milestones a crear:

**Milestone 1: v1.1 - Fundamentos**
```
Título: v1.1 - Fundamentos
Fecha límite: 2026-07-15
Descripción: 
Establecer base técnica sólida del proyecto:
- Tests unitarios
- Refactorización de eval()
- Arquitectura MVC
- Versión portable
```

**Milestone 2: v1.2 - UX Mejorada**
```
Título: v1.2 - UX Mejorada
Fecha límite: 2026-08-31
Descripción:
Mejorar experiencia de usuario:
- Atajos de teclado
- Historial de operaciones
- Configuración persistente
```

**Milestone 3: v1.3 - Funcionalidades**
```
Título: v1.3 - Funcionalidades
Fecha límite: 2026-11-30
Descripción:
Expandir capacidades de la calculadora:
- Funciones científicas avanzadas
- Sistema de temas
```

**Milestone 4: v2.0 - Web**
```
Título: v2.0 - Web
Fecha límite: 2027-03-31
Descripción:
Versión web multiplataforma de la calculadora
```

---

### 2️⃣ Asignar Issues a Milestones

#### Milestone v1.1 - Fundamentos
Asigna estas issues:
- [ ] #3 - Reemplazar eval() con parser matemático seguro
- [ ] #4 - Implementar suite completa de tests unitarios
- [ ] #5 - Crear versión portable sin instalación
- [ ] #8 - Implementar arquitectura MVC o similar

**Cómo asignar:**
1. Abre cada issue (ej: #3)
2. En el panel derecho, busca "Milestone"
3. Click y selecciona "v1.1 - Fundamentos"
4. Repite para las demás issues

#### Milestone v1.2 - UX Mejorada
Asigna estas issues:
- [ ] #1 - Implementar soporte completo para atajos de teclado
- [ ] #2 - Implementar historial de operaciones con persistencia
- [ ] #10 - Guardar preferencias del usuario entre sesiones

#### Milestone v1.3 - Funcionalidades
Asigna estas issues:
- [ ] #6 - Implementar sistema de temas de color
- [ ] #7 - Expandir funciones científicas disponibles

#### Milestone v2.0 - Web
Asigna esta issue:
- [ ] #9 - Crear versión web de la calculadora

---

### 3️⃣ Orden de Trabajo Recomendado

#### 🚀 Semana 1-2: Setup y Tests
```
1. #4 - Tests unitarios (3-5 días)
   └─ Prioridad: CRÍTICA
   └─ Bloquea: Refactorizaciones futuras
   └─ Empezar: YA

2. #5 - Modo portátil (2-3 días)
   └─ Prioridad: ALTA
   └─ Impacto: Distribución inmediata
   └─ Empezar: Después de tests básicos
```

#### 📅 Semana 3-4: Refactorización
```
3. #3 - Refactorizar eval() (5-7 días)
   └─ Prioridad: ALTA
   └─ Requiere: Tests (#4) completados
   └─ Bloquea: Extensiones futuras

4. #1 - Atajos de teclado (2-3 días)
   └─ Prioridad: ALTA
   └─ Impacto: UX inmediato
   └─ Independiente: Puede hacerse en paralelo
```

#### 📅 Mes 2: Features UX
```
5. #2 - Historial (4-5 días)
   └─ Prioridad: ALTA
   └─ Impacto: Productividad

6. #10 - Configuración persistente (3-4 días)
   └─ Prioridad: MEDIA
   └─ Complementa: Historial y temas
```

#### 📅 Mes 3: Arquitectura
```
7. #8 - Arquitectura MVC (7-10 días)
   └─ Prioridad: MEDIA
   └─ Requiere: Tests sólidos
   └─ Facilita: Desarrollo futuro
```

---

## 🎯 Matriz de Priorización Visual

```
IMPACTO
  ↑
  │  #4 Tests      │  #3 eval()
  │  #5 Portable   │  #8 MVC
  │  #1 Atajos     │
  │─────────────────┼──────────────
  │  #10 Config    │  #9 Web
  │  #6 Temas      │
  │  #7 Científico │
  └──────────────────────────→ ESFUERZO
     Bajo              Alto
```

---

## 📊 Seguimiento Semanal

### Template de Revisión Semanal

Copia esto cada semana en un comentario en la issue #11:

```markdown
## 📅 Revisión Semanal - [Fecha]

### ✅ Completado esta semana
- [ ] Issue #X - Descripción breve
- [ ] Issue #Y - Descripción breve

### 🔄 En progreso
- [ ] Issue #Z - Estado actual, % completado

### 🚧 Bloqueadores
- Ninguno / Descripción del bloqueador

### 📈 Métricas
- Issues cerradas: X
- Issues abiertas: Y
- Progreso milestone actual: Z%

### 🎯 Objetivos próxima semana
1. Completar Issue #X
2. Empezar Issue #Y
3. Revisar PR de Issue #Z

### 💭 Notas
- Observaciones importantes
- Decisiones tomadas
- Cambios de plan
```

---

## 🔧 Comandos Git Útiles

### Workflow por Issue

```bash
# 1. Crear branch para la issue
git checkout -b feature/issue-4-tests-unitarios

# 2. Hacer cambios y commits
git add .
git commit -m "Añadir tests para operaciones básicas

- Tests para suma, resta, multiplicación, división
- Tests para funciones científicas
- Coverage al 60%

Refs #4"

# 3. Push y crear PR
git push origin feature/issue-4-tests-unitarios

# 4. En el PR, mencionar la issue
# Título del PR: "Implementar tests unitarios (#4)"
# Descripción: "Closes #4"
```

### Cerrar Issue Automáticamente

En el commit o PR, usa estas palabras clave:
- `Fixes #4`
- `Closes #4`
- `Resolves #4`

---

## 📈 Dashboard de Progreso

### Ver Progreso General
```
https://github.com/RodrigoHornos/proyecto/milestones
```

### Filtros Útiles en Issues

**Issues de alta prioridad sin asignar:**
```
is:issue is:open label:high-priority no:assignee
```

**Issues del milestone actual:**
```
is:issue is:open milestone:"v1.1 - Fundamentos"
```

**Issues que puedes hacer ahora (sin dependencias):**
```
is:issue is:open label:high-priority -label:blocked
```

---

## 🎨 Crear un Project Board (Opcional pero Recomendado)

### Paso a paso:
1. Ve a tu repositorio
2. Click en **"Projects"** (barra superior)
3. Click en **"New project"**
4. Selecciona **"Board"** template
5. Nombra: "Calculadora - Development"

### Columnas sugeridas:
1. **📋 Backlog** - Issues sin priorizar
2. **📝 To Do** - Próximas a trabajar
3. **🔄 In Progress** - En desarrollo
4. **👀 Review** - En revisión/testing
5. **✅ Done** - Completadas

### Automatización:
- Issues nuevas → Backlog
- Issues asignadas → To Do
- PR abierto → In Progress
- PR merged → Done

---

## 💡 Tips de Productividad

### 1. Usa Templates de Issues
Crea `.github/ISSUE_TEMPLATE/feature_request.md`:
```markdown
---
name: Feature Request
about: Proponer nueva funcionalidad
---

## Descripción
[Descripción clara de la funcionalidad]

## Motivación
[Por qué es necesaria]

## Propuesta
[Cómo implementarla]

## Alternativas
[Otras opciones consideradas]
```

### 2. Usa Templates de PR
Crea `.github/PULL_REQUEST_TEMPLATE.md`:
```markdown
## Descripción
[Qué cambia este PR]

## Issues relacionadas
Closes #

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Documentación

## Checklist
- [ ] Tests añadidos/actualizados
- [ ] Documentación actualizada
- [ ] Código sigue style guide
- [ ] Self-review completado
```

### 3. Usa GitHub CLI (opcional)
```bash
# Instalar
brew install gh

# Autenticar
gh auth login

# Crear issue desde terminal
gh issue create --title "Bug en cálculo" --body "Descripción"

# Ver issues
gh issue list

# Crear PR
gh pr create --title "Fix #4" --body "Implementa tests"
```

---

## 📚 Recursos Adicionales

### Documentación
- [GitHub Issues](https://docs.github.com/en/issues)
- [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)

### Herramientas
- [GitHub Desktop](https://desktop.github.com/) - GUI para Git
- [GitKraken](https://www.gitkraken.com/) - Cliente Git avanzado
- [Notion](https://notion.so) - Documentación adicional
- [Trello](https://trello.com) - Alternativa a Projects

---

## 🎯 Checklist de Setup Inicial

Completa estos pasos para tener todo organizado:

- [ ] Crear los 4 milestones en GitHub
- [ ] Asignar las 10 issues a sus milestones
- [ ] Crear Project Board (opcional)
- [ ] Configurar templates de issues y PRs (opcional)
- [ ] Hacer primera revisión semanal
- [ ] Empezar con Issue #4 (Tests unitarios)
- [ ] Configurar notificaciones de GitHub
- [ ] Invitar colaboradores (si aplica)
- [ ] Crear CHANGELOG.md para releases
- [ ] Configurar GitHub Actions para CI (futuro)

---

## 🚀 ¡Listo para Empezar!

**Próximo paso inmediato:**
1. Ve a https://github.com/RodrigoHornos/proyecto/milestones
2. Crea el primer milestone "v1.1 - Fundamentos"
3. Asigna las issues #3, #4, #5, #8
4. Empieza a trabajar en #4 (Tests unitarios)

**¿Dudas?**
- Revisa la issue #11 en GitHub para la guía completa
- Consulta el documento GITHUB_ISSUES_PROPUESTAS.md para detalles de cada issue

---

**Última actualización:** 2026-05-13
**Versión:** 1.0