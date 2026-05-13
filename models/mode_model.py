"""
Modelo para gestión de modos de operación de la calculadora.

Este módulo define los diferentes modos de operación disponibles y gestiona
el cambio entre ellos, así como las operaciones permitidas en cada modo.
"""

from enum import Enum
from typing import List, Dict, Set, Optional, Callable


class CalculatorMode(Enum):
    """Enumeración de los modos de operación de la calculadora."""
    
    BASIC = "basic"           # Modo básico: operaciones aritméticas simples
    EXTENDED = "extended"     # Modo ampliado: incluye funciones científicas básicas
    SCIENTIFIC = "scientific" # Modo científico: funciones avanzadas
    PROGRAMMER = "programmer" # Modo programador: operaciones binarias, hex, etc.
    GRAPHING = "graphing"     # Modo gráfico: representación de funciones
    
    @classmethod
    def from_value(cls, value: str) -> 'CalculatorMode':
        """
        Crea un modo desde su valor string.
        
        Args:
            value: Valor del modo como string
            
        Returns:
            CalculatorMode correspondiente
            
        Raises:
            ValueError: Si el valor no corresponde a ningún modo
        """
        for mode in cls:
            if mode.value == value.lower():
                return mode
        raise ValueError(f"Modo inválido: {value}")


class ModeModel:
    """
    Modelo para gestionar los modos de operación de la calculadora.
    
    Attributes:
        current_mode: Modo actual de operación
        mode_history: Historial de cambios de modo
        callbacks: Callbacks registrados para cambios de modo
    """
    
    # Definición de operaciones disponibles por modo
    MODE_OPERATIONS: Dict[CalculatorMode, Set[str]] = {
        CalculatorMode.BASIC: {
            # Operaciones básicas
            '+', '-', '*', '/', '(', ')',
            # Números
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.',
            # Funciones básicas
            'C', 'CE', '±', '=', 'MC', 'MR', 'M+', 'M-', 'MS'
        },
        CalculatorMode.EXTENDED: {
            # Incluye todas las operaciones básicas
            '+', '-', '*', '/', '(', ')', '^',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.',
            'C', 'CE', '±', '=', 'MC', 'MR', 'M+', 'M-', 'MS',
            # Funciones científicas básicas
            'sqrt', 'pow', 'log', 'ln',
            'sin', 'cos', 'tan',
            'π', 'e'
        },
        CalculatorMode.SCIENTIFIC: {
            # Incluye todas las operaciones ampliadas
            '+', '-', '*', '/', '(', ')', '^',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.',
            'C', 'CE', '±', '=', 'MC', 'MR', 'M+', 'M-', 'MS',
            'sqrt', 'pow', 'log', 'ln',
            'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
            'sinh', 'cosh', 'tanh',
            'π', 'e',
            # Funciones científicas avanzadas
            'exp', 'abs', 'factorial', 'mod',
            'deg', 'rad', 'grad'
        },
        CalculatorMode.PROGRAMMER: {
            # Operaciones de programador
            '+', '-', '*', '/', '(', ')',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E', 'F',
            'C', 'CE', '=',
            # Operaciones binarias
            'AND', 'OR', 'XOR', 'NOT', 'LSHIFT', 'RSHIFT',
            # Bases
            'BIN', 'OCT', 'DEC', 'HEX'
        },
        CalculatorMode.GRAPHING: {
            # Incluye operaciones científicas
            '+', '-', '*', '/', '(', ')', '^',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.',
            'C', 'CE', '±', '=',
            'sqrt', 'pow', 'log', 'ln',
            'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
            'π', 'e', 'x', 'y',
            # Funciones de gráficos
            'PLOT', 'ZOOM', 'TRACE', 'TABLE'
        }
    }
    
    # Descripciones de cada modo
    MODE_DESCRIPTIONS: Dict[CalculatorMode, str] = {
        CalculatorMode.BASIC: "Operaciones aritméticas básicas (+, -, *, /)",
        CalculatorMode.EXTENDED: "Incluye funciones científicas básicas (sqrt, pow, log, sin, cos, tan)",
        CalculatorMode.SCIENTIFIC: "Funciones científicas avanzadas completas",
        CalculatorMode.PROGRAMMER: "Operaciones binarias, hexadecimales y lógicas",
        CalculatorMode.GRAPHING: "Representación gráfica de funciones matemáticas"
    }
    
    def __init__(self, initial_mode: CalculatorMode = CalculatorMode.BASIC):
        """
        Inicializa el modelo de modos.
        
        Args:
            initial_mode: Modo inicial de operación
        """
        self._current_mode = initial_mode
        self._mode_history: List[CalculatorMode] = [initial_mode]
        self._callbacks: Dict[str, Callable] = {}
    
    @property
    def current_mode(self) -> CalculatorMode:
        """Obtiene el modo actual."""
        return self._current_mode
    
    @current_mode.setter
    def current_mode(self, mode: CalculatorMode) -> None:
        """
        Establece el modo actual.
        
        Args:
            mode: Nuevo modo de operación
        """
        if not isinstance(mode, CalculatorMode):
            raise TypeError("El modo debe ser una instancia de CalculatorMode")
        
        old_mode = self._current_mode
        self._current_mode = mode
        self._mode_history.append(mode)
        
        # Notificar a los callbacks
        self._notify_mode_change(old_mode, mode)
    
    def set_mode(self, mode: CalculatorMode) -> None:
        """
        Establece el modo de operación.
        
        Args:
            mode: Nuevo modo de operación
        """
        self.current_mode = mode
    
    def get_mode(self) -> CalculatorMode:
        """
        Obtiene el modo actual.
        
        Returns:
            Modo actual de operación
        """
        return self._current_mode
    
    def get_available_operations(self, mode: Optional[CalculatorMode] = None) -> Set[str]:
        """
        Obtiene las operaciones disponibles para un modo.
        
        Args:
            mode: Modo del que obtener operaciones (None = modo actual)
            
        Returns:
            Conjunto de operaciones disponibles
        """
        target_mode = mode if mode is not None else self._current_mode
        return self.MODE_OPERATIONS.get(target_mode, set())
    
    def is_operation_available(self, operation: str, mode: Optional[CalculatorMode] = None) -> bool:
        """
        Verifica si una operación está disponible en un modo.
        
        Args:
            operation: Operación a verificar
            mode: Modo a verificar (None = modo actual)
            
        Returns:
            True si la operación está disponible
        """
        available_ops = self.get_available_operations(mode)
        return operation in available_ops
    
    def get_mode_description(self, mode: Optional[CalculatorMode] = None) -> str:
        """
        Obtiene la descripción de un modo.
        
        Args:
            mode: Modo del que obtener descripción (None = modo actual)
            
        Returns:
            Descripción del modo
        """
        target_mode = mode if mode is not None else self._current_mode
        return self.MODE_DESCRIPTIONS.get(target_mode, "Modo desconocido")
    
    def get_mode_history(self) -> List[CalculatorMode]:
        """
        Obtiene el historial de cambios de modo.
        
        Returns:
            Lista de modos en orden cronológico
        """
        return self._mode_history.copy()
    
    def clear_mode_history(self) -> None:
        """Limpia el historial de modos, manteniendo solo el modo actual."""
        self._mode_history = [self._current_mode]
    
    def get_previous_mode(self) -> Optional[CalculatorMode]:
        """
        Obtiene el modo anterior al actual.
        
        Returns:
            Modo anterior o None si no hay historial
        """
        if len(self._mode_history) < 2:
            return None
        return self._mode_history[-2]
    
    def switch_to_previous_mode(self) -> bool:
        """
        Cambia al modo anterior.
        
        Returns:
            True si se pudo cambiar, False si no hay modo anterior
        """
        previous = self.get_previous_mode()
        if previous is None:
            return False
        
        self.current_mode = previous
        return True
    
    def register_callback(self, name: str, callback: Callable) -> None:
        """
        Registra un callback para cambios de modo.
        
        Args:
            name: Nombre identificador del callback
            callback: Función a llamar cuando cambie el modo
                     Debe aceptar (old_mode, new_mode)
        """
        self._callbacks[name] = callback
    
    def unregister_callback(self, name: str) -> bool:
        """
        Elimina un callback registrado.
        
        Args:
            name: Nombre del callback a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        if name in self._callbacks:
            del self._callbacks[name]
            return True
        return False
    
    def _notify_mode_change(self, old_mode: CalculatorMode, new_mode: CalculatorMode) -> None:
        """
        Notifica a los callbacks sobre un cambio de modo.
        
        Args:
            old_mode: Modo anterior
            new_mode: Modo nuevo
        """
        for callback in self._callbacks.values():
            try:
                callback(old_mode, new_mode)
            except Exception:
                # Ignorar errores en callbacks para no interrumpir el flujo
                pass
    
    def get_all_modes(self) -> List[CalculatorMode]:
        """
        Obtiene todos los modos disponibles.
        
        Returns:
            Lista de todos los modos
        """
        return list(CalculatorMode)
    
    def to_dict(self) -> Dict:
        """
        Convierte el modelo a diccionario.
        
        Returns:
            Diccionario con los datos del modelo
        """
        return {
            'current_mode': self._current_mode.value,
            'mode_history': [mode.value for mode in self._mode_history]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ModeModel':
        """
        Crea un modelo desde un diccionario.
        
        Args:
            data: Diccionario con los datos
            
        Returns:
            Nueva instancia de ModeModel
        """
        current_mode = CalculatorMode.from_value(data.get('current_mode', 'basic'))
        model = cls(current_mode)
        
        # Restaurar historial
        history = data.get('mode_history', [])
        model._mode_history = [CalculatorMode.from_value(m) for m in history]
        
        return model
    
    def __str__(self) -> str:
        """Representación en string del modelo."""
        return f"ModeModel(current={self._current_mode.value}, history_length={len(self._mode_history)})"
    
    def __repr__(self) -> str:
        """Representación detallada del modelo."""
        return f"ModeModel(current_mode={self._current_mode!r}, mode_history={self._mode_history!r})"

# Made with Bob
