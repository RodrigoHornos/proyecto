"""
Tests para el modelo de programación.
"""

import pytest
from models.programmer_model import (
    ProgrammerModel,
    NumberBase,
    BitwiseOperation
)


@pytest.fixture
def programmer_8bit():
    """Fixture con modelo de 8 bits sin signo."""
    return ProgrammerModel(bit_width=8, signed=False)


@pytest.fixture
def programmer_16bit():
    """Fixture con modelo de 16 bits sin signo."""
    return ProgrammerModel(bit_width=16, signed=False)


@pytest.fixture
def programmer_32bit():
    """Fixture con modelo de 32 bits sin signo."""
    return ProgrammerModel(bit_width=32, signed=False)


@pytest.fixture
def programmer_signed():
    """Fixture con modelo de 8 bits con signo."""
    return ProgrammerModel(bit_width=8, signed=True)


class TestProgrammerModelInit:
    """Tests para inicialización del modelo."""
    
    def test_default_initialization(self):
        """Test inicialización con valores por defecto."""
        model = ProgrammerModel()
        assert model.bit_width == 32
        assert model.signed is False
    
    def test_custom_initialization(self):
        """Test inicialización con valores personalizados."""
        model = ProgrammerModel(bit_width=16, signed=True)
        assert model.bit_width == 16
        assert model.signed is True
    
    def test_invalid_bit_width_raises_error(self):
        """Test que bit_width inválido lanza error."""
        with pytest.raises(ValueError, match="bit_width debe ser"):
            ProgrammerModel(bit_width=24)
    
    def test_valid_bit_widths(self):
        """Test todos los anchos de bit válidos."""
        for width in [8, 16, 32, 64]:
            model = ProgrammerModel(bit_width=width)
            assert model.bit_width == width
    
    def test_str_representation(self):
        """Test representación en string."""
        model = ProgrammerModel(bit_width=16, signed=False)
        result = str(model)
        assert '16-bit' in result
        assert 'unsigned' in result
    
    def test_repr_representation(self):
        """Test representación detallada."""
        model = ProgrammerModel(bit_width=8, signed=True)
        result = repr(model)
        assert 'ProgrammerModel' in result
        assert 'bit_width=8' in result
        assert 'signed=True' in result


class TestProperties:
    """Tests para propiedades del modelo."""
    
    def test_bit_width_property(self, programmer_8bit):
        """Test propiedad bit_width."""
        assert programmer_8bit.bit_width == 8
        programmer_8bit.bit_width = 16
        assert programmer_8bit.bit_width == 16
    
    def test_bit_width_invalid_value(self, programmer_8bit):
        """Test que valor inválido lanza error."""
        with pytest.raises(ValueError):
            programmer_8bit.bit_width = 12
    
    def test_signed_property(self, programmer_8bit):
        """Test propiedad signed."""
        assert programmer_8bit.signed is False
        programmer_8bit.signed = True
        assert programmer_8bit.signed is True
    
    def test_changing_bit_width_updates_limits(self):
        """Test que cambiar bit_width actualiza límites."""
        model = ProgrammerModel(bit_width=8, signed=False)
        model.bit_width = 16
        # Verificar que acepta valores mayores a 255
        result = model.bitwise_and(300, 300)
        assert result == 300
    
    def test_changing_signed_updates_limits(self):
        """Test que cambiar signed actualiza límites."""
        model = ProgrammerModel(bit_width=8, signed=False)
        model.signed = True
        # Verificar que maneja números negativos
        result = model.bitwise_not(0)
        assert result == -1


class TestBaseConversion:
    """Tests para conversión entre bases."""
    
    def test_binary_to_decimal(self, programmer_8bit):
        """Test conversión binario a decimal."""
        result = programmer_8bit.convert_base(
            '1010',
            NumberBase.BINARY,
            NumberBase.DECIMAL
        )
        assert result == '10'
    
    def test_decimal_to_binary(self, programmer_8bit):
        """Test conversión decimal a binario."""
        result = programmer_8bit.convert_base(
            '10',
            NumberBase.DECIMAL,
            NumberBase.BINARY
        )
        assert result == '00001010'
    
    def test_decimal_to_hexadecimal(self, programmer_8bit):
        """Test conversión decimal a hexadecimal."""
        result = programmer_8bit.convert_base(
            '255',
            NumberBase.DECIMAL,
            NumberBase.HEXADECIMAL
        )
        assert result == 'FF'
    
    def test_hexadecimal_to_decimal(self, programmer_8bit):
        """Test conversión hexadecimal a decimal."""
        result = programmer_8bit.convert_base(
            'FF',
            NumberBase.HEXADECIMAL,
            NumberBase.DECIMAL
        )
        assert result == '255'
    
    def test_decimal_to_octal(self, programmer_8bit):
        """Test conversión decimal a octal."""
        result = programmer_8bit.convert_base(
            '64',
            NumberBase.DECIMAL,
            NumberBase.OCTAL
        )
        assert result == '100'
    
    def test_octal_to_decimal(self, programmer_8bit):
        """Test conversión octal a decimal."""
        result = programmer_8bit.convert_base(
            '100',
            NumberBase.OCTAL,
            NumberBase.DECIMAL
        )
        assert result == '64'
    
    def test_binary_to_hexadecimal(self, programmer_8bit):
        """Test conversión binario a hexadecimal."""
        result = programmer_8bit.convert_base(
            '11111111',
            NumberBase.BINARY,
            NumberBase.HEXADECIMAL
        )
        assert result == 'FF'
    
    def test_invalid_value_raises_error(self, programmer_8bit):
        """Test que valor inválido lanza error."""
        with pytest.raises(ValueError, match="no válido"):
            programmer_8bit.convert_base(
                'XYZ',
                NumberBase.DECIMAL,
                NumberBase.BINARY
            )
    
    def test_conversion_with_overflow(self, programmer_8bit):
        """Test conversión con overflow."""
        result = programmer_8bit.convert_base(
            '256',
            NumberBase.DECIMAL,
            NumberBase.BINARY
        )
        # 256 en 8 bits = 0
        assert result == '00000000'


class TestBitwiseOperations:
    """Tests para operaciones bit a bit."""
    
    def test_bitwise_and(self, programmer_8bit):
        """Test operación AND."""
        result = programmer_8bit.bitwise_and(0b1100, 0b1010)
        assert result == 0b1000
    
    def test_bitwise_or(self, programmer_8bit):
        """Test operación OR."""
        result = programmer_8bit.bitwise_or(0b1100, 0b1010)
        assert result == 0b1110
    
    def test_bitwise_xor(self, programmer_8bit):
        """Test operación XOR."""
        result = programmer_8bit.bitwise_xor(0b1100, 0b1010)
        assert result == 0b0110
    
    def test_bitwise_not(self, programmer_8bit):
        """Test operación NOT."""
        result = programmer_8bit.bitwise_not(0b00001111)
        assert result == 0b11110000
    
    def test_bitwise_not_signed(self, programmer_signed):
        """Test operación NOT con signo."""
        result = programmer_signed.bitwise_not(0)
        assert result == -1
    
    def test_bitwise_operations_with_overflow(self, programmer_8bit):
        """Test operaciones con overflow."""
        result = programmer_8bit.bitwise_and(300, 200)
        # 300 & 0xFF = 44, 200 & 0xFF = 200
        assert result == (44 & 200)


class TestShiftOperations:
    """Tests para operaciones de desplazamiento."""
    
    def test_left_shift(self, programmer_8bit):
        """Test desplazamiento a la izquierda."""
        result = programmer_8bit.left_shift(0b00000001, 3)
        assert result == 0b00001000
    
    def test_left_shift_with_overflow(self, programmer_8bit):
        """Test left shift con overflow."""
        result = programmer_8bit.left_shift(0b10000000, 1)
        assert result == 0  # Overflow en 8 bits
    
    def test_right_shift(self, programmer_8bit):
        """Test desplazamiento a la derecha."""
        result = programmer_8bit.right_shift(0b00001000, 3)
        assert result == 0b00000001
    
    def test_right_shift_unsigned(self, programmer_8bit):
        """Test right shift sin signo."""
        result = programmer_8bit.right_shift(0b10000000, 1)
        assert result == 0b01000000
    
    def test_right_shift_signed_positive(self, programmer_signed):
        """Test right shift con signo (positivo)."""
        result = programmer_signed.right_shift(0b01000000, 1)
        assert result == 0b00100000
    
    def test_right_shift_signed_negative(self, programmer_signed):
        """Test right shift con signo (negativo)."""
        result = programmer_signed.right_shift(-128, 1)
        # -128 >> 1 = -64 (desplazamiento aritmético)
        assert result == -64
    
    def test_shift_negative_positions_raises_error(self, programmer_8bit):
        """Test que posiciones negativas lanzan error."""
        with pytest.raises(ValueError, match="deben ser >= 0"):
            programmer_8bit.left_shift(5, -1)
        
        with pytest.raises(ValueError, match="deben ser >= 0"):
            programmer_8bit.right_shift(5, -1)
    
    def test_shift_zero_positions(self, programmer_8bit):
        """Test desplazamiento de 0 posiciones."""
        assert programmer_8bit.left_shift(5, 0) == 5
        assert programmer_8bit.right_shift(5, 0) == 5


class TestRotateOperations:
    """Tests para operaciones de rotación."""
    
    def test_rotate_left(self, programmer_8bit):
        """Test rotación a la izquierda."""
        result = programmer_8bit.rotate_left(0b10000001, 1)
        assert result == 0b00000011
    
    def test_rotate_right(self, programmer_8bit):
        """Test rotación a la derecha."""
        result = programmer_8bit.rotate_right(0b10000001, 1)
        assert result == 0b11000000
    
    def test_rotate_full_cycle(self, programmer_8bit):
        """Test rotación de ciclo completo."""
        value = 0b10101010
        result = programmer_8bit.rotate_left(value, 8)
        assert result == value
    
    def test_rotate_multiple_positions(self, programmer_8bit):
        """Test rotación múltiples posiciones."""
        result = programmer_8bit.rotate_left(0b00000001, 4)
        assert result == 0b00010000


class TestBitManipulation:
    """Tests para manipulación de bits individuales."""
    
    def test_count_set_bits(self, programmer_8bit):
        """Test contar bits en 1."""
        assert programmer_8bit.count_set_bits(0b00000000) == 0
        assert programmer_8bit.count_set_bits(0b11111111) == 8
        assert programmer_8bit.count_set_bits(0b10101010) == 4
    
    def test_get_bit(self, programmer_8bit):
        """Test obtener bit específico."""
        value = 0b10101010
        assert programmer_8bit.get_bit(value, 0) == 0
        assert programmer_8bit.get_bit(value, 1) == 1
        assert programmer_8bit.get_bit(value, 7) == 1
    
    def test_get_bit_invalid_position(self, programmer_8bit):
        """Test get_bit con posición inválida."""
        with pytest.raises(ValueError, match="debe estar entre"):
            programmer_8bit.get_bit(0, -1)
        
        with pytest.raises(ValueError, match="debe estar entre"):
            programmer_8bit.get_bit(0, 8)
    
    def test_set_bit(self, programmer_8bit):
        """Test establecer bit específico."""
        value = 0b00000000
        result = programmer_8bit.set_bit(value, 3, 1)
        assert result == 0b00001000
        
        result = programmer_8bit.set_bit(result, 3, 0)
        assert result == 0b00000000
    
    def test_set_bit_invalid_position(self, programmer_8bit):
        """Test set_bit con posición inválida."""
        with pytest.raises(ValueError, match="debe estar entre"):
            programmer_8bit.set_bit(0, -1, 1)
        
        with pytest.raises(ValueError, match="debe estar entre"):
            programmer_8bit.set_bit(0, 8, 1)
    
    def test_set_bit_invalid_value(self, programmer_8bit):
        """Test set_bit con valor inválido."""
        with pytest.raises(ValueError, match="debe ser 0 o 1"):
            programmer_8bit.set_bit(0, 0, 2)
    
    def test_toggle_bit(self, programmer_8bit):
        """Test invertir bit específico."""
        value = 0b00001000
        result = programmer_8bit.toggle_bit(value, 3)
        assert result == 0b00000000
        
        result = programmer_8bit.toggle_bit(result, 3)
        assert result == 0b00001000
    
    def test_toggle_bit_invalid_position(self, programmer_8bit):
        """Test toggle_bit con posición inválida."""
        with pytest.raises(ValueError, match="debe estar entre"):
            programmer_8bit.toggle_bit(0, -1)
        
        with pytest.raises(ValueError, match="debe estar entre"):
            programmer_8bit.toggle_bit(0, 8)


class TestBinaryString:
    """Tests para conversión a string binario."""
    
    def test_to_binary_string_no_grouping(self, programmer_8bit):
        """Test conversión sin agrupación."""
        result = programmer_8bit.to_binary_string(0b10101010, group_size=0)
        assert result == '10101010'
    
    def test_to_binary_string_with_grouping(self, programmer_8bit):
        """Test conversión con agrupación."""
        result = programmer_8bit.to_binary_string(0b10101010, group_size=4)
        assert result == '1010 1010'
    
    def test_to_binary_string_16bit(self, programmer_16bit):
        """Test conversión 16 bits."""
        result = programmer_16bit.to_binary_string(0xABCD, group_size=4)
        assert result == '1010 1011 1100 1101'
    
    def test_to_binary_string_with_padding(self, programmer_8bit):
        """Test conversión con padding."""
        result = programmer_8bit.to_binary_string(0b1, group_size=0)
        assert result == '00000001'


class TestDifferentBitWidths:
    """Tests para diferentes anchos de bit."""
    
    def test_8bit_operations(self, programmer_8bit):
        """Test operaciones en 8 bits."""
        assert programmer_8bit.bitwise_not(0) == 255
        assert programmer_8bit.left_shift(128, 1) == 0
    
    def test_16bit_operations(self, programmer_16bit):
        """Test operaciones en 16 bits."""
        assert programmer_16bit.bitwise_not(0) == 65535
        assert programmer_16bit.left_shift(32768, 1) == 0
    
    def test_32bit_operations(self, programmer_32bit):
        """Test operaciones en 32 bits."""
        assert programmer_32bit.bitwise_not(0) == 4294967295
    
    def test_64bit_operations(self):
        """Test operaciones en 64 bits."""
        model = ProgrammerModel(bit_width=64, signed=False)
        assert model.bitwise_not(0) == 18446744073709551615


class TestSignedOperations:
    """Tests para operaciones con signo."""
    
    def test_signed_8bit_range(self, programmer_signed):
        """Test rango de 8 bits con signo."""
        # -128 a 127
        assert programmer_signed.bitwise_and(-128, -128) == -128
        assert programmer_signed.bitwise_and(127, 127) == 127
    
    def test_signed_not_operation(self, programmer_signed):
        """Test NOT con signo."""
        assert programmer_signed.bitwise_not(0) == -1
        assert programmer_signed.bitwise_not(-1) == 0
    
    def test_signed_overflow(self, programmer_signed):
        """Test overflow con signo."""
        result = programmer_signed.left_shift(64, 1)
        # 64 << 1 = 128, que en 8 bits con signo es -128
        assert result == -128


class TestEdgeCases:
    """Tests para casos extremos."""
    
    def test_zero_operations(self, programmer_8bit):
        """Test operaciones con cero."""
        assert programmer_8bit.bitwise_and(0, 255) == 0
        assert programmer_8bit.bitwise_or(0, 255) == 255
        assert programmer_8bit.bitwise_xor(0, 255) == 255
    
    def test_all_ones_operations(self, programmer_8bit):
        """Test operaciones con todos los bits en 1."""
        all_ones = 255
        assert programmer_8bit.bitwise_and(all_ones, all_ones) == all_ones
        assert programmer_8bit.bitwise_or(all_ones, 0) == all_ones
        assert programmer_8bit.bitwise_xor(all_ones, all_ones) == 0
    
    def test_large_shift_values(self, programmer_8bit):
        """Test desplazamientos grandes."""
        result = programmer_8bit.left_shift(1, 10)
        assert result == 0  # Overflow
    
    def test_conversion_edge_cases(self, programmer_8bit):
        """Test casos extremos de conversión."""
        # Valor máximo
        result = programmer_8bit.convert_base(
            '255',
            NumberBase.DECIMAL,
            NumberBase.BINARY
        )
        assert result == '11111111'
        
        # Valor mínimo
        result = programmer_8bit.convert_base(
            '0',
            NumberBase.DECIMAL,
            NumberBase.BINARY
        )
        assert result == '00000000'

# Made with Bob
