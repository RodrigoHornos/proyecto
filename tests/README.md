# Suite de Tests - Calculadora Científica

Esta carpeta contiene la suite completa de tests unitarios para la calculadora científica.

## Estructura de Tests

```
tests/
├── __init__.py                      # Inicialización del paquete de tests
├── test_operaciones_basicas.py      # Tests para operaciones aritméticas básicas
├── test_funciones_cientificas.py    # Tests para funciones científicas
├── test_memoria.py                  # Tests para el sistema de memoria
└── README.md                        # Este archivo
```

## Cobertura de Tests

### test_operaciones_basicas.py
- **TestOperacionesBasicas**: Tests para operaciones aritméticas
  - Suma (simple, negativos, decimales)
  - Resta (simple, resultado negativo)
  - Multiplicación (simple, por cero, negativos)
  - División (simple, decimales, división por cero)
  - Precedencia de operadores
  - Operaciones complejas
  - Números muy grandes y muy pequeños

- **TestFuncionesBasicas**: Tests para funciones de interfaz
  - Agregar caracteres
  - Limpiar pantalla
  - Borrar último carácter
  - Cambiar signo

- **TestExpresionesInvalidas**: Tests para manejo de errores
  - Expresión vacía
  - Expresión inválida
  - Operador sin operando
  - Paréntesis sin cerrar

### test_funciones_cientificas.py
- **TestFuncionesTrigonometricas**: Tests para funciones trigonométricas
  - sin() con diferentes ángulos (0°, 30°, 90°, negativos)
  - cos() con diferentes ángulos (0°, 60°, 90°)
  - tan() con diferentes ángulos (0°, 45°)

- **TestFuncionesMatematicas**: Tests para otras funciones matemáticas
  - sqrt() (raíz cuadrada positiva, cero, negativa)
  - pow() (potencia al cuadrado)
  - log() (logaritmo base 10, casos de error)

- **TestFuncionesCientificasConExpresiones**: Tests con expresiones complejas
  - Funciones aplicadas a resultados de operaciones

### test_memoria.py
- **TestSistemaMemoria**: Tests para operaciones de memoria
  - M+ (sumar a memoria)
  - M- (restar de memoria)
  - MR (recuperar memoria)
  - MC (limpiar memoria)
  - Operaciones combinadas
  - Persistencia entre cálculos

- **TestMemoriaEdgeCases**: Tests para casos extremos
  - Números muy grandes
  - Números muy pequeños
  - Precisión decimal

## Instalación de Dependencias

```bash
# Instalar dependencias de testing
pip install -r requirements.txt
```

## Ejecutar Tests

### Ejecutar todos los tests
```bash
pytest
```

### Ejecutar tests con cobertura
```bash
pytest --cov=. --cov-report=html
```

### Ejecutar un archivo específico
```bash
pytest tests/test_operaciones_basicas.py
```

### Ejecutar una clase específica
```bash
pytest tests/test_operaciones_basicas.py::TestOperacionesBasicas
```

### Ejecutar un test específico
```bash
pytest tests/test_operaciones_basicas.py::TestOperacionesBasicas::test_suma_simple
```

### Ejecutar tests con verbose
```bash
pytest -v
```

### Ejecutar tests y mostrar print statements
```bash
pytest -s
```

## Reporte de Cobertura

Después de ejecutar los tests con cobertura, se generará un reporte HTML en `htmlcov/index.html`.

```bash
# Ejecutar tests con cobertura
pytest --cov=. --cov-report=html

# Abrir reporte en navegador (macOS)
open htmlcov/index.html

# Abrir reporte en navegador (Linux)
xdg-open htmlcov/index.html

# Abrir reporte en navegador (Windows)
start htmlcov/index.html
```

## Objetivo de Cobertura

- **Objetivo mínimo**: 80% de cobertura de código
- **Objetivo ideal**: 90%+ de cobertura de código

## Convenciones de Naming

- Archivos de test: `test_*.py`
- Clases de test: `Test*`
- Funciones de test: `test_*`
- Fixtures: nombres descriptivos sin prefijo `test_`

## Buenas Prácticas

1. **Un test, una aserción**: Cada test debe verificar una sola cosa
2. **Tests independientes**: Los tests no deben depender unos de otros
3. **Nombres descriptivos**: Los nombres de los tests deben explicar qué verifican
4. **Arrange-Act-Assert**: Estructura clara en cada test
   - Arrange: Preparar datos y estado
   - Act: Ejecutar la acción a probar
   - Assert: Verificar el resultado
5. **Usar fixtures**: Para código de setup común
6. **Tests rápidos**: Los tests unitarios deben ejecutarse rápidamente

## Añadir Nuevos Tests

Para añadir nuevos tests:

1. Crear un nuevo archivo `test_*.py` en la carpeta `tests/`
2. Importar pytest y las clases necesarias
3. Crear clases de test que hereden de `object` (o nada)
4. Usar fixtures para setup común
5. Escribir funciones de test con nombres descriptivos
6. Ejecutar los tests para verificar que funcionan

Ejemplo:

```python
import pytest
from calculadora import Calculadora

class TestNuevaFuncionalidad:
    @pytest.fixture
    def calc(self):
        root = tk.Tk()
        calculadora = Calculadora(root)
        yield calculadora
        root.destroy()
    
    def test_nueva_funcion(self, calc):
        # Arrange
        calc.expresion = "5"
        
        # Act
        calc.nueva_funcion()
        
        # Assert
        assert calc.expresion == "resultado_esperado"
```

## Continuous Integration

Los tests se ejecutan automáticamente en CI/CD cuando se hace push al repositorio.

## Troubleshooting

### Error: "No module named 'pytest'"
```bash
pip install pytest
```

### Error: "No module named 'calculadora'"
Asegúrate de estar en el directorio raíz del proyecto al ejecutar pytest.

### Tests fallan en macOS con Tkinter
Asegúrate de tener Python instalado con soporte para Tkinter:
```bash
brew install python-tk
```

## Contacto

Para preguntas o problemas con los tests, abre un issue en el repositorio.