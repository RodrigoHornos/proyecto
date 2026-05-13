"""
Tests para el modelo de exportación a PDF.
"""

import pytest
import os
import tempfile
from datetime import datetime
from models.export_pdf_model import PDFExportModel


class TestPDFExportModel:
    """Tests para el modelo de exportación PDF."""
    
    def test_create_pdf_export_model(self):
        """Verifica la creación del modelo."""
        model = PDFExportModel()
        assert model.title == 'Historial de Cálculos'
        assert model.author == 'Calculadora Científica'
    
    def test_create_with_custom_params(self):
        """Verifica la creación con parámetros personalizados."""
        model = PDFExportModel(
            page_size='A4',
            title='Mi Historial',
            author='Usuario',
            subject='Cálculos'
        )
        assert model.title == 'Mi Historial'
        assert model.author == 'Usuario'
        assert model.subject == 'Cálculos'
    
    def test_export_history_empty(self):
        """Verifica error con historial vacío."""
        model = PDFExportModel()
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            with pytest.raises(ValueError):
                model.export_history([], filename)
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_history_single_entry(self):
        """Verifica exportación con una entrada."""
        model = PDFExportModel()
        
        entries = [{
            'timestamp': datetime.now().isoformat(),
            'expression': '2 + 2',
            'result': '4',
            'mode': 'basic'
        }]
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_history(entries, filename)
            assert os.path.exists(result)
            assert result.endswith('.pdf')
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_history_multiple_entries(self):
        """Verifica exportación con múltiples entradas."""
        model = PDFExportModel()
        
        entries = [
            {
                'timestamp': datetime.now().isoformat(),
                'expression': '2 + 2',
                'result': '4',
                'mode': 'basic'
            },
            {
                'timestamp': datetime.now().isoformat(),
                'expression': 'sqrt(16)',
                'result': '4.0',
                'mode': 'scientific'
            },
            {
                'timestamp': datetime.now().isoformat(),
                'expression': 'sin(0)',
                'result': '0.0',
                'mode': 'scientific'
            }
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_history(entries, filename)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_history_with_errors(self):
        """Verifica exportación con entradas con errores."""
        model = PDFExportModel()
        
        entries = [
            {
                'timestamp': datetime.now().isoformat(),
                'expression': '2 + 2',
                'result': '4',
                'mode': 'basic'
            },
            {
                'timestamp': datetime.now().isoformat(),
                'expression': '1 / 0',
                'result': '',
                'mode': 'basic',
                'error': 'División por cero'
            }
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_history(entries, filename)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_history_without_statistics(self):
        """Verifica exportación sin estadísticas."""
        model = PDFExportModel()
        
        entries = [{
            'timestamp': datetime.now().isoformat(),
            'expression': '2 + 2',
            'result': '4',
            'mode': 'basic'
        }]
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_history(
                entries,
                filename,
                include_statistics=False
            )
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_history_without_summary(self):
        """Verifica exportación sin resumen."""
        model = PDFExportModel()
        
        entries = [{
            'timestamp': datetime.now().isoformat(),
            'expression': '2 + 2',
            'result': '4',
            'mode': 'basic'
        }]
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_history(
                entries,
                filename,
                include_summary=False
            )
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_history_adds_pdf_extension(self):
        """Verifica que se añade extensión .pdf si no existe."""
        model = PDFExportModel()
        
        entries = [{
            'timestamp': datetime.now().isoformat(),
            'expression': '2 + 2',
            'result': '4',
            'mode': 'basic'
        }]
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_history(entries, filename)
            assert result.endswith('.pdf')
            assert os.path.exists(result)
        finally:
            if os.path.exists(result):
                os.remove(result)
    
    def test_export_history_different_modes(self):
        """Verifica exportación con diferentes modos."""
        model = PDFExportModel()
        
        entries = [
            {'timestamp': datetime.now().isoformat(), 'expression': '2+2', 'result': '4', 'mode': 'basic'},
            {'timestamp': datetime.now().isoformat(), 'expression': 'sqrt(4)', 'result': '2', 'mode': 'extended'},
            {'timestamp': datetime.now().isoformat(), 'expression': 'sin(0)', 'result': '0', 'mode': 'scientific'},
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_history(entries, filename)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_single_calculation(self):
        """Verifica exportación de un solo cálculo."""
        model = PDFExportModel()
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_single_calculation(
                expression='2 + 2',
                result='4',
                filename=filename,
                mode='basic'
            )
            assert os.path.exists(result)
            assert result.endswith('.pdf')
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_single_calculation_with_notes(self):
        """Verifica exportación con notas."""
        model = PDFExportModel()
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_single_calculation(
                expression='sqrt(16)',
                result='4.0',
                filename=filename,
                mode='scientific',
                notes='Cálculo de raíz cuadrada'
            )
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_single_calculation_adds_extension(self):
        """Verifica que se añade extensión en cálculo individual."""
        model = PDFExportModel()
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_single_calculation(
                expression='2 + 2',
                result='4',
                filename=filename
            )
            assert result.endswith('.pdf')
            assert os.path.exists(result)
        finally:
            if os.path.exists(result):
                os.remove(result)
    
    def test_export_history_long_expressions(self):
        """Verifica manejo de expresiones largas."""
        model = PDFExportModel()
        
        long_expr = '1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + 11 + 12 + 13 + 14 + 15'
        entries = [{
            'timestamp': datetime.now().isoformat(),
            'expression': long_expr,
            'result': '120',
            'mode': 'basic'
        }]
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_history(entries, filename)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_history_many_entries(self):
        """Verifica exportación con muchas entradas."""
        model = PDFExportModel()
        
        entries = []
        for i in range(50):
            entries.append({
                'timestamp': datetime.now().isoformat(),
                'expression': f'{i} + {i}',
                'result': str(i * 2),
                'mode': 'basic'
            })
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            filename = f.name
        
        try:
            result = model.export_history(entries, filename)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_page_size_letter(self):
        """Verifica tamaño de página letter."""
        model = PDFExportModel(page_size='letter')
        assert model.page_size is not None
    
    def test_page_size_a4(self):
        """Verifica tamaño de página A4."""
        model = PDFExportModel(page_size='A4')
        assert model.page_size is not None
    
    def test_str_representation(self):
        """Verifica la representación en string."""
        model = PDFExportModel()
        s = str(model)
        assert 'PDFExportModel' in s
        assert 'Historial de Cálculos' in s
    
    def test_repr_representation(self):
        """Verifica la representación detallada."""
        model = PDFExportModel()
        r = repr(model)
        assert 'PDFExportModel' in r
        assert 'title' in r
        assert 'author' in r

# Made with Bob
