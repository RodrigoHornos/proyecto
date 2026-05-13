"""
Tests para el modelo de historial (HistoryModel y HistoryEntry).

Verifica el correcto funcionamiento del sistema de historial incluyendo:
- Creación y gestión de entradas
- Búsqueda y filtrado
- Estadísticas
- Exportación/importación JSON
"""

import pytest
from datetime import datetime, timedelta
import json
from models.history_model import HistoryModel, HistoryEntry


class TestHistoryEntry:
    """Tests para la clase HistoryEntry."""
    
    def test_create_entry(self):
        """Test: crear una entrada básica."""
        entry = HistoryEntry("2+2", "4")
        
        assert entry.expression == "2+2"
        assert entry.result == "4"
        assert entry.mode == "básico"
        assert entry.notes == ""
        assert entry.error is None
        assert isinstance(entry.timestamp, datetime)
    
    def test_create_entry_with_mode(self):
        """Test: crear entrada con modo específico."""
        entry = HistoryEntry("sin(30)", "0.5", mode="científico")
        
        assert entry.mode == "científico"
    
    def test_create_entry_with_notes(self):
        """Test: crear entrada con notas."""
        entry = HistoryEntry("10*5", "50", notes="Cálculo importante")
        
        assert entry.notes == "Cálculo importante"
    
    def test_create_entry_with_error(self):
        """Test: crear entrada con error."""
        entry = HistoryEntry("1/0", "", error="División por cero")
        
        assert entry.error == "División por cero"
        assert entry.result == ""
    
    def test_to_dict(self):
        """Test: convertir entrada a diccionario."""
        entry = HistoryEntry("3*3", "9", mode="básico", notes="Test")
        data = entry.to_dict()
        
        assert data['expression'] == "3*3"
        assert data['result'] == "9"
        assert data['mode'] == "básico"
        assert data['notes'] == "Test"
        assert data['error'] is None
        assert 'timestamp' in data
    
    def test_from_dict(self):
        """Test: crear entrada desde diccionario."""
        data = {
            'timestamp': datetime.now().isoformat(),
            'expression': '5+5',
            'result': '10',
            'mode': 'básico',
            'notes': 'Nota',
            'error': None
        }
        
        entry = HistoryEntry.from_dict(data)
        
        assert entry.expression == '5+5'
        assert entry.result == '10'
        assert entry.mode == 'básico'
        assert entry.notes == 'Nota'
    
    def test_str_representation(self):
        """Test: representación en string."""
        entry = HistoryEntry("7+3", "10")
        str_repr = str(entry)
        
        assert "7+3" in str_repr
        assert "10" in str_repr
        assert "=" in str_repr
    
    def test_str_representation_with_error(self):
        """Test: representación en string con error."""
        entry = HistoryEntry("1/0", "", error="División por cero")
        str_repr = str(entry)
        
        assert "1/0" in str_repr
        assert "Error" in str_repr
        assert "División por cero" in str_repr


class TestHistoryModel:
    """Tests para la clase HistoryModel."""
    
    def test_create_history(self):
        """Test: crear historial vacío."""
        history = HistoryModel()
        
        assert history.count == 0
        assert history.is_empty
        assert isinstance(history.session_start, datetime)
    
    def test_add_entry(self):
        """Test: añadir entrada al historial."""
        history = HistoryModel()
        entry = history.add_entry("2+2", "4")
        
        assert history.count == 1
        assert not history.is_empty
        assert isinstance(entry, HistoryEntry)
        assert entry.expression == "2+2"
    
    def test_add_multiple_entries(self):
        """Test: añadir múltiples entradas."""
        history = HistoryModel()
        
        history.add_entry("1+1", "2")
        history.add_entry("2+2", "4")
        history.add_entry("3+3", "6")
        
        assert history.count == 3
    
    def test_get_entries(self):
        """Test: obtener todas las entradas."""
        history = HistoryModel()
        
        history.add_entry("1+1", "2")
        history.add_entry("2+2", "4")
        history.add_entry("3+3", "6")
        
        entries = history.get_entries()
        
        assert len(entries) == 3
        # Más reciente primero
        assert entries[0].expression == "3+3"
        assert entries[1].expression == "2+2"
        assert entries[2].expression == "1+1"
    
    def test_get_entries_with_limit(self):
        """Test: obtener entradas con límite."""
        history = HistoryModel()
        
        for i in range(10):
            history.add_entry(f"{i}+{i}", str(i*2))
        
        entries = history.get_entries(limit=5)
        
        assert len(entries) == 5
    
    def test_get_last_entry(self):
        """Test: obtener última entrada."""
        history = HistoryModel()
        
        history.add_entry("1+1", "2")
        history.add_entry("2+2", "4")
        
        last = history.get_last_entry()
        
        assert last is not None
        assert last.expression == "2+2"
    
    def test_get_last_entry_empty(self):
        """Test: obtener última entrada de historial vacío."""
        history = HistoryModel()
        
        assert history.get_last_entry() is None
    
    def test_clear_history(self):
        """Test: limpiar historial."""
        history = HistoryModel()
        
        history.add_entry("1+1", "2")
        history.add_entry("2+2", "4")
        
        assert history.count == 2
        
        history.clear()
        
        assert history.count == 0
        assert history.is_empty
    
    def test_remove_entry(self):
        """Test: eliminar entrada específica."""
        history = HistoryModel()
        
        history.add_entry("1+1", "2")
        history.add_entry("2+2", "4")
        history.add_entry("3+3", "6")
        
        # Eliminar la más reciente (índice 0)
        success = history.remove_entry(0)
        
        assert success
        assert history.count == 2
        assert history.get_last_entry().expression == "2+2"
    
    def test_remove_entry_invalid_index(self):
        """Test: eliminar entrada con índice inválido."""
        history = HistoryModel()
        history.add_entry("1+1", "2")
        
        success = history.remove_entry(10)
        
        assert not success
        assert history.count == 1
    
    def test_search(self):
        """Test: buscar en el historial."""
        history = HistoryModel()
        
        history.add_entry("sin(30)", "0.5", mode="científico")
        history.add_entry("2+2", "4", mode="básico")
        history.add_entry("cos(60)", "0.5", mode="científico")
        
        results = history.search("sin")
        
        assert len(results) == 1
        assert results[0].expression == "sin(30)"
    
    def test_search_case_insensitive(self):
        """Test: búsqueda case-insensitive."""
        history = HistoryModel()
        
        history.add_entry("SIN(30)", "0.5")
        
        results = history.search("sin")
        
        assert len(results) == 1
    
    def test_search_in_notes(self):
        """Test: buscar en notas."""
        history = HistoryModel()
        
        history.add_entry("2+2", "4", notes="Importante")
        history.add_entry("3+3", "6", notes="Normal")
        
        results = history.search("importante")
        
        assert len(results) == 1
        assert results[0].notes == "Importante"
    
    def test_filter_by_mode(self):
        """Test: filtrar por modo."""
        history = HistoryModel()
        
        history.add_entry("2+2", "4", mode="básico")
        history.add_entry("sin(30)", "0.5", mode="científico")
        history.add_entry("3+3", "6", mode="básico")
        
        basic_entries = history.filter_by_mode("básico")
        
        assert len(basic_entries) == 2
        assert all(e.mode == "básico" for e in basic_entries)
    
    def test_filter_by_date(self):
        """Test: filtrar por rango de fechas."""
        history = HistoryModel()
        
        # Añadir entradas
        history.add_entry("1+1", "2")
        history.add_entry("2+2", "4")
        
        # Filtrar desde hace 1 minuto
        start = datetime.now() - timedelta(minutes=1)
        entries = history.filter_by_date(start_date=start)
        
        assert len(entries) == 2
    
    def test_add_note_to_entry(self):
        """Test: añadir nota a entrada existente."""
        history = HistoryModel()
        
        history.add_entry("2+2", "4")
        history.add_entry("3+3", "6")
        
        # Añadir nota a la más reciente
        success = history.add_note_to_entry(0, "Nota importante")
        
        assert success
        assert history.get_last_entry().notes == "Nota importante"
    
    def test_add_note_invalid_index(self):
        """Test: añadir nota con índice inválido."""
        history = HistoryModel()
        history.add_entry("2+2", "4")
        
        success = history.add_note_to_entry(10, "Nota")
        
        assert not success
    
    def test_get_statistics_empty(self):
        """Test: estadísticas de historial vacío."""
        history = HistoryModel()
        stats = history.get_statistics()
        
        assert stats['total_operations'] == 0
        assert stats['successful_operations'] == 0
        assert stats['failed_operations'] == 0
    
    def test_get_statistics(self):
        """Test: estadísticas del historial."""
        history = HistoryModel()
        
        history.add_entry("2+2", "4", mode="básico")
        history.add_entry("3+3", "6", mode="básico")
        history.add_entry("1/0", "", mode="básico", error="División por cero")
        history.add_entry("sin(30)", "0.5", mode="científico")
        
        stats = history.get_statistics()
        
        assert stats['total_operations'] == 4
        assert stats['successful_operations'] == 3
        assert stats['failed_operations'] == 1
        assert stats['success_rate'] == "75.0%"
        assert 'básico' in stats['modes_used']
        assert 'científico' in stats['modes_used']
        assert stats['operations_per_mode']['básico'] == 3
        assert stats['operations_per_mode']['científico'] == 1
    
    def test_to_json(self):
        """Test: exportar a JSON."""
        history = HistoryModel()
        
        history.add_entry("2+2", "4", mode="básico")
        history.add_entry("3+3", "6", mode="científico")
        
        json_str = history.to_json()
        
        assert isinstance(json_str, str)
        data = json.loads(json_str)
        
        assert 'session_start' in data
        assert 'entries' in data
        assert 'statistics' in data
        assert len(data['entries']) == 2
    
    def test_from_json(self):
        """Test: importar desde JSON."""
        history1 = HistoryModel()
        history1.add_entry("2+2", "4", mode="básico")
        history1.add_entry("3+3", "6", mode="científico")
        
        json_str = history1.to_json()
        
        history2 = HistoryModel.from_json(json_str)
        
        assert history2.count == 2
        assert history2.get_entries()[0].expression == "3+3"
        assert history2.get_entries()[1].expression == "2+2"
    
    def test_max_entries_limit(self):
        """Test: límite máximo de entradas."""
        history = HistoryModel(max_entries=3)
        
        history.add_entry("1+1", "2")
        history.add_entry("2+2", "4")
        history.add_entry("3+3", "6")
        history.add_entry("4+4", "8")  # Debe eliminar la primera
        
        assert history.count == 3
        entries = history.get_entries()
        # La primera entrada (1+1) debe haber sido eliminada
        assert entries[-1].expression != "1+1"
        assert entries[0].expression == "4+4"
    
    def test_len_method(self):
        """Test: método __len__."""
        history = HistoryModel()
        
        assert len(history) == 0
        
        history.add_entry("2+2", "4")
        history.add_entry("3+3", "6")
        
        assert len(history) == 2
    
    def test_str_representation(self):
        """Test: representación en string del historial."""
        history = HistoryModel()
        
        # Historial vacío
        assert "vacío" in str(history).lower()
        
        # Con entradas
        history.add_entry("2+2", "4")
        str_repr = str(history)
        
        assert "2+2" in str_repr
        assert "4" in str_repr
    
    def test_entry_with_all_parameters(self):
        """Test: entrada con todos los parámetros."""
        history = HistoryModel()
        
        entry = history.add_entry(
            expression="sin(45)",
            result="0.707",
            mode="científico",
            notes="Ángulo de 45 grados",
            error=None
        )
        
        assert entry.expression == "sin(45)"
        assert entry.result == "0.707"
        assert entry.mode == "científico"
        assert entry.notes == "Ángulo de 45 grados"
        assert entry.error is None
    
    def test_session_start_property(self):
        """Test: propiedad session_start."""
        history = HistoryModel()
        
        start = history.session_start
        assert isinstance(start, datetime)
        
        # Añadir entradas no debe cambiar session_start
        history.add_entry("2+2", "4")
        assert history.session_start == start
        
        # Clear debe actualizar session_start
        history.clear()
        assert history.session_start > start


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

# Made with Bob
