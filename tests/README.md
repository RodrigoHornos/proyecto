# Suite de Tests - Calculadora Científica

Esta carpeta contiene la suite completa de tests unitarios para la calculadora científica.

## Estructura de Tests

```
tests/
├── __init__.py                      # Inicialización del paquete de tests
├── test_operaciones_basicas.py      # Tests para operaciones aritméticas básicas (22 tests)
├── test_funciones_cientificas.py    # Tests para funciones científicas (27 tests)
├── test_memoria.py                  # Tests para el sistema de memoria (25 tests)
├── test_math_parser.py              # Tests para parser matemático seguro (46 tests)
├── test_mvc_models.py               # Tests para modelos MVC (32 tests)
├── test_history_model.py            # Tests para sistema de historial (34 tests)
├── test_keyboard_model.py           # Tests para atajos de teclado (37 tests)
├── test_theme_model.py              # Tests para sistema de temas (32 tests)
├── test_mode_model.py               # Tests para modos de operación (40 tests)
├── test_scientific_model.py         # Tests para modo científico (69 tests)
├── test_pdf_exporter.py             # Tests para exportación PDF (19 tests)
├── test_excel_exporter.py           # Tests para exportación Excel (32 tests)
├── test_programmer_model.py         # Tests para modo programación (61 tests)
├── test_graphing_model.py           # Tests para modo gráfico (59 tests)
└── README.md                        # Este archivo
```

**Total: 535 tests con 74.87% de cobertura global**

## Estadísticas de Cobertura por Módulo

| Módulo | Tests | Cobertura |
|--------|-------|-----------|
| calculadora.py | 22 | 84.10% |
| math_parser.py | 46 | 90.53% |
| calculator_model.py | 32 | 77.24% |
| memory_model.py | 25 | 100.00% |
| history_model.py | 34 | 93.66% |
| keyboard_model.py | 37 | 94.39% |
| theme_model.py | 32 | 89.66% |
| mode_model.py | 40 | 100.00% |
| scientific_model.py | 69 | 93.27% |
| pdf_exporter.py | 19 | 98.24% |
| excel_exporter.py | 32 | 99.56% |
| programmer_model.py | 61 | 96.43% |
| graphing_model.py | 59 | 84.36% |

## Cobertura de Tests

### test_operaciones_basicas.py (22 tests)
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

### test_funciones_cientificas.py (27 tests)
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

### test_memoria.py (25 tests)
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

### test_math_parser.py (46 tests)
- **TestMathParser**: Tests para parser matemático seguro
  - Operaciones básicas con sympy
  - Funciones científicas
  - Validación de expresiones
  - Manejo de errores
  - Casos extremos

### test_mvc_models.py (32 tests)
- **TestCalculatorModel**: Tests para modelo de calculadora
  - Operaciones básicas
  - Funciones científicas
  - Validación de expresiones
- **TestMemoryModel**: Tests para modelo de memoria
  - Operaciones de memoria (M+, M-, MR, MC)
  - Persistencia

### test_history_model.py (34 tests)
- **TestHistoryModel**: Tests para sistema de historial
  - Agregar entradas con timestamps
  - Búsqueda y filtrado
  - Exportación de historial
  - Persistencia JSON
  - Límite de entradas

### test_keyboard_model.py (37 tests)
- **TestKeyboardModel**: Tests para atajos de teclado
  - Registro de atajos
  - Modificadores (Ctrl, Alt, Shift)
  - Validación de atajos
  - Persistencia
  - Atajos personalizables

### test_theme_model.py (32 tests)
- **TestThemeModel**: Tests para sistema de temas
  - 6 temas predefinidos (Default, Dark, Light, High Contrast, Solarized, Monokai)
  - Cambio de temas
  - Validación de colores
  - Persistencia
  - Temas personalizados

### test_mode_model.py (40 tests)
- **TestModeModel**: Tests para modos de operación
  - 5 modos (Básico, Ampliado, Científico, Programación, Gráfico)
  - Cambio entre modos
  - Validación de modos
  - Persistencia

### test_scientific_model.py (69 tests)
- **TestScientificModel**: Tests para modo científico
  - Funciones trigonométricas (sin, cos, tan, asin, acos, atan)
  - Funciones hiperbólicas (sinh, cosh, tanh)
  - Logaritmos (log, ln)
  - Exponenciales
  - Constantes matemáticas (π, e, φ)
  - Factorial
  - Conversión de ángulos

### test_pdf_exporter.py (19 tests)
- **TestPDFExporter**: Tests para exportación PDF
  - Generación de PDFs
  - Formato profesional
  - Inclusión de tablas
  - Metadatos
  - Validación de archivos

### test_excel_exporter.py (32 tests)
- **TestExcelExporter**: Tests para exportación Excel
  - Generación de archivos Excel
  - Múltiples hojas
  - Formato de celdas
  - Fórmulas
  - Validación de archivos

### test_programmer_model.py (61 tests)
- **TestProgrammerModel**: Tests para modo programación
  - Conversión entre bases (2, 8, 10, 16)
  - Operaciones bit a bit (AND, OR, XOR, NOT)
  - Desplazamientos (left shift, right shift)
  - Rotaciones (rotate left, rotate right)
  - Manipulación de bits individuales
  - Soporte para 8, 16, 32, 64 bits
  - Números con/sin signo

### test_graphing_model.py (59 tests)
- **TestGraphingModel**: Tests para modo gráfico
  - Graficación de funciones
  - Parseo de expresiones con sympy
  - Búsqueda de raíces
  - Cálculo de derivadas
  - Búsqueda de extremos
  - Cálculo de límites
  - Intersecciones entre funciones
  - Integración numérica
  - Manejo de discontinuidades

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

- **Cobertura actual**: 74.87%
- **Objetivo mínimo**: 80% de cobertura de código
- **Objetivo ideal**: 90%+ de cobertura de código
- **Total de tests**: 535 tests

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