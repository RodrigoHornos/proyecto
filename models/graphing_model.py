"""
Modelo para graficación de funciones matemáticas.

Este módulo proporciona funcionalidades para graficar funciones,
calcular puntos, encontrar raíces y analizar propiedades.
"""

from typing import List, Tuple, Optional, Callable, Dict
import numpy as np
from sympy import symbols, sympify, lambdify, diff, solve, limit, oo
from sympy.core.sympify import SympifyError


class GraphingModel:
    """
    Modelo para graficación de funciones matemáticas.
    
    Attributes:
        x_min: Límite inferior del eje X
        x_max: Límite superior del eje X
        y_min: Límite inferior del eje Y
        y_max: Límite superior del eje Y
        num_points: Número de puntos a calcular
    """
    
    def __init__(
        self,
        x_min: float = -10,
        x_max: float = 10,
        y_min: float = -10,
        y_max: float = 10,
        num_points: int = 1000
    ):
        """
        Inicializa el modelo de graficación.
        
        Args:
            x_min: Límite inferior del eje X
            x_max: Límite superior del eje X
            y_min: Límite inferior del eje Y
            y_max: Límite superior del eje Y
            num_points: Número de puntos a calcular
            
        Raises:
            ValueError: Si los límites o num_points no son válidos
        """
        if x_min >= x_max:
            raise ValueError("x_min debe ser menor que x_max")
        if y_min >= y_max:
            raise ValueError("y_min debe ser menor que y_max")
        if num_points < 10:
            raise ValueError("num_points debe ser al menos 10")
        
        self._x_min = x_min
        self._x_max = x_max
        self._y_min = y_min
        self._y_max = y_max
        self._num_points = num_points
        self._x_symbol = symbols('x')
    
    @property
    def x_min(self) -> float:
        """Obtiene el límite inferior de X."""
        return self._x_min
    
    @x_min.setter
    def x_min(self, value: float) -> None:
        """Establece el límite inferior de X."""
        if value >= self._x_max:
            raise ValueError("x_min debe ser menor que x_max")
        self._x_min = value
    
    @property
    def x_max(self) -> float:
        """Obtiene el límite superior de X."""
        return self._x_max
    
    @x_max.setter
    def x_max(self, value: float) -> None:
        """Establece el límite superior de X."""
        if value <= self._x_min:
            raise ValueError("x_max debe ser mayor que x_min")
        self._x_max = value
    
    @property
    def y_min(self) -> float:
        """Obtiene el límite inferior de Y."""
        return self._y_min
    
    @y_min.setter
    def y_min(self, value: float) -> None:
        """Establece el límite inferior de Y."""
        if value >= self._y_max:
            raise ValueError("y_min debe ser menor que y_max")
        self._y_min = value
    
    @property
    def y_max(self) -> float:
        """Obtiene el límite superior de Y."""
        return self._y_max
    
    @y_max.setter
    def y_max(self, value: float) -> None:
        """Establece el límite superior de Y."""
        if value <= self._y_min:
            raise ValueError("y_max debe ser mayor que y_min")
        self._y_max = value
    
    @property
    def num_points(self) -> int:
        """Obtiene el número de puntos."""
        return self._num_points
    
    @num_points.setter
    def num_points(self, value: int) -> None:
        """Establece el número de puntos."""
        if value < 10:
            raise ValueError("num_points debe ser al menos 10")
        self._num_points = value
    
    def parse_function(self, expression: str) -> Callable:
        """
        Parsea una expresión matemática y retorna una función evaluable.
        
        Args:
            expression: Expresión matemática como string
            
        Returns:
            Función evaluable
            
        Raises:
            ValueError: Si la expresión no es válida
        """
        try:
            expr = sympify(expression)
            func = lambdify(self._x_symbol, expr, modules=['numpy'])
            return func
        except (SympifyError, Exception) as e:
            raise ValueError(f"Expresión inválida: {str(e)}")
    
    def calculate_points(
        self,
        expression: str,
        x_range: Optional[Tuple[float, float]] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula puntos de la función en el rango especificado.
        
        Args:
            expression: Expresión matemática
            x_range: Rango personalizado (x_min, x_max), usa self.x_min/x_max si es None
            
        Returns:
            Tupla (x_values, y_values)
            
        Raises:
            ValueError: Si la expresión no es válida
        """
        func = self.parse_function(expression)
        
        if x_range is None:
            x_min, x_max = self._x_min, self._x_max
        else:
            x_min, x_max = x_range
        
        x_values = np.linspace(x_min, x_max, self._num_points)
        
        try:
            y_values = func(x_values)
            # Manejar valores infinitos o NaN
            y_values = np.where(np.isfinite(y_values), y_values, np.nan)
        except Exception as e:
            raise ValueError(f"Error al evaluar la función: {str(e)}")
        
        return x_values, y_values
    
    def find_roots(
        self,
        expression: str,
        x_range: Optional[Tuple[float, float]] = None
    ) -> List[float]:
        """
        Encuentra las raíces de la función en el rango especificado.
        
        Args:
            expression: Expresión matemática
            x_range: Rango de búsqueda (x_min, x_max)
            
        Returns:
            Lista de raíces encontradas
            
        Raises:
            ValueError: Si la expresión no es válida
        """
        try:
            expr = sympify(expression)
            roots = solve(expr, self._x_symbol)
            
            # Filtrar raíces reales en el rango
            real_roots = []
            if x_range is None:
                x_min, x_max = self._x_min, self._x_max
            else:
                x_min, x_max = x_range
            
            for root in roots:
                try:
                    root_val = complex(root)
                    if root_val.imag == 0:  # Solo raíces reales
                        root_real = root_val.real
                        if x_min <= root_real <= x_max:
                            real_roots.append(root_real)
                except:
                    pass
            
            return sorted(real_roots)
        except Exception as e:
            raise ValueError(f"Error al encontrar raíces: {str(e)}")
    
    def calculate_derivative(self, expression: str) -> str:
        """
        Calcula la derivada de la función.
        
        Args:
            expression: Expresión matemática
            
        Returns:
            Derivada como string
            
        Raises:
            ValueError: Si la expresión no es válida
        """
        try:
            expr = sympify(expression)
            derivative = diff(expr, self._x_symbol)
            return str(derivative)
        except Exception as e:
            raise ValueError(f"Error al calcular derivada: {str(e)}")
    
    def evaluate_at_point(self, expression: str, x_value: float) -> float:
        """
        Evalúa la función en un punto específico.
        
        Args:
            expression: Expresión matemática
            x_value: Valor de x donde evaluar
            
        Returns:
            Valor de f(x)
            
        Raises:
            ValueError: Si la expresión no es válida o la evaluación falla
        """
        func = self.parse_function(expression)
        try:
            result = func(x_value)
            if not np.isfinite(result):
                raise ValueError("El resultado no es finito")
            return float(result)
        except Exception as e:
            raise ValueError(f"Error al evaluar en x={x_value}: {str(e)}")
    
    def find_extrema(
        self,
        expression: str,
        x_range: Optional[Tuple[float, float]] = None
    ) -> Dict[str, List[Tuple[float, float]]]:
        """
        Encuentra los extremos (máximos y mínimos) de la función.
        
        Args:
            expression: Expresión matemática
            x_range: Rango de búsqueda
            
        Returns:
            Diccionario con 'maxima' y 'minima', cada uno con lista de (x, y)
            
        Raises:
            ValueError: Si la expresión no es válida
        """
        try:
            expr = sympify(expression)
            derivative = diff(expr, self._x_symbol)
            second_derivative = diff(derivative, self._x_symbol)
            
            # Encontrar puntos críticos
            critical_points = solve(derivative, self._x_symbol)
            
            if x_range is None:
                x_min, x_max = self._x_min, self._x_max
            else:
                x_min, x_max = x_range
            
            maxima = []
            minima = []
            
            for point in critical_points:
                try:
                    x_val = complex(point)
                    if x_val.imag == 0:  # Solo puntos reales
                        x_real = float(x_val.real)
                        if x_min <= x_real <= x_max:
                            # Evaluar segunda derivada
                            second_deriv_val = second_derivative.subs(self._x_symbol, point)
                            y_val = float(expr.subs(self._x_symbol, point))
                            
                            if second_deriv_val < 0:
                                maxima.append((x_real, y_val))
                            elif second_deriv_val > 0:
                                minima.append((x_real, y_val))
                except:
                    pass
            
            return {'maxima': maxima, 'minima': minima}
        except Exception as e:
            raise ValueError(f"Error al encontrar extremos: {str(e)}")
    
    def calculate_limit(
        self,
        expression: str,
        point: float,
        direction: str = 'both'
    ) -> Dict[str, Optional[float]]:
        """
        Calcula el límite de la función en un punto.
        
        Args:
            expression: Expresión matemática
            point: Punto donde calcular el límite
            direction: 'left', 'right', o 'both'
            
        Returns:
            Diccionario con límites calculados
            
        Raises:
            ValueError: Si la expresión no es válida o direction no es válido
        """
        if direction not in ['left', 'right', 'both']:
            raise ValueError("direction debe ser 'left', 'right' o 'both'")
        
        try:
            expr = sympify(expression)
            results = {}
            
            if direction in ['left', 'both']:
                try:
                    lim_left = limit(expr, self._x_symbol, point, '-')
                    results['left'] = float(lim_left) if lim_left.is_finite else None
                except:
                    results['left'] = None
            
            if direction in ['right', 'both']:
                try:
                    lim_right = limit(expr, self._x_symbol, point, '+')
                    results['right'] = float(lim_right) if lim_right.is_finite else None
                except:
                    results['right'] = None
            
            if direction == 'both':
                if results.get('left') == results.get('right'):
                    results['limit'] = results['left']
                else:
                    results['limit'] = None
            
            return results
        except Exception as e:
            raise ValueError(f"Error al calcular límite: {str(e)}")
    
    def find_intersections(
        self,
        expression1: str,
        expression2: str,
        x_range: Optional[Tuple[float, float]] = None
    ) -> List[Tuple[float, float]]:
        """
        Encuentra los puntos de intersección entre dos funciones.
        
        Args:
            expression1: Primera expresión matemática
            expression2: Segunda expresión matemática
            x_range: Rango de búsqueda
            
        Returns:
            Lista de puntos de intersección (x, y)
            
        Raises:
            ValueError: Si alguna expresión no es válida
        """
        try:
            expr1 = sympify(expression1)
            expr2 = sympify(expression2)
            
            # Resolver expr1 - expr2 = 0
            diff_expr = expr1 - expr2
            solutions = solve(diff_expr, self._x_symbol)
            
            if x_range is None:
                x_min, x_max = self._x_min, self._x_max
            else:
                x_min, x_max = x_range
            
            intersections = []
            for sol in solutions:
                try:
                    x_val = complex(sol)
                    if x_val.imag == 0:  # Solo soluciones reales
                        x_real = float(x_val.real)
                        if x_min <= x_real <= x_max:
                            y_val = float(expr1.subs(self._x_symbol, sol))
                            intersections.append((x_real, y_val))
                except:
                    pass
            
            return sorted(intersections, key=lambda p: p[0])
        except Exception as e:
            raise ValueError(f"Error al encontrar intersecciones: {str(e)}")
    
    def calculate_area_under_curve(
        self,
        expression: str,
        x_start: float,
        x_end: float
    ) -> float:
        """
        Calcula el área bajo la curva usando integración numérica.
        
        Args:
            expression: Expresión matemática
            x_start: Límite inferior de integración
            x_end: Límite superior de integración
            
        Returns:
            Área calculada
            
        Raises:
            ValueError: Si la expresión no es válida o los límites son inválidos
        """
        if x_start >= x_end:
            raise ValueError("x_start debe ser menor que x_end")
        
        func = self.parse_function(expression)
        
        try:
            # Usar regla del trapecio
            x_values = np.linspace(x_start, x_end, self._num_points)
            y_values = func(x_values)
            # Asegurar que y_values es un array
            if np.isscalar(y_values):
                y_values = np.full_like(x_values, y_values)
            
            # Filtrar valores no finitos
            mask = np.isfinite(y_values)
            if not np.any(mask):
                raise ValueError("No hay valores finitos en el rango")
            
            # Usar trapezoid (numpy 2.x) o trapz (numpy 1.x)
            if hasattr(np, 'trapezoid'):
                area = np.trapezoid(y_values[mask], x_values[mask])
            else:
                area = np.trapz(y_values[mask], x_values[mask])
            return float(area)
        except Exception as e:
            raise ValueError(f"Error al calcular área: {str(e)}")
    
    def __str__(self) -> str:
        """Representación en string del modelo."""
        return (f"GraphingModel(x=[{self._x_min}, {self._x_max}], "
                f"y=[{self._y_min}, {self._y_max}], points={self._num_points})")
    
    def __repr__(self) -> str:
        """Representación detallada del modelo."""
        return (f"GraphingModel(x_min={self._x_min}, x_max={self._x_max}, "
                f"y_min={self._y_min}, y_max={self._y_max}, "
                f"num_points={self._num_points})")

# Made with Bob
