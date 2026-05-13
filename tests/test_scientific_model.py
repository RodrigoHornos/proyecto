"""
Tests para el modelo de funciones científicas avanzadas.
"""

import pytest
import math
from models.scientific_model import ScientificModel


class TestScientificModel:
    """Tests para el modelo científico."""
    
    def test_create_scientific_model(self):
        """Verifica la creación del modelo."""
        model = ScientificModel()
        assert model.angle_mode == 'rad'
    
    def test_set_angle_mode(self):
        """Verifica el cambio de modo de ángulos."""
        model = ScientificModel()
        model.angle_mode = 'deg'
        assert model.angle_mode == 'deg'
        
        model.angle_mode = 'grad'
        assert model.angle_mode == 'grad'
    
    def test_set_invalid_angle_mode(self):
        """Verifica que se lance error con modo inválido."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.angle_mode = 'invalid'


class TestTrigonometricInverse:
    """Tests para funciones trigonométricas inversas."""
    
    def test_asin(self):
        """Verifica el arcoseno."""
        model = ScientificModel()
        result = model.asin(0.5)
        assert abs(result - math.pi/6) < 1e-10
    
    def test_asin_deg(self):
        """Verifica arcoseno en grados."""
        model = ScientificModel()
        model.angle_mode = 'deg'
        result = model.asin(0.5)
        assert abs(result - 30) < 1e-10
    
    def test_asin_out_of_range(self):
        """Verifica error con valor fuera de rango."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.asin(2)
    
    def test_acos(self):
        """Verifica el arcocoseno."""
        model = ScientificModel()
        result = model.acos(0.5)
        assert abs(result - math.pi/3) < 1e-10
    
    def test_acos_deg(self):
        """Verifica arcocoseno en grados."""
        model = ScientificModel()
        model.angle_mode = 'deg'
        result = model.acos(0.5)
        assert abs(result - 60) < 1e-10
    
    def test_acos_out_of_range(self):
        """Verifica error con valor fuera de rango."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.acos(1.5)
    
    def test_atan(self):
        """Verifica la arcotangente."""
        model = ScientificModel()
        result = model.atan(1)
        assert abs(result - math.pi/4) < 1e-10
    
    def test_atan_deg(self):
        """Verifica arcotangente en grados."""
        model = ScientificModel()
        model.angle_mode = 'deg'
        result = model.atan(1)
        assert abs(result - 45) < 1e-10
    
    def test_atan2(self):
        """Verifica atan2."""
        model = ScientificModel()
        result = model.atan2(1, 1)
        assert abs(result - math.pi/4) < 1e-10


class TestHyperbolic:
    """Tests para funciones hiperbólicas."""
    
    def test_sinh(self):
        """Verifica el seno hiperbólico."""
        model = ScientificModel()
        result = model.sinh(0)
        assert abs(result) < 1e-10
    
    def test_cosh(self):
        """Verifica el coseno hiperbólico."""
        model = ScientificModel()
        result = model.cosh(0)
        assert abs(result - 1) < 1e-10
    
    def test_tanh(self):
        """Verifica la tangente hiperbólica."""
        model = ScientificModel()
        result = model.tanh(0)
        assert abs(result) < 1e-10
    
    def test_asinh(self):
        """Verifica el arcoseno hiperbólico."""
        model = ScientificModel()
        result = model.asinh(0)
        assert abs(result) < 1e-10
    
    def test_acosh(self):
        """Verifica el arcocoseno hiperbólico."""
        model = ScientificModel()
        result = model.acosh(1)
        assert abs(result) < 1e-10
    
    def test_acosh_invalid(self):
        """Verifica error con valor inválido."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.acosh(0.5)
    
    def test_atanh(self):
        """Verifica la arcotangente hiperbólica."""
        model = ScientificModel()
        result = model.atanh(0)
        assert abs(result) < 1e-10
    
    def test_atanh_invalid(self):
        """Verifica error con valor inválido."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.atanh(1)
        with pytest.raises(ValueError):
            model.atanh(-1)


class TestExponentialLogarithmic:
    """Tests para funciones exponenciales y logarítmicas."""
    
    def test_exp(self):
        """Verifica la exponencial."""
        model = ScientificModel()
        result = model.exp(1)
        assert abs(result - math.e) < 1e-10
    
    def test_ln(self):
        """Verifica el logaritmo natural."""
        model = ScientificModel()
        result = model.ln(math.e)
        assert abs(result - 1) < 1e-10
    
    def test_ln_invalid(self):
        """Verifica error con valor inválido."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.ln(0)
        with pytest.raises(ValueError):
            model.ln(-1)
    
    def test_log10(self):
        """Verifica el logaritmo base 10."""
        model = ScientificModel()
        result = model.log10(100)
        assert abs(result - 2) < 1e-10
    
    def test_log10_invalid(self):
        """Verifica error con valor inválido."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.log10(-1)
    
    def test_log_custom_base(self):
        """Verifica logaritmo en base personalizada."""
        model = ScientificModel()
        result = model.log(8, 2)
        assert abs(result - 3) < 1e-10
    
    def test_log_invalid_base(self):
        """Verifica error con base inválida."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.log(10, 1)
        with pytest.raises(ValueError):
            model.log(10, -1)


class TestPowerRoots:
    """Tests para funciones de potencia y raíces."""
    
    def test_sqrt(self):
        """Verifica la raíz cuadrada."""
        model = ScientificModel()
        result = model.sqrt(16)
        assert abs(result - 4) < 1e-10
    
    def test_sqrt_invalid(self):
        """Verifica error con valor negativo."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.sqrt(-1)
    
    def test_cbrt(self):
        """Verifica la raíz cúbica."""
        model = ScientificModel()
        result = model.cbrt(27)
        assert abs(result - 3) < 1e-10
    
    def test_cbrt_negative(self):
        """Verifica raíz cúbica de número negativo."""
        model = ScientificModel()
        result = model.cbrt(-8)
        assert abs(result - (-2)) < 1e-10
    
    def test_nroot(self):
        """Verifica la raíz n-ésima."""
        model = ScientificModel()
        result = model.nroot(32, 5)
        assert abs(result - 2) < 1e-10
    
    def test_nroot_invalid(self):
        """Verifica error con raíz par de negativo."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.nroot(-4, 2)


class TestCombinatorial:
    """Tests para funciones combinatorias."""
    
    def test_factorial(self):
        """Verifica el factorial."""
        model = ScientificModel()
        assert model.factorial(0) == 1
        assert model.factorial(5) == 120
    
    def test_factorial_invalid(self):
        """Verifica error con valor inválido."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.factorial(-1)
        with pytest.raises(ValueError):
            model.factorial(3.5)
    
    def test_permutations(self):
        """Verifica las permutaciones."""
        model = ScientificModel()
        result = model.permutations(5, 3)
        assert result == 60
    
    def test_permutations_invalid(self):
        """Verifica error con valores inválidos."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.permutations(3, 5)
        with pytest.raises(ValueError):
            model.permutations(-1, 2)
    
    def test_combinations(self):
        """Verifica las combinaciones."""
        model = ScientificModel()
        result = model.combinations(5, 3)
        assert result == 10
    
    def test_combinations_invalid(self):
        """Verifica error con valores inválidos."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.combinations(3, 5)
        with pytest.raises(ValueError):
            model.combinations(-1, 2)


class TestRounding:
    """Tests para funciones de redondeo."""
    
    def test_abs(self):
        """Verifica el valor absoluto."""
        model = ScientificModel()
        assert model.abs(-5) == 5
        assert model.abs(5) == 5
    
    def test_floor(self):
        """Verifica el redondeo hacia abajo."""
        model = ScientificModel()
        assert model.floor(3.7) == 3
        assert model.floor(-3.7) == -4
    
    def test_ceil(self):
        """Verifica el redondeo hacia arriba."""
        model = ScientificModel()
        assert model.ceil(3.2) == 4
        assert model.ceil(-3.2) == -3
    
    def test_round(self):
        """Verifica el redondeo."""
        model = ScientificModel()
        assert model.round(3.14159, 2) == 3.14
        assert model.round(3.5) == 4
    
    def test_trunc(self):
        """Verifica el truncado."""
        model = ScientificModel()
        assert model.trunc(3.7) == 3
        assert model.trunc(-3.7) == -3


class TestModulo:
    """Tests para funciones de módulo."""
    
    def test_mod(self):
        """Verifica el módulo."""
        model = ScientificModel()
        assert model.mod(10, 3) == 1
        assert model.mod(10, 5) == 0
    
    def test_mod_zero_division(self):
        """Verifica error con división por cero."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.mod(10, 0)
    
    def test_gcd(self):
        """Verifica el máximo común divisor."""
        model = ScientificModel()
        assert model.gcd(12, 8) == 4
        assert model.gcd(17, 5) == 1
    
    def test_lcm(self):
        """Verifica el mínimo común múltiplo."""
        model = ScientificModel()
        assert model.lcm(12, 8) == 24
        assert model.lcm(3, 5) == 15


class TestStatistics:
    """Tests para funciones estadísticas."""
    
    def test_mean(self):
        """Verifica la media."""
        model = ScientificModel()
        result = model.mean([1, 2, 3, 4, 5])
        assert result == 3
    
    def test_mean_empty(self):
        """Verifica error con lista vacía."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.mean([])
    
    def test_median_odd(self):
        """Verifica la mediana con cantidad impar."""
        model = ScientificModel()
        result = model.median([1, 2, 3, 4, 5])
        assert result == 3
    
    def test_median_even(self):
        """Verifica la mediana con cantidad par."""
        model = ScientificModel()
        result = model.median([1, 2, 3, 4])
        assert result == 2.5
    
    def test_median_empty(self):
        """Verifica error con lista vacía."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.median([])
    
    def test_std_dev_sample(self):
        """Verifica la desviación estándar de muestra."""
        model = ScientificModel()
        result = model.std_dev([2, 4, 4, 4, 5, 5, 7, 9], sample=True)
        assert abs(result - 2.138) < 0.01
    
    def test_std_dev_population(self):
        """Verifica la desviación estándar de población."""
        model = ScientificModel()
        result = model.std_dev([2, 4, 4, 4, 5, 5, 7, 9], sample=False)
        assert abs(result - 2.0) < 0.01
    
    def test_std_dev_empty(self):
        """Verifica error con lista vacía."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.std_dev([])
    
    def test_std_dev_single_value(self):
        """Verifica error con un solo valor (muestra)."""
        model = ScientificModel()
        with pytest.raises(ValueError):
            model.std_dev([5], sample=True)


class TestAngleConversions:
    """Tests para conversiones de ángulos."""
    
    def test_deg_to_rad(self):
        """Verifica conversión de grados a radianes."""
        model = ScientificModel()
        result = model.deg_to_rad(180)
        assert abs(result - math.pi) < 1e-10
    
    def test_rad_to_deg(self):
        """Verifica conversión de radianes a grados."""
        model = ScientificModel()
        result = model.rad_to_deg(math.pi)
        assert abs(result - 180) < 1e-10
    
    def test_deg_to_grad(self):
        """Verifica conversión de grados a gradianes."""
        model = ScientificModel()
        result = model.deg_to_grad(90)
        assert abs(result - 100) < 1e-10
    
    def test_grad_to_deg(self):
        """Verifica conversión de gradianes a grados."""
        model = ScientificModel()
        result = model.grad_to_deg(100)
        assert abs(result - 90) < 1e-10
    
    def test_rad_to_grad(self):
        """Verifica conversión de radianes a gradianes."""
        model = ScientificModel()
        result = model.rad_to_grad(math.pi)
        assert abs(result - 200) < 1e-10
    
    def test_grad_to_rad(self):
        """Verifica conversión de gradianes a radianes."""
        model = ScientificModel()
        result = model.grad_to_rad(200)
        assert abs(result - math.pi) < 1e-10


class TestConstants:
    """Tests para constantes matemáticas."""
    
    def test_pi(self):
        """Verifica la constante π."""
        model = ScientificModel()
        assert abs(model.pi - math.pi) < 1e-10
    
    def test_e(self):
        """Verifica la constante e."""
        model = ScientificModel()
        assert abs(model.e - math.e) < 1e-10
    
    def test_tau(self):
        """Verifica la constante τ."""
        model = ScientificModel()
        assert abs(model.tau - 2*math.pi) < 1e-10
    
    def test_phi(self):
        """Verifica la constante φ (proporción áurea)."""
        model = ScientificModel()
        expected = (1 + math.sqrt(5)) / 2
        assert abs(model.phi - expected) < 1e-10


class TestRepresentation:
    """Tests para representaciones del modelo."""
    
    def test_str_representation(self):
        """Verifica la representación en string."""
        model = ScientificModel()
        s = str(model)
        assert "ScientificModel" in s
        assert "rad" in s
    
    def test_repr_representation(self):
        """Verifica la representación detallada."""
        model = ScientificModel()
        r = repr(model)
        assert "ScientificModel" in r
        assert "angle_mode" in r

# Made with Bob
