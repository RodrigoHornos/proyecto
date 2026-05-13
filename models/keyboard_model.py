"""
Modelo de atajos de teclado para la calculadora.

Este módulo gestiona los atajos de teclado, permitiendo configuración personalizada
y mapeo de teclas a acciones de la calculadora.
"""

from typing import Dict, Callable, Optional, List, Tuple
from enum import Enum


class KeyAction(Enum):
    """Acciones disponibles para atajos de teclado."""
    # Números
    NUMBER_0 = "number_0"
    NUMBER_1 = "number_1"
    NUMBER_2 = "number_2"
    NUMBER_3 = "number_3"
    NUMBER_4 = "number_4"
    NUMBER_5 = "number_5"
    NUMBER_6 = "number_6"
    NUMBER_7 = "number_7"
    NUMBER_8 = "number_8"
    NUMBER_9 = "number_9"
    
    # Operadores básicos
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    EQUALS = "equals"
    DECIMAL = "decimal"
    
    # Funciones
    CLEAR = "clear"
    DELETE = "delete"
    SIGN = "sign"
    PERCENT = "percent"
    
    # Funciones científicas
    SQRT = "sqrt"
    POWER = "power"
    LOG = "log"
    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    
    # Memoria
    MEMORY_CLEAR = "memory_clear"
    MEMORY_RECALL = "memory_recall"
    MEMORY_ADD = "memory_add"
    MEMORY_SUBTRACT = "memory_subtract"
    
    # Historial
    HISTORY_SHOW = "history_show"
    HISTORY_CLEAR = "history_clear"
    
    # Navegación
    COPY = "copy"
    PASTE = "paste"
    UNDO = "undo"
    
    # Modos
    MODE_BASIC = "mode_basic"
    MODE_SCIENTIFIC = "mode_scientific"
    MODE_PROGRAMMER = "mode_programmer"


class KeyboardModel:
    """
    Modelo que gestiona los atajos de teclado de la calculadora.
    
    Attributes:
        bindings: Diccionario de teclas a acciones
        custom_bindings: Atajos personalizados del usuario
        enabled: Si los atajos están habilitados
    """
    
    # Atajos por defecto
    DEFAULT_BINDINGS = {
        # Números
        '0': KeyAction.NUMBER_0,
        '1': KeyAction.NUMBER_1,
        '2': KeyAction.NUMBER_2,
        '3': KeyAction.NUMBER_3,
        '4': KeyAction.NUMBER_4,
        '5': KeyAction.NUMBER_5,
        '6': KeyAction.NUMBER_6,
        '7': KeyAction.NUMBER_7,
        '8': KeyAction.NUMBER_8,
        '9': KeyAction.NUMBER_9,
        
        # Operadores
        '+': KeyAction.ADD,
        '-': KeyAction.SUBTRACT,
        '*': KeyAction.MULTIPLY,
        '/': KeyAction.DIVIDE,
        '=': KeyAction.EQUALS,
        '<Return>': KeyAction.EQUALS,
        '<KP_Enter>': KeyAction.EQUALS,
        '.': KeyAction.DECIMAL,
        ',': KeyAction.DECIMAL,
        
        # Funciones básicas
        '<Escape>': KeyAction.CLEAR,
        'c': KeyAction.CLEAR,
        'C': KeyAction.CLEAR,
        '<BackSpace>': KeyAction.DELETE,
        '<Delete>': KeyAction.DELETE,
        's': KeyAction.SIGN,
        'S': KeyAction.SIGN,
        '%': KeyAction.PERCENT,
        
        # Funciones científicas
        'r': KeyAction.SQRT,
        'R': KeyAction.SQRT,
        '^': KeyAction.POWER,
        'l': KeyAction.LOG,
        'L': KeyAction.LOG,
        
        # Memoria (con Control)
        '<Control-m>': KeyAction.MEMORY_CLEAR,
        '<Control-r>': KeyAction.MEMORY_RECALL,
        '<Control-p>': KeyAction.MEMORY_ADD,
        '<Control-minus>': KeyAction.MEMORY_SUBTRACT,
        
        # Historial
        '<Control-h>': KeyAction.HISTORY_SHOW,
        '<Control-Shift-H>': KeyAction.HISTORY_CLEAR,
        
        # Navegación
        '<Control-c>': KeyAction.COPY,
        '<Control-v>': KeyAction.PASTE,
        '<Control-z>': KeyAction.UNDO,
        
        # Modos (con Alt)
        '<Alt-1>': KeyAction.MODE_BASIC,
        '<Alt-2>': KeyAction.MODE_SCIENTIFIC,
        '<Alt-3>': KeyAction.MODE_PROGRAMMER,
    }
    
    def __init__(self):
        """Inicializa el modelo de teclado con atajos por defecto."""
        self._bindings: Dict[str, KeyAction] = self.DEFAULT_BINDINGS.copy()
        self._custom_bindings: Dict[str, KeyAction] = {}
        self._enabled = True
        self._callbacks: Dict[KeyAction, List[Callable]] = {}
    
    def bind(self, key: str, action: KeyAction) -> bool:
        """
        Vincula una tecla a una acción.
        
        Args:
            key: Tecla o combinación (ej: 'a', '<Control-c>')
            action: Acción a ejecutar
            
        Returns:
            True si se vinculó correctamente
        """
        if not key or not isinstance(action, KeyAction):
            return False
        
        self._custom_bindings[key] = action
        self._bindings[key] = action
        return True
    
    def unbind(self, key: str) -> bool:
        """
        Elimina la vinculación de una tecla.
        
        Args:
            key: Tecla a desvincular
            
        Returns:
            True si se eliminó la vinculación
        """
        if key in self._custom_bindings:
            del self._custom_bindings[key]
        
        if key in self._bindings:
            # Restaurar binding por defecto si existe
            if key in self.DEFAULT_BINDINGS:
                self._bindings[key] = self.DEFAULT_BINDINGS[key]
            else:
                del self._bindings[key]
            return True
        
        return False
    
    def get_action(self, key: str) -> Optional[KeyAction]:
        """
        Obtiene la acción asociada a una tecla.
        
        Args:
            key: Tecla a consultar
            
        Returns:
            Acción asociada o None si no existe
        """
        if not self._enabled:
            return None
        
        return self._bindings.get(key)
    
    def get_key_for_action(self, action: KeyAction) -> Optional[str]:
        """
        Obtiene la primera tecla asociada a una acción.
        
        Args:
            action: Acción a buscar
            
        Returns:
            Tecla asociada o None si no existe
        """
        for key, act in self._bindings.items():
            if act == action:
                return key
        return None
    
    def get_all_keys_for_action(self, action: KeyAction) -> List[str]:
        """
        Obtiene todas las teclas asociadas a una acción.
        
        Args:
            action: Acción a buscar
            
        Returns:
            Lista de teclas asociadas
        """
        return [key for key, act in self._bindings.items() if act == action]
    
    def reset_to_defaults(self) -> None:
        """Restaura todos los atajos a los valores por defecto."""
        self._bindings = self.DEFAULT_BINDINGS.copy()
        self._custom_bindings.clear()
    
    def reset_key(self, key: str) -> bool:
        """
        Restaura una tecla específica a su valor por defecto.
        
        Args:
            key: Tecla a restaurar
            
        Returns:
            True si se restauró
        """
        if key in self._custom_bindings:
            del self._custom_bindings[key]
        
        if key in self.DEFAULT_BINDINGS:
            self._bindings[key] = self.DEFAULT_BINDINGS[key]
            return True
        elif key in self._bindings:
            del self._bindings[key]
            return True
        
        return False
    
    def enable(self) -> None:
        """Habilita los atajos de teclado."""
        self._enabled = True
    
    def disable(self) -> None:
        """Deshabilita los atajos de teclado."""
        self._enabled = False
    
    def is_enabled(self) -> bool:
        """Verifica si los atajos están habilitados."""
        return self._enabled
    
    def get_all_bindings(self) -> Dict[str, KeyAction]:
        """
        Obtiene todos los atajos actuales.
        
        Returns:
            Diccionario de teclas a acciones
        """
        return self._bindings.copy()
    
    def get_custom_bindings(self) -> Dict[str, KeyAction]:
        """
        Obtiene solo los atajos personalizados.
        
        Returns:
            Diccionario de atajos personalizados
        """
        return self._custom_bindings.copy()
    
    def has_custom_bindings(self) -> bool:
        """Verifica si hay atajos personalizados."""
        return len(self._custom_bindings) > 0
    
    def is_custom_binding(self, key: str) -> bool:
        """
        Verifica si una tecla tiene un atajo personalizado.
        
        Args:
            key: Tecla a verificar
            
        Returns:
            True si es personalizado
        """
        return key in self._custom_bindings
    
    def get_bindings_by_category(self) -> Dict[str, List[Tuple[str, KeyAction]]]:
        """
        Obtiene los atajos agrupados por categoría.
        
        Returns:
            Diccionario de categorías con sus atajos
        """
        categories = {
            'Números': [],
            'Operadores': [],
            'Funciones Básicas': [],
            'Funciones Científicas': [],
            'Memoria': [],
            'Historial': [],
            'Navegación': [],
            'Modos': []
        }
        
        for key, action in self._bindings.items():
            if action.value.startswith('number_'):
                categories['Números'].append((key, action))
            elif action in [KeyAction.ADD, KeyAction.SUBTRACT, KeyAction.MULTIPLY, 
                          KeyAction.DIVIDE, KeyAction.EQUALS, KeyAction.DECIMAL]:
                categories['Operadores'].append((key, action))
            elif action in [KeyAction.CLEAR, KeyAction.DELETE, KeyAction.SIGN, 
                          KeyAction.PERCENT]:
                categories['Funciones Básicas'].append((key, action))
            elif action in [KeyAction.SQRT, KeyAction.POWER, KeyAction.LOG,
                          KeyAction.SIN, KeyAction.COS, KeyAction.TAN]:
                categories['Funciones Científicas'].append((key, action))
            elif action.value.startswith('memory_'):
                categories['Memoria'].append((key, action))
            elif action.value.startswith('history_'):
                categories['Historial'].append((key, action))
            elif action in [KeyAction.COPY, KeyAction.PASTE, KeyAction.UNDO]:
                categories['Navegación'].append((key, action))
            elif action.value.startswith('mode_'):
                categories['Modos'].append((key, action))
        
        # Eliminar categorías vacías
        return {k: v for k, v in categories.items() if v}
    
    def register_callback(self, action: KeyAction, callback: Callable) -> None:
        """
        Registra un callback para una acción.
        
        Args:
            action: Acción a escuchar
            callback: Función a ejecutar
        """
        if action not in self._callbacks:
            self._callbacks[action] = []
        self._callbacks[action].append(callback)
    
    def unregister_callback(self, action: KeyAction, callback: Callable) -> bool:
        """
        Elimina un callback de una acción.
        
        Args:
            action: Acción
            callback: Función a eliminar
            
        Returns:
            True si se eliminó
        """
        if action in self._callbacks and callback in self._callbacks[action]:
            self._callbacks[action].remove(callback)
            return True
        return False
    
    def trigger_action(self, action: KeyAction, *args, **kwargs) -> None:
        """
        Ejecuta todos los callbacks de una acción.
        
        Args:
            action: Acción a ejecutar
            *args: Argumentos posicionales
            **kwargs: Argumentos nombrados
        """
        if action in self._callbacks:
            for callback in self._callbacks[action]:
                callback(*args, **kwargs)
    
    def to_dict(self) -> Dict[str, str]:
        """
        Exporta los atajos personalizados a diccionario.
        
        Returns:
            Diccionario con atajos personalizados
        """
        return {key: action.value for key, action in self._custom_bindings.items()}
    
    def from_dict(self, data: Dict[str, str]) -> None:
        """
        Importa atajos personalizados desde diccionario.
        
        Args:
            data: Diccionario con atajos
        """
        self._custom_bindings.clear()
        
        for key, action_value in data.items():
            try:
                action = KeyAction(action_value)
                self.bind(key, action)
            except ValueError:
                # Ignorar acciones inválidas
                pass
    
    def get_help_text(self) -> str:
        """
        Genera texto de ayuda con todos los atajos.
        
        Returns:
            String con ayuda formateada
        """
        lines = ["Atajos de Teclado:\n"]
        
        categories = self.get_bindings_by_category()
        
        for category, bindings in categories.items():
            lines.append(f"\n{category}:")
            for key, action in sorted(bindings):
                # Formatear nombre de acción
                action_name = action.value.replace('_', ' ').title()
                lines.append(f"  {key:20} → {action_name}")
        
        return "\n".join(lines)
    
    def __len__(self) -> int:
        """Número de atajos configurados."""
        return len(self._bindings)
    
    def __contains__(self, key: str) -> bool:
        """Verifica si una tecla está configurada."""
        return key in self._bindings
    
    def __str__(self) -> str:
        """Representación en string."""
        total = len(self._bindings)
        custom = len(self._custom_bindings)
        status = "habilitados" if self._enabled else "deshabilitados"
        return f"KeyboardModel: {total} atajos ({custom} personalizados), {status}"

# Made with Bob
