# 🔧 Instalación de Tkinter en macOS

Tu sistema tiene Python 3.14 instalado vía Homebrew, pero tkinter no está disponible. Aquí están las soluciones:

## Opción 1: Reinstalar Python con soporte para Tkinter (Recomendado)

```bash
# Reinstalar Python con tkinter
brew reinstall python-tk@3.14
```

## Opción 2: Usar Python del sistema

macOS incluye Python con tkinter. Prueba:

```bash
# Verificar si el Python del sistema tiene tkinter
/usr/bin/python3 -m tkinter

# Si funciona, ejecutar la calculadora con:
/usr/bin/python3 calculadora.py
```

## Opción 3: Instalar Python desde python.org

1. Descarga Python desde https://www.python.org/downloads/
2. Instala el paquete .pkg
3. Esta versión incluye tkinter por defecto

## Verificar instalación de Tkinter

Después de instalar, verifica que tkinter funciona:

```bash
python3 -c "import tkinter; print('Tkinter OK')"
```

Si ves "Tkinter OK", la calculadora funcionará correctamente.

## Alternativa: Versión de Consola

Si prefieres no instalar tkinter, he creado una versión de consola de la calculadora en `calculadora_consola.py` que funciona sin dependencias adicionales.

```bash
python3 calculadora_consola.py