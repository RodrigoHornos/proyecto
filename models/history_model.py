"""
Modelo de historial para la calculadora.

Este módulo implementa el sistema de historial que registra todas las operaciones
realizadas durante una sesión, incluyendo timestamps, expresiones, resultados y metadatos.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
import json


class HistoryEntry:
    """
    Representa una entrada individual en el historial.
    
    Attributes:
        timestamp: Momento en que se realizó la operación
        expression: Expresión matemática evaluada
        result: Resultado de la evaluación
        mode: Modo de operación utilizado (básico, científico, etc.)
        notes: Notas opcionales del usuario
        error: Mensaje de error si la operación falló
    """
    
    def __init__(
        self,
        expression: str,
        result: str,
        mode: str = "básico",
        notes: str = "",
        error: Optional[str] = None
    ):
        """
        Inicializa una entrada de historial.
        
        Args:
            expression: Expresión matemática
            result: Resultado de la evaluación
            mode: Modo de operación (default: "básico")
            notes: Notas del usuario (default: "")
            error: Mensaje de error si aplica (default: None)
        """
        self.timestamp = datetime.now()
        self.expression = expression
        self.result = result
        self.mode = mode
        self.notes = notes
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la entrada a un diccionario.
        
        Returns:
            Diccionario con todos los datos de la entrada
        """
        return {
            'timestamp': self.timestamp.isoformat(),
            'expression': self.expression,
            'result': self.result,
            'mode': self.mode,
            'notes': self.notes,
            'error': self.error
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HistoryEntry':
        """
        Crea una entrada desde un diccionario.
        
        Args:
            data: Diccionario con los datos de la entrada
            
        Returns:
            Nueva instancia de HistoryEntry
        """
        entry = cls(
            expression=data['expression'],
            result=data['result'],
            mode=data.get('mode', 'básico'),
            notes=data.get('notes', ''),
            error=data.get('error')
        )
        # Restaurar timestamp original
        entry.timestamp = datetime.fromisoformat(data['timestamp'])
        return entry
    
    def __str__(self) -> str:
        """Representación en string de la entrada."""
        time_str = self.timestamp.strftime("%H:%M:%S")
        if self.error:
            return f"[{time_str}] {self.expression} → Error: {self.error}"
        return f"[{time_str}] {self.expression} = {self.result}"
    
    def __repr__(self) -> str:
        """Representación técnica de la entrada."""
        return f"HistoryEntry(expression='{self.expression}', result='{self.result}', timestamp={self.timestamp})"


class HistoryModel:
    """
    Modelo que gestiona el historial completo de operaciones.
    
    Attributes:
        entries: Lista de entradas del historial
        session_start: Momento de inicio de la sesión
        max_entries: Número máximo de entradas a mantener (0 = ilimitado)
    """
    
    def __init__(self, max_entries: int = 0):
        """
        Inicializa el modelo de historial.
        
        Args:
            max_entries: Número máximo de entradas (0 = ilimitado)
        """
        self._entries: List[HistoryEntry] = []
        self._session_start = datetime.now()
        self._max_entries = max_entries
    
    def add_entry(
        self,
        expression: str,
        result: str,
        mode: str = "básico",
        notes: str = "",
        error: Optional[str] = None
    ) -> HistoryEntry:
        """
        Añade una nueva entrada al historial.
        
        Args:
            expression: Expresión matemática
            result: Resultado de la evaluación
            mode: Modo de operación
            notes: Notas del usuario
            error: Mensaje de error si aplica
            
        Returns:
            La entrada creada
        """
        entry = HistoryEntry(expression, result, mode, notes, error)
        self._entries.append(entry)
        
        # Limitar tamaño si es necesario
        if self._max_entries > 0 and len(self._entries) > self._max_entries:
            self._entries.pop(0)
        
        return entry
    
    def get_entries(self, limit: Optional[int] = None) -> List[HistoryEntry]:
        """
        Obtiene las entradas del historial.
        
        Args:
            limit: Número máximo de entradas a retornar (None = todas)
            
        Returns:
            Lista de entradas (más recientes primero)
        """
        entries = list(reversed(self._entries))
        if limit:
            return entries[:limit]
        return entries
    
    def get_last_entry(self) -> Optional[HistoryEntry]:
        """
        Obtiene la última entrada del historial.
        
        Returns:
            Última entrada o None si el historial está vacío
        """
        return self._entries[-1] if self._entries else None
    
    def clear(self) -> None:
        """Limpia todo el historial."""
        self._entries.clear()
        self._session_start = datetime.now()
    
    def remove_entry(self, index: int) -> bool:
        """
        Elimina una entrada específica del historial.
        
        Args:
            index: Índice de la entrada a eliminar (0 = más reciente)
            
        Returns:
            True si se eliminó, False si el índice es inválido
        """
        try:
            # Convertir índice (0 = más reciente) a índice de lista
            actual_index = len(self._entries) - 1 - index
            if 0 <= actual_index < len(self._entries):
                self._entries.pop(actual_index)
                return True
            return False
        except (IndexError, ValueError):
            return False
    
    def search(self, query: str) -> List[HistoryEntry]:
        """
        Busca entradas que contengan el texto especificado.
        
        Args:
            query: Texto a buscar (case-insensitive)
            
        Returns:
            Lista de entradas que coinciden con la búsqueda
        """
        query_lower = query.lower()
        return [
            entry for entry in self._entries
            if query_lower in entry.expression.lower() or
               query_lower in entry.result.lower() or
               query_lower in entry.notes.lower()
        ]
    
    def filter_by_mode(self, mode: str) -> List[HistoryEntry]:
        """
        Filtra entradas por modo de operación.
        
        Args:
            mode: Modo a filtrar
            
        Returns:
            Lista de entradas del modo especificado
        """
        return [entry for entry in self._entries if entry.mode == mode]
    
    def filter_by_date(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[HistoryEntry]:
        """
        Filtra entradas por rango de fechas.
        
        Args:
            start_date: Fecha de inicio (None = desde el principio)
            end_date: Fecha de fin (None = hasta ahora)
            
        Returns:
            Lista de entradas en el rango especificado
        """
        filtered = self._entries
        
        if start_date:
            filtered = [e for e in filtered if e.timestamp >= start_date]
        
        if end_date:
            filtered = [e for e in filtered if e.timestamp <= end_date]
        
        return filtered
    
    def add_note_to_entry(self, index: int, note: str) -> bool:
        """
        Añade una nota a una entrada existente.
        
        Args:
            index: Índice de la entrada (0 = más reciente)
            note: Nota a añadir
            
        Returns:
            True si se añadió la nota, False si el índice es inválido
        """
        try:
            actual_index = len(self._entries) - 1 - index
            if 0 <= actual_index < len(self._entries):
                self._entries[actual_index].notes = note
                return True
            return False
        except (IndexError, ValueError):
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del historial.
        
        Returns:
            Diccionario con estadísticas de uso
        """
        if not self._entries:
            return {
                'total_operations': 0,
                'successful_operations': 0,
                'failed_operations': 0,
                'modes_used': {},
                'session_duration': '0:00:00',
                'operations_per_mode': {}
            }
        
        # Calcular estadísticas
        total = len(self._entries)
        successful = sum(1 for e in self._entries if e.error is None)
        failed = total - successful
        
        # Contar operaciones por modo
        modes = {}
        for entry in self._entries:
            modes[entry.mode] = modes.get(entry.mode, 0) + 1
        
        # Duración de sesión
        duration = datetime.now() - self._session_start
        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{hours}:{minutes:02d}:{seconds:02d}"
        
        return {
            'total_operations': total,
            'successful_operations': successful,
            'failed_operations': failed,
            'success_rate': f"{(successful/total*100):.1f}%" if total > 0 else "0%",
            'modes_used': list(modes.keys()),
            'operations_per_mode': modes,
            'session_duration': duration_str,
            'session_start': self._session_start.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def to_json(self) -> str:
        """
        Exporta el historial a formato JSON.
        
        Returns:
            String JSON con todo el historial
        """
        data = {
            'session_start': self._session_start.isoformat(),
            'entries': [entry.to_dict() for entry in self._entries],
            'statistics': self.get_statistics()
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'HistoryModel':
        """
        Crea un modelo de historial desde JSON.
        
        Args:
            json_str: String JSON con el historial
            
        Returns:
            Nueva instancia de HistoryModel
        """
        data = json.loads(json_str)
        model = cls()
        model._session_start = datetime.fromisoformat(data['session_start'])
        model._entries = [HistoryEntry.from_dict(e) for e in data['entries']]
        return model
    
    @property
    def count(self) -> int:
        """Número total de entradas en el historial."""
        return len(self._entries)
    
    @property
    def is_empty(self) -> bool:
        """Indica si el historial está vacío."""
        return len(self._entries) == 0
    
    @property
    def session_start(self) -> datetime:
        """Momento de inicio de la sesión."""
        return self._session_start
    
    def __len__(self) -> int:
        """Número de entradas en el historial."""
        return len(self._entries)
    
    def __str__(self) -> str:
        """Representación en string del historial."""
        if not self._entries:
            return "Historial vacío"
        
        lines = [f"Historial ({len(self._entries)} entradas):"]
        for entry in reversed(self._entries[-5:]):  # Últimas 5
            lines.append(f"  {entry}")
        
        if len(self._entries) > 5:
            lines.append(f"  ... y {len(self._entries) - 5} más")
        
        return "\n".join(lines)

# Made with Bob
