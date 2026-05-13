# Calculadora Científica

Una calculadora científica completa desarrollada en Python con interfaz gráfica usando Tkinter.

## 🚀 Características

- ✅ Operaciones básicas: suma, resta, multiplicación, división
- ✅ Funciones científicas: sin, cos, tan, √, x², log
- ✅ Sistema de memoria: MC, MR, M+, M-
- ✅ Interfaz gráfica intuitiva
- ✅ **Parser matemático seguro** (sympy) - sin riesgos de eval()
- ✅ **Arquitectura MVC** - separación clara de responsabilidades
- ✅ Manejo de errores robusto con mensajes específicos
- ✅ Suite completa de tests unitarios (152 tests, 91% cobertura)
- ✅ Validación de expresiones antes de evaluar
- ✅ Código modular y extensible

## 📋 Requisitos

- Python 3.8 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)
- sympy >= 1.12 (parser matemático seguro)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/RodrigoHornos/proyecto.git
cd proyecto
```

### 2. Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🎮 Uso

### Versión MVC (Recomendada)

```bash
python3 calculadora_mvc.py
```

Esta versión utiliza arquitectura MVC con separación clara de responsabilidades.

### Versión Original

```bash
python3 calculadora.py
```

Versión monolítica mantenida para compatibilidad.

### Versión de consola

```bash
python3 calculadora_consola.py
```

## 🧪 Tests

El proyecto incluye una suite completa de tests unitarios con pytest.

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar tests con cobertura

```bash
pytest --cov=. --cov-report=html
```

### Ver reporte de cobertura

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Estadísticas de tests

- **Total de tests**: 152 ✅
- **Cobertura global**: 91%
- **Cobertura por módulo**:
  - calculadora.py: 84.10%
  - math_parser.py: 90.53%
  - calculator_model.py: 77.24%
  - memory_model.py: 100.00%
- **Tests por categoría**:
  - Operaciones básicas: 22 tests
  - Funciones científicas: 27 tests
  - Sistema de memoria: 25 tests
  - Parser matemático: 46 tests
  - **Modelos MVC**: 32 tests (nuevos)

Para más información sobre los tests, consulta [tests/README.md](tests/README.md).

## 📁 Estructura del Proyecto

```
proyecto/
├── models/                     # 🆕 Modelos MVC (Lógica de negocio)
│   ├── __init__.py
│   ├── calculator_model.py    # Modelo de calculadora
│   └── memory_model.py        # Modelo de memoria
├── views/                      # 🆕 Vistas MVC (Interfaz gráfica)
│   ├── __init__.py
│   └── calculator_view.py     # Vista Tkinter
├── controllers/                # 🆕 Controladores MVC (Coordinación)
│   ├── __init__.py
│   └── calculator_controller.py
├── calculadora_mvc.py          # 🆕 Punto de entrada MVC (recomendado)
├── calculadora.py              # Calculadora original (compatibilidad)
├── calculadora_consola.py      # Versión de consola
├── math_parser.py              # Parser matemático seguro (sympy)
├── tests/                      # Suite de tests
│   ├── test_operaciones_basicas.py
│   ├── test_funciones_cientificas.py
│   ├── test_memoria.py
│   ├── test_math_parser.py
│   ├── test_mvc_models.py     # 🆕 Tests de modelos MVC (32 tests)
│   └── README.md
├── requirements.txt            # Dependencias del proyecto
├── pytest.ini                  # Configuración de pytest
├── .coveragerc                 # Configuración de cobertura
├── .gitignore                  # Archivos ignorados por git
├── CALCULADORA_README.md       # Documentación detallada
├── INSTALACION_TKINTER.md      # Guía de instalación de Tkinter
├── REFACTORIZACION_EVAL.md     # Documentación refactorización eval()
├── ARQUITECTURA_MVC.md         # 🆕 Documentación arquitectura MVC
├── GESTION_PROYECTO.md         # Guía de gestión del proyecto
├── ROADMAP_DEFINITIVO.md       # Roadmap completo
├── REORGANIZACION_MILESTONES.md # Cambios en estructura
└── README.md                   # Este archivo
```

## 📖 Documentación

- [CALCULADORA_README.md](CALCULADORA_README.md) - Documentación completa de uso
- [INSTALACION_TKINTER.md](INSTALACION_TKINTER.md) - Guía de instalación de Tkinter
- [REFACTORIZACION_EVAL.md](REFACTORIZACION_EVAL.md) - Refactorización eval() → parser seguro
- [ARQUITECTURA_MVC.md](ARQUITECTURA_MVC.md) - 🆕 Arquitectura MVC completa
- [ROADMAP_DEFINITIVO.md](ROADMAP_DEFINITIVO.md) - Roadmap completo y detallado
- [REORGANIZACION_MILESTONES.md](REORGANIZACION_MILESTONES.md) - Cambios en la estructura
- [GESTION_PROYECTO.md](GESTION_PROYECTO.md) - Gestión del proyecto
- [tests/README.md](tests/README.md) - Documentación de tests

## 🏗️ Arquitectura

El proyecto utiliza **arquitectura MVC (Model-View-Controller)** para separar responsabilidades:

- **Modelos** (`models/`): Lógica de negocio pura, sin dependencias de UI
- **Vistas** (`views/`): Interfaz gráfica Tkinter, sin lógica de negocio
- **Controladores** (`controllers/`): Coordinación entre modelos y vistas

### Beneficios de MVC

- ✅ **Testabilidad**: Modelos testeables sin UI (152 tests, 91% cobertura)
- ✅ **Mantenibilidad**: Código organizado y fácil de modificar
- ✅ **Extensibilidad**: Fácil añadir nuevas funcionalidades
- ✅ **Reutilización**: Lógica independiente de la interfaz
- ✅ **Separación clara**: Cada componente tiene una responsabilidad única

Para más detalles, consulta [ARQUITECTURA_MVC.md](ARQUITECTURA_MVC.md).

## 🗺️ Roadmap (Actualizado)

El proyecto ha sido reorganizado para consolidar funcionalidades relacionadas:

### v1.1 - Fundamentos Técnicos ✅ (En progreso - 75%)
**Objetivo**: Base técnica sólida + Calculadora profesional completa

- [x] #4 Tests unitarios (COMPLETADO ✅)
- [x] #3 Refactorizar eval() con parser seguro (COMPLETADO ✅)
- [x] #8 Implementar arquitectura MVC (COMPLETADO ✅)
- [ ] 🆕 #13 Modos de operación avanzados y exportación
  - 5 modos: Básico, Ampliado, Científico, Programación, Gráfico
  - Exportación a PDF y Excel
  - Historial avanzado con timestamps
  - Atajos de teclado integrados
  - Sistema de temas
  - Configuración persistente

**Duración estimada**: 9-11 semanas

### v1.4 - Distribución Profesional
**Objetivo**: Aplicación lista para distribución

- [ ] #5 Versión portable (Windows, macOS, Linux)
  - Builds automáticos con CI/CD
  - Releases en GitHub

**Duración estimada**: 2-3 semanas

### v2.0 - Plataforma Web
**Objetivo**: Alcance multiplataforma

- [ ] #9 Versión web
  - Frontend React/Vue
  - Backend FastAPI
  - PWA con capacidad offline

**Duración estimada**: 4-6 semanas

### 📋 Cambios Importantes

**Issues consolidadas en #13**:
- ~~#1 Atajos de teclado~~ → Integrado en #13
- ~~#2 Historial~~ → Integrado en #13
- ~~#6 Temas de color~~ → Integrado en #13
- ~~#7 Funciones científicas~~ → Integrado en #13
- ~~#10 Configuración persistente~~ → Integrado en #13

**Justificación**: Estas funcionalidades están intrínsecamente relacionadas con los modos de operación y deben implementarse de forma coherente para ofrecer una experiencia profesional desde v1.1.

Para más detalles, consulta:
- [ROADMAP_DEFINITIVO.md](ROADMAP_DEFINITIVO.md) - Roadmap completo
- [Issues del proyecto](https://github.com/RodrigoHornos/proyecto/issues)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Ejecutar tests antes de contribuir

```bash
# Asegúrate de que todos los tests pasen
pytest

# Verifica la cobertura de código
pytest --cov=. --cov-report=term-missing
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

**Rodrigo Hornos**

- GitHub: [@RodrigoHornos](https://github.com/RodrigoHornos)

## 🙏 Agradecimientos

- Desarrollado con Python y Tkinter
- Tests con pytest
- Documentación generada con Bob

---

**Nota**: Este proyecto está en desarrollo activo. Consulta las [issues](https://github.com/RodrigoHornos/proyecto/issues) para ver las mejoras planificadas.
