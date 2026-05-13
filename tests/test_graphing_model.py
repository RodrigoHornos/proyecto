"""
Tests para el modelo de graficación.
"""

import pytest
import numpy as np
from models.graphing_model import GraphingModel


@pytest.fixture
def graphing_model():
    """Fixture con modelo de graficación por defecto."""
    return GraphingModel()


@pytest.fixture
def custom_graphing_model():
    """Fixture con modelo personalizado."""
    return GraphingModel(
        x_min=-5,
        x_max=5,
        y_min=-5,
        y_max=5,
        num_points=500
    )


class TestGraphingModelInit:
    """Tests para inicialización del modelo."""
    
    def test_default_initialization(self):
        """Test inicialización con valores por defecto."""
        model = GraphingModel()
        assert model.x_min == -10
        assert model.x_max == 10
        assert model.y_min == -10
        assert model.y_max == 10
        assert model.num_points == 1000
    
    def test_custom_initialization(self):
        """Test inicialización con valores personalizados."""
        model = GraphingModel(
            x_min=-5,
            x_max=5,
            y_min=-3,
            y_max=3,
            num_points=500
        )
        assert model.x_min == -5
        assert model.x_max == 5
        assert model.y_min == -3
        assert model.y_max == 3
        assert model.num_points == 500
    
    def test_invalid_x_range_raises_error(self):
        """Test que rango X inválido lanza error."""
        with pytest.raises(ValueError, match="x_min debe ser menor"):
            GraphingModel(x_min=10, x_max=5)
    
    def test_invalid_y_range_raises_error(self):
        """Test que rango Y inválido lanza error."""
        with pytest.raises(ValueError, match="y_min debe ser menor"):
            GraphingModel(y_min=10, y_max=5)
    
    def test_invalid_num_points_raises_error(self):
        """Test que num_points inválido lanza error."""
        with pytest.raises(ValueError, match="num_points debe ser al menos"):
            GraphingModel(num_points=5)
    
    def test_str_representation(self):
        """Test representación en string."""
        model = GraphingModel()
        result = str(model)
        assert 'GraphingModel' in result
        assert 'x=[-10, 10]' in result
        assert 'points=1000' in result
    
    def test_repr_representation(self):
        """Test representación detallada."""
        model = GraphingModel(x_min=-5, x_max=5)
        result = repr(model)
        assert 'GraphingModel' in result
        assert 'x_min=-5' in result
        assert 'x_max=5' in result


class TestProperties:
    """Tests para propiedades del modelo."""
    
    def test_x_min_property(self, graphing_model):
        """Test propiedad x_min."""
        assert graphing_model.x_min == -10
        graphing_model.x_min = -20
        assert graphing_model.x_min == -20
    
    def test_x_min_invalid_value(self, graphing_model):
        """Test que x_min >= x_max lanza error."""
        with pytest.raises(ValueError):
            graphing_model.x_min = 20
    
    def test_x_max_property(self, graphing_model):
        """Test propiedad x_max."""
        assert graphing_model.x_max == 10
        graphing_model.x_max = 20
        assert graphing_model.x_max == 20
    
    def test_x_max_invalid_value(self, graphing_model):
        """Test que x_max <= x_min lanza error."""
        with pytest.raises(ValueError):
            graphing_model.x_max = -20
    
    def test_y_min_property(self, graphing_model):
        """Test propiedad y_min."""
        assert graphing_model.y_min == -10
        graphing_model.y_min = -20
        assert graphing_model.y_min == -20
    
    def test_y_max_property(self, graphing_model):
        """Test propiedad y_max."""
        assert graphing_model.y_max == 10
        graphing_model.y_max = 20
        assert graphing_model.y_max == 20
    
    def test_num_points_property(self, graphing_model):
        """Test propiedad num_points."""
        assert graphing_model.num_points == 1000
        graphing_model.num_points = 500
        assert graphing_model.num_points == 500
    
    def test_num_points_invalid_value(self, graphing_model):
        """Test que num_points < 10 lanza error."""
        with pytest.raises(ValueError):
            graphing_model.num_points = 5


class TestParseFunction:
    """Tests para parseo de funciones."""
    
    def test_parse_simple_function(self, graphing_model):
        """Test parseo de función simple."""
        func = graphing_model.parse_function('x**2')
        assert callable(func)
        assert func(2) == 4
    
    def test_parse_trigonometric_function(self, graphing_model):
        """Test parseo de función trigonométrica."""
        func = graphing_model.parse_function('sin(x)')
        result = func(0)
        assert abs(result) < 1e-10
    
    def test_parse_complex_function(self, graphing_model):
        """Test parseo de función compleja."""
        func = graphing_model.parse_function('x**3 - 2*x + 1')
        assert callable(func)
    
    def test_parse_invalid_expression(self, graphing_model):
        """Test que expresión inválida lanza error."""
        with pytest.raises(ValueError, match="Expresión inválida"):
            graphing_model.parse_function('invalid expression @@')


class TestCalculatePoints:
    """Tests para cálculo de puntos."""
    
    def test_calculate_points_linear(self, graphing_model):
        """Test cálculo de puntos para función lineal."""
        x_vals, y_vals = graphing_model.calculate_points('2*x + 1')
        
        assert len(x_vals) == 1000
        assert len(y_vals) == 1000
        assert x_vals[0] == -10
        assert x_vals[-1] == 10
    
    def test_calculate_points_quadratic(self, graphing_model):
        """Test cálculo de puntos para función cuadrática."""
        x_vals, y_vals = graphing_model.calculate_points('x**2')
        
        assert len(x_vals) == 1000
        assert y_vals[500] >= 0  # En x=0, y=0
    
    def test_calculate_points_custom_range(self, graphing_model):
        """Test cálculo con rango personalizado."""
        x_vals, y_vals = graphing_model.calculate_points('x', x_range=(-5, 5))
        
        assert x_vals[0] == -5
        assert x_vals[-1] == 5
    
    def test_calculate_points_with_discontinuity(self, graphing_model):
        """Test cálculo con discontinuidad."""
        x_vals, y_vals = graphing_model.calculate_points('1/x')
        
        # Debe manejar división por cero con NaN
        assert len(x_vals) == 1000
        assert len(y_vals) == 1000


class TestFindRoots:
    """Tests para encontrar raíces."""
    
    def test_find_roots_linear(self, graphing_model):
        """Test encontrar raíz de función lineal."""
        roots = graphing_model.find_roots('x - 3')
        assert len(roots) == 1
        assert abs(roots[0] - 3) < 1e-10
    
    def test_find_roots_quadratic(self, graphing_model):
        """Test encontrar raíces de función cuadrática."""
        roots = graphing_model.find_roots('x**2 - 4')
        assert len(roots) == 2
        assert -2 in [round(r) for r in roots]
        assert 2 in [round(r) for r in roots]
    
    def test_find_roots_no_roots(self, graphing_model):
        """Test función sin raíces en el rango."""
        roots = graphing_model.find_roots('x**2 + 1')
        assert len(roots) == 0
    
    def test_find_roots_custom_range(self, graphing_model):
        """Test encontrar raíces en rango personalizado."""
        roots = graphing_model.find_roots('x**2 - 4', x_range=(0, 10))
        assert len(roots) == 1
        assert abs(roots[0] - 2) < 1e-10


class TestCalculateDerivative:
    """Tests para cálculo de derivadas."""
    
    def test_derivative_constant(self, graphing_model):
        """Test derivada de constante."""
        deriv = graphing_model.calculate_derivative('5')
        assert deriv == '0'
    
    def test_derivative_linear(self, graphing_model):
        """Test derivada de función lineal."""
        deriv = graphing_model.calculate_derivative('2*x')
        assert '2' in deriv
    
    def test_derivative_quadratic(self, graphing_model):
        """Test derivada de función cuadrática."""
        deriv = graphing_model.calculate_derivative('x**2')
        assert '2*x' in deriv
    
    def test_derivative_trigonometric(self, graphing_model):
        """Test derivada de función trigonométrica."""
        deriv = graphing_model.calculate_derivative('sin(x)')
        assert 'cos' in deriv


class TestEvaluateAtPoint:
    """Tests para evaluación en punto."""
    
    def test_evaluate_linear(self, graphing_model):
        """Test evaluar función lineal."""
        result = graphing_model.evaluate_at_point('2*x + 1', 3)
        assert result == 7
    
    def test_evaluate_quadratic(self, graphing_model):
        """Test evaluar función cuadrática."""
        result = graphing_model.evaluate_at_point('x**2', 4)
        assert result == 16
    
    def test_evaluate_trigonometric(self, graphing_model):
        """Test evaluar función trigonométrica."""
        result = graphing_model.evaluate_at_point('sin(x)', 0)
        assert abs(result) < 1e-10
    
    def test_evaluate_invalid_point(self, graphing_model):
        """Test evaluar en punto que causa error."""
        with pytest.raises(ValueError):
            graphing_model.evaluate_at_point('1/x', 0)


class TestFindExtrema:
    """Tests para encontrar extremos."""
    
    def test_find_extrema_quadratic(self, graphing_model):
        """Test encontrar extremos de parábola."""
        extrema = graphing_model.find_extrema('x**2')
        
        assert len(extrema['minima']) == 1
        assert len(extrema['maxima']) == 0
        assert abs(extrema['minima'][0][0]) < 1e-10  # x = 0
    
    def test_find_extrema_cubic(self, graphing_model):
        """Test encontrar extremos de cúbica."""
        extrema = graphing_model.find_extrema('x**3 - 3*x')
        
        # Debe tener un máximo y un mínimo
        assert len(extrema['maxima']) >= 1
        assert len(extrema['minima']) >= 1
    
    def test_find_extrema_no_extrema(self, graphing_model):
        """Test función sin extremos."""
        extrema = graphing_model.find_extrema('x')
        
        assert len(extrema['maxima']) == 0
        assert len(extrema['minima']) == 0


class TestCalculateLimit:
    """Tests para cálculo de límites."""
    
    def test_limit_continuous_function(self, graphing_model):
        """Test límite de función continua."""
        limits = graphing_model.calculate_limit('x**2', 2, 'both')
        
        assert limits['left'] == 4
        assert limits['right'] == 4
        assert limits['limit'] == 4
    
    def test_limit_left_only(self, graphing_model):
        """Test límite por la izquierda."""
        limits = graphing_model.calculate_limit('x', 0, 'left')
        
        assert 'left' in limits
        assert 'right' not in limits
    
    def test_limit_right_only(self, graphing_model):
        """Test límite por la derecha."""
        limits = graphing_model.calculate_limit('x', 0, 'right')
        
        assert 'right' in limits
        assert 'left' not in limits
    
    def test_limit_invalid_direction(self, graphing_model):
        """Test dirección inválida lanza error."""
        with pytest.raises(ValueError, match="direction debe ser"):
            graphing_model.calculate_limit('x', 0, 'invalid')


class TestFindIntersections:
    """Tests para encontrar intersecciones."""
    
    def test_intersections_linear_functions(self, graphing_model):
        """Test intersección de funciones lineales."""
        intersections = graphing_model.find_intersections('x', '2*x - 1')
        
        assert len(intersections) == 1
        assert abs(intersections[0][0] - 1) < 1e-10
    
    def test_intersections_quadratic_linear(self, graphing_model):
        """Test intersección cuadrática con lineal."""
        intersections = graphing_model.find_intersections('x**2', 'x')
        
        # x^2 = x tiene soluciones en x=0 y x=1
        assert len(intersections) == 2
    
    def test_intersections_no_intersections(self, graphing_model):
        """Test funciones sin intersecciones."""
        intersections = graphing_model.find_intersections('x**2 + 1', 'x**2 - 1')
        
        # Estas funciones no se intersectan
        assert len(intersections) == 0
    
    def test_intersections_custom_range(self, graphing_model):
        """Test intersecciones en rango personalizado."""
        intersections = graphing_model.find_intersections(
            'x**2',
            'x',
            x_range=(0, 10)
        )
        
        # Solo debe encontrar x=1 en el rango [0, 10]
        assert len(intersections) >= 1


class TestCalculateArea:
    """Tests para cálculo de área."""
    
    def test_area_constant_function(self, graphing_model):
        """Test área bajo función constante."""
        area = graphing_model.calculate_area_under_curve('2', 0, 5)
        
        # Área = base * altura = 5 * 2 = 10
        assert abs(area - 10) < 0.1
    
    def test_area_linear_function(self, graphing_model):
        """Test área bajo función lineal."""
        area = graphing_model.calculate_area_under_curve('x', 0, 2)
        
        # Área = (base * altura) / 2 = (2 * 2) / 2 = 2
        assert abs(area - 2) < 0.1
    
    def test_area_quadratic_function(self, graphing_model):
        """Test área bajo función cuadrática."""
        area = graphing_model.calculate_area_under_curve('x**2', 0, 1)
        
        # Integral de x^2 de 0 a 1 = 1/3
        assert abs(area - 1/3) < 0.01
    
    def test_area_invalid_range(self, graphing_model):
        """Test que rango inválido lanza error."""
        with pytest.raises(ValueError, match="x_start debe ser menor"):
            graphing_model.calculate_area_under_curve('x', 5, 0)
    
    def test_area_negative_values(self, graphing_model):
        """Test área con valores negativos."""
        area = graphing_model.calculate_area_under_curve('x', -1, 1)
        
        # Área neta debe ser cercana a 0 (simétrica)
        assert abs(area) < 0.1


class TestEdgeCases:
    """Tests para casos extremos."""
    
    def test_very_large_range(self):
        """Test con rango muy grande."""
        model = GraphingModel(x_min=-1000, x_max=1000)
        x_vals, y_vals = model.calculate_points('x')
        
        assert len(x_vals) == 1000
        assert x_vals[0] == -1000
        assert x_vals[-1] == 1000
    
    def test_very_small_range(self):
        """Test con rango muy pequeño."""
        model = GraphingModel(x_min=-0.1, x_max=0.1)
        x_vals, y_vals = model.calculate_points('x**2')
        
        assert len(x_vals) == 1000
        assert all(y >= 0 for y in y_vals if np.isfinite(y))
    
    def test_high_precision_points(self):
        """Test con muchos puntos."""
        model = GraphingModel(num_points=10000)
        x_vals, y_vals = model.calculate_points('sin(x)')
        
        assert len(x_vals) == 10000
    
    def test_function_with_asymptote(self, graphing_model):
        """Test función con asíntota."""
        x_vals, y_vals = graphing_model.calculate_points('1/x')
        
        # Debe manejar valores infinitos o muy grandes
        assert len(x_vals) == 1000
        # Verificar que hay valores finitos y algunos muy grandes cerca de x=0
        assert np.any(np.isfinite(y_vals))
        assert np.any(np.abs(y_vals[np.isfinite(y_vals)]) > 10)


class TestComplexFunctions:
    """Tests para funciones complejas."""
    
    def test_exponential_function(self, graphing_model):
        """Test función exponencial."""
        x_vals, y_vals = graphing_model.calculate_points('exp(x)')
        
        assert len(x_vals) == 1000
        assert all(y > 0 for y in y_vals if np.isfinite(y))
    
    def test_logarithmic_function(self, graphing_model):
        """Test función logarítmica."""
        x_vals, y_vals = graphing_model.calculate_points('log(x)', x_range=(0.1, 10))
        
        assert len(x_vals) == 1000
    
    def test_absolute_value(self, graphing_model):
        """Test valor absoluto."""
        x_vals, y_vals = graphing_model.calculate_points('abs(x)')
        
        assert all(y >= 0 for y in y_vals if np.isfinite(y))
    
    def test_piecewise_behavior(self, graphing_model):
        """Test comportamiento por partes."""
        # sqrt(x) solo definida para x >= 0
        x_vals, y_vals = graphing_model.calculate_points('sqrt(x)', x_range=(0, 10))
        
        assert all(y >= 0 for y in y_vals if np.isfinite(y))

# Made with Bob
