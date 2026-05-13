"""
Modelo para funciones científicas avanzadas.

Este módulo proporciona funciones matemáticas y científicas avanzadas
que complementan las operaciones básicas de la calculadora.
"""

import math
from typing import Union, Tuple, List
from decimal import Decimal, getcontext


# Configurar precisión decimal
getcontext().prec = 50


class ScientificModel:
    """
    Modelo para operaciones científicas avanzadas.
    
    Proporciona funciones trigonométricas inversas, hiperbólicas,
    estadísticas, conversiones de unidades y más.
    """
    
    def __init__(self):
        """Inicializa el modelo científico."""
        self._angle_mode = 'rad'  # 'rad', 'deg', 'grad'
        self._last_result = None
    
    @property
    def angle_mode(self) -> str:
        """Obtiene el modo de ángulos actual."""
        return self._angle_mode
    
    @angle_mode.setter
    def angle_mode(self, mode: str) -> None:
        """
        Establece el modo de ángulos.
        
        Args:
            mode: 'rad', 'deg', o 'grad'
            
        Raises:
            ValueError: Si el modo no es válido
        """
        if mode not in ['rad', 'deg', 'grad']:
            raise ValueError(f"Modo de ángulo inválido: {mode}")
        self._angle_mode = mode
    
    def _to_radians(self, angle: float) -> float:
        """
        Convierte un ángulo al modo actual a radianes.
        
        Args:
            angle: Ángulo en el modo actual
            
        Returns:
            Ángulo en radianes
        """
        if self._angle_mode == 'deg':
            return math.radians(angle)
        elif self._angle_mode == 'grad':
            return angle * math.pi / 200
        return angle
    
    def _from_radians(self, angle: float) -> float:
        """
        Convierte un ángulo de radianes al modo actual.
        
        Args:
            angle: Ángulo en radianes
            
        Returns:
            Ángulo en el modo actual
        """
        if self._angle_mode == 'deg':
            return math.degrees(angle)
        elif self._angle_mode == 'grad':
            return angle * 200 / math.pi
        return angle
    
    # Funciones trigonométricas inversas
    
    def asin(self, x: float) -> float:
        """
        Calcula el arcoseno.
        
        Args:
            x: Valor entre -1 y 1
            
        Returns:
            Arcoseno en el modo de ángulo actual
            
        Raises:
            ValueError: Si x está fuera del rango [-1, 1]
        """
        if not -1 <= x <= 1:
            raise ValueError("El valor debe estar entre -1 y 1")
        result = math.asin(x)
        return self._from_radians(result)
    
    def acos(self, x: float) -> float:
        """
        Calcula el arcocoseno.
        
        Args:
            x: Valor entre -1 y 1
            
        Returns:
            Arcocoseno en el modo de ángulo actual
            
        Raises:
            ValueError: Si x está fuera del rango [-1, 1]
        """
        if not -1 <= x <= 1:
            raise ValueError("El valor debe estar entre -1 y 1")
        result = math.acos(x)
        return self._from_radians(result)
    
    def atan(self, x: float) -> float:
        """
        Calcula el arcotangente.
        
        Args:
            x: Valor numérico
            
        Returns:
            Arcotangente en el modo de ángulo actual
        """
        result = math.atan(x)
        return self._from_radians(result)
    
    def atan2(self, y: float, x: float) -> float:
        """
        Calcula el arcotangente de y/x considerando el cuadrante.
        
        Args:
            y: Coordenada y
            x: Coordenada x
            
        Returns:
            Arcotangente en el modo de ángulo actual
        """
        result = math.atan2(y, x)
        return self._from_radians(result)
    
    # Funciones hiperbólicas
    
    def sinh(self, x: float) -> float:
        """Calcula el seno hiperbólico."""
        return math.sinh(x)
    
    def cosh(self, x: float) -> float:
        """Calcula el coseno hiperbólico."""
        return math.cosh(x)
    
    def tanh(self, x: float) -> float:
        """Calcula la tangente hiperbólica."""
        return math.tanh(x)
    
    # Funciones hiperbólicas inversas
    
    def asinh(self, x: float) -> float:
        """Calcula el arcoseno hiperbólico."""
        return math.asinh(x)
    
    def acosh(self, x: float) -> float:
        """
        Calcula el arcocoseno hiperbólico.
        
        Args:
            x: Valor >= 1
            
        Returns:
            Arcocoseno hiperbólico
            
        Raises:
            ValueError: Si x < 1
        """
        if x < 1:
            raise ValueError("El valor debe ser >= 1")
        return math.acosh(x)
    
    def atanh(self, x: float) -> float:
        """
        Calcula la arcotangente hiperbólica.
        
        Args:
            x: Valor entre -1 y 1 (exclusivo)
            
        Returns:
            Arcotangente hiperbólica
            
        Raises:
            ValueError: Si |x| >= 1
        """
        if abs(x) >= 1:
            raise ValueError("El valor debe estar entre -1 y 1 (exclusivo)")
        return math.atanh(x)
    
    # Funciones exponenciales y logarítmicas
    
    def exp(self, x: float) -> float:
        """Calcula e^x."""
        return math.exp(x)
    
    def ln(self, x: float) -> float:
        """
        Calcula el logaritmo natural (base e).
        
        Args:
            x: Valor > 0
            
        Returns:
            Logaritmo natural
            
        Raises:
            ValueError: Si x <= 0
        """
        if x <= 0:
            raise ValueError("El logaritmo requiere un valor positivo")
        return math.log(x)
    
    def log10(self, x: float) -> float:
        """
        Calcula el logaritmo base 10.
        
        Args:
            x: Valor > 0
            
        Returns:
            Logaritmo base 10
            
        Raises:
            ValueError: Si x <= 0
        """
        if x <= 0:
            raise ValueError("El logaritmo requiere un valor positivo")
        return math.log10(x)
    
    def log(self, x: float, base: float = 10) -> float:
        """
        Calcula el logaritmo en cualquier base.
        
        Args:
            x: Valor > 0
            base: Base del logaritmo > 0 y != 1
            
        Returns:
            Logaritmo en la base especificada
            
        Raises:
            ValueError: Si x <= 0 o base inválida
        """
        if x <= 0:
            raise ValueError("El logaritmo requiere un valor positivo")
        if base <= 0 or base == 1:
            raise ValueError("La base debe ser > 0 y != 1")
        return math.log(x, base)
    
    # Funciones de potencia y raíces
    
    def sqrt(self, x: float) -> float:
        """
        Calcula la raíz cuadrada.
        
        Args:
            x: Valor >= 0
            
        Returns:
            Raíz cuadrada
            
        Raises:
            ValueError: Si x < 0
        """
        if x < 0:
            raise ValueError("No se puede calcular la raíz cuadrada de un número negativo")
        return math.sqrt(x)
    
    def cbrt(self, x: float) -> float:
        """Calcula la raíz cúbica."""
        return math.copysign(abs(x) ** (1/3), x)
    
    def nroot(self, x: float, n: int) -> float:
        """
        Calcula la raíz n-ésima.
        
        Args:
            x: Valor numérico
            n: Índice de la raíz
            
        Returns:
            Raíz n-ésima
            
        Raises:
            ValueError: Si n es par y x < 0
        """
        if n % 2 == 0 and x < 0:
            raise ValueError("No se puede calcular raíz par de número negativo")
        if n % 2 == 0:
            return x ** (1/n)
        return math.copysign(abs(x) ** (1/n), x)
    
    # Funciones combinatorias
    
    def factorial(self, n: int) -> int:
        """
        Calcula el factorial.
        
        Args:
            n: Entero >= 0
            
        Returns:
            n!
            
        Raises:
            ValueError: Si n < 0 o no es entero
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("El factorial requiere un entero no negativo")
        return math.factorial(n)
    
    def permutations(self, n: int, r: int) -> int:
        """
        Calcula permutaciones P(n,r) = n!/(n-r)!
        
        Args:
            n: Total de elementos
            r: Elementos a permutar
            
        Returns:
            Número de permutaciones
            
        Raises:
            ValueError: Si n < 0, r < 0, o r > n
        """
        if n < 0 or r < 0:
            raise ValueError("n y r deben ser no negativos")
        if r > n:
            raise ValueError("r no puede ser mayor que n")
        return math.perm(n, r)
    
    def combinations(self, n: int, r: int) -> int:
        """
        Calcula combinaciones C(n,r) = n!/(r!(n-r)!)
        
        Args:
            n: Total de elementos
            r: Elementos a combinar
            
        Returns:
            Número de combinaciones
            
        Raises:
            ValueError: Si n < 0, r < 0, o r > n
        """
        if n < 0 or r < 0:
            raise ValueError("n y r deben ser no negativos")
        if r > n:
            raise ValueError("r no puede ser mayor que n")
        return math.comb(n, r)
    
    # Funciones de redondeo y valor absoluto
    
    def abs(self, x: float) -> float:
        """Calcula el valor absoluto."""
        return abs(x)
    
    def floor(self, x: float) -> int:
        """Redondea hacia abajo."""
        return math.floor(x)
    
    def ceil(self, x: float) -> int:
        """Redondea hacia arriba."""
        return math.ceil(x)
    
    def round(self, x: float, decimals: int = 0) -> float:
        """
        Redondea al número de decimales especificado.
        
        Args:
            x: Valor a redondear
            decimals: Número de decimales
            
        Returns:
            Valor redondeado
        """
        return round(x, decimals)
    
    def trunc(self, x: float) -> int:
        """Trunca la parte decimal."""
        return math.trunc(x)
    
    # Funciones de módulo y resto
    
    def mod(self, x: float, y: float) -> float:
        """
        Calcula el módulo (resto de la división).
        
        Args:
            x: Dividendo
            y: Divisor
            
        Returns:
            x mod y
            
        Raises:
            ValueError: Si y == 0
        """
        if y == 0:
            raise ValueError("División por cero")
        return x % y
    
    def gcd(self, a: int, b: int) -> int:
        """
        Calcula el máximo común divisor.
        
        Args:
            a: Primer número
            b: Segundo número
            
        Returns:
            MCD de a y b
        """
        return math.gcd(a, b)
    
    def lcm(self, a: int, b: int) -> int:
        """
        Calcula el mínimo común múltiplo.
        
        Args:
            a: Primer número
            b: Segundo número
            
        Returns:
            MCM de a y b
        """
        return math.lcm(a, b)
    
    # Funciones estadísticas básicas
    
    def mean(self, values: List[float]) -> float:
        """
        Calcula la media aritmética.
        
        Args:
            values: Lista de valores
            
        Returns:
            Media
            
        Raises:
            ValueError: Si la lista está vacía
        """
        if not values:
            raise ValueError("La lista no puede estar vacía")
        return sum(values) / len(values)
    
    def median(self, values: List[float]) -> float:
        """
        Calcula la mediana.
        
        Args:
            values: Lista de valores
            
        Returns:
            Mediana
            
        Raises:
            ValueError: Si la lista está vacía
        """
        if not values:
            raise ValueError("La lista no puede estar vacía")
        sorted_values = sorted(values)
        n = len(sorted_values)
        if n % 2 == 0:
            return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
        return sorted_values[n//2]
    
    def std_dev(self, values: List[float], sample: bool = True) -> float:
        """
        Calcula la desviación estándar.
        
        Args:
            values: Lista de valores
            sample: True para muestra, False para población
            
        Returns:
            Desviación estándar
            
        Raises:
            ValueError: Si la lista está vacía o tiene un solo elemento (muestra)
        """
        if not values:
            raise ValueError("La lista no puede estar vacía")
        if sample and len(values) < 2:
            raise ValueError("Se necesitan al menos 2 valores para la desviación estándar de muestra")
        
        mean_val = self.mean(values)
        variance = sum((x - mean_val) ** 2 for x in values)
        divisor = len(values) - 1 if sample else len(values)
        return math.sqrt(variance / divisor)
    
    # Conversiones de unidades de ángulo
    
    def deg_to_rad(self, degrees: float) -> float:
        """Convierte grados a radianes."""
        return math.radians(degrees)
    
    def rad_to_deg(self, radians: float) -> float:
        """Convierte radianes a grados."""
        return math.degrees(radians)
    
    def deg_to_grad(self, degrees: float) -> float:
        """Convierte grados a gradianes."""
        return degrees * 10 / 9
    
    def grad_to_deg(self, gradians: float) -> float:
        """Convierte gradianes a grados."""
        return gradians * 9 / 10
    
    def rad_to_grad(self, radians: float) -> float:
        """Convierte radianes a gradianes."""
        return radians * 200 / math.pi
    
    def grad_to_rad(self, gradians: float) -> float:
        """Convierte gradianes a radianes."""
        return gradians * math.pi / 200
    
    # Constantes matemáticas
    
    @property
    def pi(self) -> float:
        """Retorna el valor de π."""
        return math.pi
    
    @property
    def e(self) -> float:
        """Retorna el valor de e."""
        return math.e
    
    @property
    def tau(self) -> float:
        """Retorna el valor de τ (2π)."""
        return math.tau
    
    @property
    def phi(self) -> float:
        """Retorna el valor de φ (proporción áurea)."""
        return (1 + math.sqrt(5)) / 2
    
    def __str__(self) -> str:
        """Representación en string del modelo."""
        return f"ScientificModel(angle_mode={self._angle_mode})"
    
    def __repr__(self) -> str:
        """Representación detallada del modelo."""
        return f"ScientificModel(angle_mode={self._angle_mode!r}, last_result={self._last_result})"

# Made with Bob
