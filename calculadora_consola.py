#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Consola (Versión sin GUI)
Alternativa que funciona sin tkinter
"""

import math
import sys

class CalculadoraConsola:
    def __init__(self):
        self.memoria = 0
        self.historial = []
        
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("🧮  CALCULADORA CIENTÍFICA  🧮".center(50))
        print("="*50)
        print("\n📊 OPERACIONES BÁSICAS:")
        print("  1. Suma (+)")
        print("  2. Resta (-)")
        print("  3. Multiplicación (*)")
        print("  4. División (/)")
        print("\n🔬 FUNCIONES CIENTÍFICAS:")
        print("  5. Seno (sin)")
        print("  6. Coseno (cos)")
        print("  7. Tangente (tan)")
        print("  8. Raíz cuadrada (√)")
        print("  9. Potencia al cuadrado (x²)")
        print("  10. Logaritmo base 10 (log)")
        print("\n💾 MEMORIA:")
        print("  11. Guardar en memoria (M+)")
        print("  12. Restar de memoria (M-)")
        print("  13. Recuperar memoria (MR)")
        print("  14. Limpiar memoria (MC)")
        print("\n📋 OTRAS OPCIONES:")
        print("  15. Ver historial")
        print("  16. Limpiar historial")
        print("  0. Salir")
        print("="*50)
        
    def operacion_basica(self, operacion):
        """Realiza operaciones básicas"""
        try:
            num1 = float(input("\n📝 Ingresa el primer número: "))
            num2 = float(input("📝 Ingresa el segundo número: "))
            
            resultado = 0
            simbolo = ""
            
            if operacion == '+':
                resultado = num1 + num2
                simbolo = "+"
            elif operacion == '-':
                resultado = num1 - num2
                simbolo = "-"
            elif operacion == '*':
                resultado = num1 * num2
                simbolo = "×"
            elif operacion == '/':
                if num2 == 0:
                    print("\n❌ Error: No se puede dividir por cero")
                    return
                resultado = num1 / num2
                simbolo = "÷"
            
            print(f"\n✅ Resultado: {num1} {simbolo} {num2} = {resultado}")
            self.historial.append(f"{num1} {simbolo} {num2} = {resultado}")
            
            # Preguntar si guardar en memoria
            guardar = input("\n💾 ¿Guardar resultado en memoria? (s/n): ").lower()
            if guardar == 's':
                self.memoria = resultado
                print(f"✅ Guardado en memoria: {self.memoria}")
                
        except ValueError:
            print("\n❌ Error: Ingresa números válidos")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def funcion_cientifica(self, funcion):
        """Aplica funciones científicas"""
        try:
            num = float(input("\n📝 Ingresa el número: "))
            
            resultado = 0
            texto = ""
            
            if funcion == 'sin':
                resultado = math.sin(math.radians(num))
                texto = f"sin({num}°)"
            elif funcion == 'cos':
                resultado = math.cos(math.radians(num))
                texto = f"cos({num}°)"
            elif funcion == 'tan':
                resultado = math.tan(math.radians(num))
                texto = f"tan({num}°)"
            elif funcion == 'sqrt':
                if num < 0:
                    print("\n❌ Error: No se puede calcular raíz cuadrada de número negativo")
                    return
                resultado = math.sqrt(num)
                texto = f"√{num}"
            elif funcion == 'pow':
                resultado = num ** 2
                texto = f"{num}²"
            elif funcion == 'log':
                if num <= 0:
                    print("\n❌ Error: El logaritmo requiere un número positivo")
                    return
                resultado = math.log10(num)
                texto = f"log₁₀({num})"
            
            print(f"\n✅ Resultado: {texto} = {resultado}")
            self.historial.append(f"{texto} = {resultado}")
            
            # Preguntar si guardar en memoria
            guardar = input("\n💾 ¿Guardar resultado en memoria? (s/n): ").lower()
            if guardar == 's':
                self.memoria = resultado
                print(f"✅ Guardado en memoria: {self.memoria}")
                
        except ValueError:
            print("\n❌ Error: Ingresa un número válido")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def memoria_sumar(self):
        """Suma a la memoria"""
        try:
            num = float(input("\n📝 Ingresa el número a sumar a memoria: "))
            self.memoria += num
            print(f"✅ Memoria actualizada: {self.memoria}")
        except ValueError:
            print("\n❌ Error: Ingresa un número válido")
    
    def memoria_restar(self):
        """Resta de la memoria"""
        try:
            num = float(input("\n📝 Ingresa el número a restar de memoria: "))
            self.memoria -= num
            print(f"✅ Memoria actualizada: {self.memoria}")
        except ValueError:
            print("\n❌ Error: Ingresa un número válido")
    
    def memoria_recuperar(self):
        """Muestra el valor de la memoria"""
        print(f"\n💾 Valor en memoria: {self.memoria}")
    
    def memoria_limpiar(self):
        """Limpia la memoria"""
        self.memoria = 0
        print("\n✅ Memoria limpiada (0)")
    
    def ver_historial(self):
        """Muestra el historial de operaciones"""
        if not self.historial:
            print("\n📋 El historial está vacío")
        else:
            print("\n" + "="*50)
            print("📋 HISTORIAL DE OPERACIONES".center(50))
            print("="*50)
            for i, operacion in enumerate(self.historial, 1):
                print(f"  {i}. {operacion}")
            print("="*50)
    
    def limpiar_historial(self):
        """Limpia el historial"""
        self.historial = []
        print("\n✅ Historial limpiado")
    
    def ejecutar(self):
        """Ejecuta el bucle principal de la calculadora"""
        print("\n🎉 ¡Bienvenido a la Calculadora Científica! 🎉")
        
        while True:
            self.mostrar_menu()
            
            try:
                opcion = input("\n👉 Selecciona una opción (0-16): ").strip()
                
                if opcion == '0':
                    print("\n👋 ¡Hasta luego! Gracias por usar la calculadora.")
                    sys.exit(0)
                elif opcion == '1':
                    self.operacion_basica('+')
                elif opcion == '2':
                    self.operacion_basica('-')
                elif opcion == '3':
                    self.operacion_basica('*')
                elif opcion == '4':
                    self.operacion_basica('/')
                elif opcion == '5':
                    self.funcion_cientifica('sin')
                elif opcion == '6':
                    self.funcion_cientifica('cos')
                elif opcion == '7':
                    self.funcion_cientifica('tan')
                elif opcion == '8':
                    self.funcion_cientifica('sqrt')
                elif opcion == '9':
                    self.funcion_cientifica('pow')
                elif opcion == '10':
                    self.funcion_cientifica('log')
                elif opcion == '11':
                    self.memoria_sumar()
                elif opcion == '12':
                    self.memoria_restar()
                elif opcion == '13':
                    self.memoria_recuperar()
                elif opcion == '14':
                    self.memoria_limpiar()
                elif opcion == '15':
                    self.ver_historial()
                elif opcion == '16':
                    self.limpiar_historial()
                else:
                    print("\n❌ Opción no válida. Por favor, selecciona un número del 0 al 16.")
                
                input("\n⏎ Presiona Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                input("\n⏎ Presiona Enter para continuar...")


def main():
    """Función principal"""
    calculadora = CalculadoraConsola()
    calculadora.ejecutar()


if __name__ == "__main__":
    main()

# Made with Bob
