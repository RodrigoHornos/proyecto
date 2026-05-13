# 🧮 Calculadora Científica con GUI

Una calculadora completa con interfaz gráfica desarrollada en Python usando Tkinter. Incluye operaciones básicas, funciones científicas y sistema de memoria.

## 📋 Características

### Operaciones Básicas
- ➕ Suma
- ➖ Resta
- ✖️ Multiplicación
- ➗ División

### Funciones Científicas
- **sin** - Seno (en grados)
- **cos** - Coseno (en grados)
- **tan** - Tangente (en grados)
- **√** - Raíz cuadrada
- **x²** - Potencia al cuadrado
- **log** - Logaritmo base 10

### Sistema de Memoria
- **MC** - Memory Clear (Limpiar memoria)
- **MR** - Memory Recall (Recuperar memoria)
- **M+** - Memory Add (Sumar a memoria)
- **M-** - Memory Subtract (Restar de memoria)

### Funciones Especiales
- **C** - Clear (Limpiar todo)
- **CE** - Clear Entry (Borrar última entrada)
- **+/-** - Cambiar signo del número
- **.** - Punto decimal

## 🚀 Requisitos

- Python 3.6 o superior
- Tkinter (incluido por defecto en la mayoría de instalaciones de Python)

## 💻 Instalación y Uso

### En Windows:
```bash
python calculadora.py
```

### En macOS/Linux:
```bash
python3 calculadora.py
```

O hacer el archivo ejecutable:
```bash
chmod +x calculadora.py
./calculadora.py
```

## 📖 Guía de Uso

### Operaciones Básicas
1. Ingresa el primer número usando los botones numéricos (0-9)
2. Presiona el operador deseado (+, -, *, /)
3. Ingresa el segundo número
4. Presiona **=** para obtener el resultado

**Ejemplo:** `5 + 3 =` → Resultado: `8`

### Funciones Científicas
1. Ingresa un número
2. Presiona el botón de la función científica deseada
3. El resultado se mostrará automáticamente

**Ejemplos:**
- `90` → **sin** → Resultado: `1.0` (seno de 90°)
- `16` → **√** → Resultado: `4.0` (raíz cuadrada de 16)
- `5` → **x²** → Resultado: `25` (5 al cuadrado)
- `100` → **log** → Resultado: `2.0` (log₁₀ de 100)

### Sistema de Memoria
1. **Guardar en memoria:**
   - Calcula o ingresa un número
   - Presiona **M+** para sumar a la memoria
   - Presiona **M-** para restar de la memoria

2. **Recuperar de memoria:**
   - Presiona **MR** para mostrar el valor guardado

3. **Limpiar memoria:**
   - Presiona **MC** para resetear la memoria a 0

**Ejemplo de uso:**
```
5 + 3 = → 8
M+ → (Guarda 8 en memoria)
2 * 4 = → 8
M+ → (Memoria ahora tiene 16)
MR → Muestra 16
```

### Funciones Especiales
- **C (Clear):** Borra toda la expresión y reinicia
- **CE (Clear Entry):** Borra el último carácter ingresado
- **+/-:** Cambia el signo del número actual (positivo ↔ negativo)

## 🎨 Interfaz

La calculadora cuenta con un diseño moderno y profesional:
- **Pantalla grande** con números claros y legibles
- **Botones organizados** por categorías con colores distintivos:
  - 🔵 Azul: Operaciones básicas
  - 🟣 Morado: Funciones científicas
  - 🔴 Rojo: Memoria
  - 🟠 Naranja: Funciones especiales
  - ⚪ Blanco: Números

## ⚠️ Manejo de Errores

La calculadora detecta y maneja los siguientes errores:

- **División por cero:** Muestra "Error: Div/0"
- **Raíz cuadrada de número negativo:** Muestra "Error: √ negativa"
- **Logaritmo de número ≤ 0:** Muestra "Error: log ≤ 0"
- **Expresiones inválidas:** Muestra "Error"

## 🔧 Estructura del Código

```
calculadora.py
├── Clase Calculadora
│   ├── __init__() - Inicialización
│   ├── configurar_estilo() - Colores y diseño
│   ├── crear_pantalla() - Display
│   ├── crear_botones() - Interfaz de botones
│   ├── agregar_caracter() - Input de caracteres
│   ├── calcular() - Evaluación de expresiones
│   ├── funcion_cientifica() - Funciones matemáticas
│   ├── memoria_* - Sistema de memoria
│   └── limpiar/borrar - Funciones de limpieza
└── main() - Función principal
```

## 📝 Notas Técnicas

- Las funciones trigonométricas trabajan en **grados**, no radianes
- El logaritmo utiliza base 10 (log₁₀)
- La calculadora usa `eval()` para evaluar expresiones matemáticas
- Los resultados se muestran con precisión decimal completa

## 🐛 Solución de Problemas

### La calculadora no inicia
- Verifica que Python esté instalado correctamente
- Asegúrate de que Tkinter esté disponible: `python -m tkinter`

### Error de importación
```bash
# Instalar tkinter en Ubuntu/Debian
sudo apt-get install python3-tk

# En Fedora/RHEL
sudo dnf install python3-tkinter
```

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de:
- Reportar bugs
- Sugerir mejoras
- Añadir nuevas funcionalidades
- Mejorar el diseño

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal.

## ✨ Características Futuras (Posibles Mejoras)

- [ ] Historial de cálculos
- [ ] Modo de ángulos (grados/radianes)
- [ ] Más funciones científicas (factorial, exponencial, etc.)
- [ ] Temas de color personalizables
- [ ] Atajos de teclado
- [ ] Exportar resultados

---

**Desarrollado con ❤️ usando Python y Tkinter**