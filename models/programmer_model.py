"""
Modelo para operaciones de programación.

Este módulo proporciona funcionalidades para operaciones binarias,
hexadecimales, octales y manipulación de bits.
"""

from typing import Union, Tuple, Optional
from enum import Enum


class NumberBase(Enum):
    """Bases numéricas soportadas."""
    BINARY = 2
    OCTAL = 8
    DECIMAL = 10
    HEXADECIMAL = 16


class BitwiseOperation(Enum):
    """Operaciones bit a bit."""
    AND = 'and'
    OR = 'or'
    XOR = 'xor'
    NOT = 'not'
    LEFT_SHIFT = 'lshift'
    RIGHT_SHIFT = 'rshift'


class ProgrammerModel:
    """
    Modelo para operaciones de programación.
    
    Attributes:
        bit_width: Ancho de bits (8, 16, 32, 64)
        signed: Si los números son con signo
    """
    
    def __init__(self, bit_width: int = 32, signed: bool = False):
        """
        Inicializa el modelo de programación.
        
        Args:
            bit_width: Ancho de bits (8, 16, 32, 64)
            signed: Si los números son con signo
            
        Raises:
            ValueError: Si bit_width no es válido
        """
        if bit_width not in [8, 16, 32, 64]:
            raise ValueError("bit_width debe ser 8, 16, 32 o 64")
        
        self._bit_width = bit_width
        self._signed = signed
        self._max_value = self._calculate_max_value()
        self._min_value = self._calculate_min_value()
    
    @property
    def bit_width(self) -> int:
        """Obtiene el ancho de bits."""
        return self._bit_width
    
    @bit_width.setter
    def bit_width(self, value: int) -> None:
        """
        Establece el ancho de bits.
        
        Args:
            value: Nuevo ancho de bits
            
        Raises:
            ValueError: Si el valor no es válido
        """
        if value not in [8, 16, 32, 64]:
            raise ValueError("bit_width debe ser 8, 16, 32 o 64")
        self._bit_width = value
        self._max_value = self._calculate_max_value()
        self._min_value = self._calculate_min_value()
    
    @property
    def signed(self) -> bool:
        """Obtiene si los números son con signo."""
        return self._signed
    
    @signed.setter
    def signed(self, value: bool) -> None:
        """
        Establece si los números son con signo.
        
        Args:
            value: True para con signo, False para sin signo
        """
        self._signed = value
        self._max_value = self._calculate_max_value()
        self._min_value = self._calculate_min_value()
    
    def _calculate_max_value(self) -> int:
        """Calcula el valor máximo según bit_width y signed."""
        if self._signed:
            return (2 ** (self._bit_width - 1)) - 1
        return (2 ** self._bit_width) - 1
    
    def _calculate_min_value(self) -> int:
        """Calcula el valor mínimo según bit_width y signed."""
        if self._signed:
            return -(2 ** (self._bit_width - 1))
        return 0
    
    def _validate_value(self, value: int) -> None:
        """
        Valida que un valor esté en el rango permitido.
        
        Args:
            value: Valor a validar
            
        Raises:
            ValueError: Si el valor está fuera de rango
        """
        if value < self._min_value or value > self._max_value:
            raise ValueError(
                f"Valor {value} fuera de rango [{self._min_value}, {self._max_value}]"
            )
    
    def _mask_value(self, value: int) -> int:
        """
        Aplica máscara al valor según bit_width.
        
        Args:
            value: Valor a enmascarar
            
        Returns:
            Valor enmascarado
        """
        mask = (1 << self._bit_width) - 1
        result = value & mask
        
        # Manejar signo si es necesario
        if self._signed and (result & (1 << (self._bit_width - 1))):
            result -= (1 << self._bit_width)
        
        return result
    
    def convert_base(
        self,
        value: str,
        from_base: NumberBase,
        to_base: NumberBase
    ) -> str:
        """
        Convierte un número entre bases.
        
        Args:
            value: Valor a convertir (como string)
            from_base: Base origen
            to_base: Base destino
            
        Returns:
            Valor convertido como string
            
        Raises:
            ValueError: Si el valor no es válido
        """
        # Convertir a decimal
        try:
            decimal_value = int(value, from_base.value)
        except ValueError:
            raise ValueError(f"Valor '{value}' no válido para base {from_base.value}")
        
        # Aplicar máscara
        decimal_value = self._mask_value(decimal_value)
        
        # Convertir a base destino
        if to_base == NumberBase.BINARY:
            result = bin(decimal_value & ((1 << self._bit_width) - 1))[2:]
            return result.zfill(self._bit_width)
        elif to_base == NumberBase.OCTAL:
            return oct(decimal_value & ((1 << self._bit_width) - 1))[2:]
        elif to_base == NumberBase.DECIMAL:
            return str(decimal_value)
        elif to_base == NumberBase.HEXADECIMAL:
            return hex(decimal_value & ((1 << self._bit_width) - 1))[2:].upper()
        
        raise ValueError(f"Base {to_base} no soportada")
    
    def bitwise_and(self, a: int, b: int) -> int:
        """
        Operación AND bit a bit.
        
        Args:
            a: Primer operando
            b: Segundo operando
            
        Returns:
            Resultado de a AND b
        """
        return self._mask_value(a & b)
    
    def bitwise_or(self, a: int, b: int) -> int:
        """
        Operación OR bit a bit.
        
        Args:
            a: Primer operando
            b: Segundo operando
            
        Returns:
            Resultado de a OR b
        """
        return self._mask_value(a | b)
    
    def bitwise_xor(self, a: int, b: int) -> int:
        """
        Operación XOR bit a bit.
        
        Args:
            a: Primer operando
            b: Segundo operando
            
        Returns:
            Resultado de a XOR b
        """
        return self._mask_value(a ^ b)
    
    def bitwise_not(self, a: int) -> int:
        """
        Operación NOT bit a bit.
        
        Args:
            a: Operando
            
        Returns:
            Resultado de NOT a
        """
        return self._mask_value(~a)
    
    def left_shift(self, value: int, positions: int) -> int:
        """
        Desplazamiento a la izquierda.
        
        Args:
            value: Valor a desplazar
            positions: Número de posiciones
            
        Returns:
            Valor desplazado
            
        Raises:
            ValueError: Si positions es negativo
        """
        if positions < 0:
            raise ValueError("Las posiciones deben ser >= 0")
        
        return self._mask_value(value << positions)
    
    def right_shift(self, value: int, positions: int) -> int:
        """
        Desplazamiento a la derecha.
        
        Args:
            value: Valor a desplazar
            positions: Número de posiciones
            
        Returns:
            Valor desplazado
            
        Raises:
            ValueError: Si positions es negativo
        """
        if positions < 0:
            raise ValueError("Las posiciones deben ser >= 0")
        
        # Para números sin signo, desplazamiento lógico
        if not self._signed:
            return self._mask_value(value >> positions)
        
        # Para números con signo, desplazamiento aritmético
        if value < 0:
            # Convertir a representación sin signo
            unsigned = value & ((1 << self._bit_width) - 1)
            result = unsigned >> positions
            # Rellenar con 1s desde la izquierda
            if positions < self._bit_width:
                fill_mask = ((1 << positions) - 1) << (self._bit_width - positions)
                result |= fill_mask
            return self._mask_value(result)
        
        return self._mask_value(value >> positions)
    
    def rotate_left(self, value: int, positions: int) -> int:
        """
        Rotación a la izquierda.
        
        Args:
            value: Valor a rotar
            positions: Número de posiciones
            
        Returns:
            Valor rotado
        """
        positions = positions % self._bit_width
        value = value & ((1 << self._bit_width) - 1)
        
        left_part = (value << positions) & ((1 << self._bit_width) - 1)
        right_part = value >> (self._bit_width - positions)
        
        return self._mask_value(left_part | right_part)
    
    def rotate_right(self, value: int, positions: int) -> int:
        """
        Rotación a la derecha.
        
        Args:
            value: Valor a rotar
            positions: Número de posiciones
            
        Returns:
            Valor rotado
        """
        positions = positions % self._bit_width
        value = value & ((1 << self._bit_width) - 1)
        
        right_part = value >> positions
        left_part = (value << (self._bit_width - positions)) & ((1 << self._bit_width) - 1)
        
        return self._mask_value(right_part | left_part)
    
    def count_set_bits(self, value: int) -> int:
        """
        Cuenta los bits en 1.
        
        Args:
            value: Valor a analizar
            
        Returns:
            Número de bits en 1
        """
        value = value & ((1 << self._bit_width) - 1)
        count = 0
        while value:
            count += value & 1
            value >>= 1
        return count
    
    def get_bit(self, value: int, position: int) -> int:
        """
        Obtiene el valor de un bit específico.
        
        Args:
            value: Valor a analizar
            position: Posición del bit (0 = LSB)
            
        Returns:
            0 o 1
            
        Raises:
            ValueError: Si position está fuera de rango
        """
        if position < 0 or position >= self._bit_width:
            raise ValueError(f"Posición debe estar entre 0 y {self._bit_width - 1}")
        
        value = value & ((1 << self._bit_width) - 1)
        return (value >> position) & 1
    
    def set_bit(self, value: int, position: int, bit_value: int) -> int:
        """
        Establece el valor de un bit específico.
        
        Args:
            value: Valor original
            position: Posición del bit (0 = LSB)
            bit_value: Nuevo valor del bit (0 o 1)
            
        Returns:
            Valor modificado
            
        Raises:
            ValueError: Si position o bit_value no son válidos
        """
        if position < 0 or position >= self._bit_width:
            raise ValueError(f"Posición debe estar entre 0 y {self._bit_width - 1}")
        
        if bit_value not in [0, 1]:
            raise ValueError("bit_value debe ser 0 o 1")
        
        value = value & ((1 << self._bit_width) - 1)
        
        if bit_value == 1:
            value |= (1 << position)
        else:
            value &= ~(1 << position)
        
        return self._mask_value(value)
    
    def toggle_bit(self, value: int, position: int) -> int:
        """
        Invierte el valor de un bit específico.
        
        Args:
            value: Valor original
            position: Posición del bit (0 = LSB)
            
        Returns:
            Valor modificado
            
        Raises:
            ValueError: Si position está fuera de rango
        """
        if position < 0 or position >= self._bit_width:
            raise ValueError(f"Posición debe estar entre 0 y {self._bit_width - 1}")
        
        value = value & ((1 << self._bit_width) - 1)
        value ^= (1 << position)
        
        return self._mask_value(value)
    
    def to_binary_string(self, value: int, group_size: int = 4) -> str:
        """
        Convierte un valor a string binario con agrupación.
        
        Args:
            value: Valor a convertir
            group_size: Tamaño de grupos (0 = sin agrupar)
            
        Returns:
            String binario agrupado
        """
        value = value & ((1 << self._bit_width) - 1)
        binary = bin(value)[2:].zfill(self._bit_width)
        
        if group_size <= 0:
            return binary
        
        # Agrupar desde la derecha
        groups = []
        for i in range(0, len(binary), group_size):
            groups.append(binary[i:i+group_size])
        
        return ' '.join(groups)
    
    def __str__(self) -> str:
        """Representación en string del modelo."""
        sign_str = "signed" if self._signed else "unsigned"
        return f"ProgrammerModel({self._bit_width}-bit {sign_str})"
    
    def __repr__(self) -> str:
        """Representación detallada del modelo."""
        return f"ProgrammerModel(bit_width={self._bit_width}, signed={self._signed})"

# Made with Bob
