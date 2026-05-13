# Calculadora Científica

Una calculadora científica completa desarrollada en Python con interfaz gráfica usando Tkinter.

## 🚀 Características

- ✅ Operaciones básicas: suma, resta, multiplicación, división
- ✅ Funciones científicas: sin, cos, tan, √, x², log
- ✅ Sistema de memoria: MC, MR, M+, M-
- ✅ Interfaz gráfica intuitiva
- ✅ Manejo de errores robusto
- ✅ Suite completa de tests unitarios (74 tests, 91% cobertura)

## 📋 Requisitos

- Python 3.8 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)

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

### Versión con GUI

```bash
python3 calculadora.py
```

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

- **Total de tests**: 74
- **Cobertura**: 91.18% para calculadora.py
- **Tests por categoría**:
  - Operaciones básicas: 22 tests
  - Funciones científicas: 27 tests
  - Sistema de memoria: 25 tests

Para más información sobre los tests, consulta [tests/README.md](tests/README.md).

## 📁 Estructura del Proyecto

```
proyecto/
├── calculadora.py              # Calculadora con GUI (Tkinter)
├── calculadora_consola.py      # Versión de consola
├── tests/                      # Suite de tests
│   ├── test_operaciones_basicas.py
│   ├── test_funciones_cientificas.py
│   ├── test_memoria.py
│   └── README.md
├── requirements.txt            # Dependencias del proyecto
├── pytest.ini                  # Configuración de pytest
├── .coveragerc                 # Configuración de cobertura
├── .gitignore                  # Archivos ignorados por git
├── CALCULADORA_README.md       # Documentación detallada
├── INSTALACION_TKINTER.md      # Guía de instalación de Tkinter
├── GESTION_PROYECTO.md         # Guía de gestión del proyecto
└── README.md                   # Este archivo
```

## 📖 Documentación

- [CALCULADORA_README.md](CALCULADORA_README.md) - Documentación completa de uso
- [INSTALACION_TKINTER.md](INSTALACION_TKINTER.md) - Guía de instalación de Tkinter
- [GESTION_PROYECTO.md](GESTION_PROYECTO.md) - Gestión y roadmap del proyecto
- [tests/README.md](tests/README.md) - Documentación de tests

## 🗺️ Roadmap

El proyecto sigue un roadmap estructurado en milestones:

### v1.1 - Fundamentos ✅ (En progreso)
- [x] Tests unitarios completos
- [ ] Refactorizar eval() con parser seguro
- [ ] Implementar arquitectura MVC
- [ ] Crear versión portable

### v1.2 - UX Mejorada
- [ ] Atajos de teclado
- [ ] Historial de operaciones
- [ ] Configuración persistente

### v1.3 - Funcionalidades
- [ ] Funciones científicas avanzadas
- [ ] Sistema de temas de color

### v2.0 - Web
- [ ] Versión web multiplataforma

Para más detalles, consulta las [issues del proyecto](https://github.com/RodrigoHornos/proyecto/issues).

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
