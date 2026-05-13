#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora Científica Avanzada con Arquitectura MVC
Punto de entrada principal de la aplicación
"""

import tkinter as tk
from views import AdvancedCalculatorView
from controllers import AdvancedCalculatorController


def main():
    """
    Función principal que inicializa la aplicación con arquitectura MVC
    
    Flujo de inicialización:
    1. Crear ventana raíz de Tkinter
    2. Crear la Vista Avanzada (AdvancedCalculatorView)
    3. Crear el Controlador Avanzado (AdvancedCalculatorController)
    4. El Controlador crea todos los Modelos (Calculator, Memory, History, Config, etc.)
    5. El Controlador conecta Vista y Modelos
    6. Iniciar el loop de eventos de Tkinter
    """
    # Crear ventana raíz
    root = tk.Tk()
    
    # Crear vista avanzada
    view = AdvancedCalculatorView(root)
    
    # Crear controlador avanzado (conecta vista y todos los modelos)
    controller = AdvancedCalculatorController(view)
    
    # Iniciar aplicación
    root.mainloop()


if __name__ == "__main__":
    main()

# Made with Bob
