"""
Modelo para exportación de historial a PDF.

Este módulo proporciona funcionalidades para exportar el historial
de cálculos a documentos PDF con formato profesional.
"""

from typing import List, Dict, Optional
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class PDFExportModel:
    """
    Modelo para exportar historial de cálculos a PDF.
    
    Attributes:
        page_size: Tamaño de página (letter o A4)
        title: Título del documento
        author: Autor del documento
        subject: Asunto del documento
    """
    
    def __init__(
        self,
        page_size: str = 'letter',
        title: str = 'Historial de Cálculos',
        author: str = 'Calculadora Científica',
        subject: str = 'Reporte de Cálculos'
    ):
        """
        Inicializa el modelo de exportación PDF.
        
        Args:
            page_size: 'letter' o 'A4'
            title: Título del documento
            author: Autor del documento
            subject: Asunto del documento
        """
        self.page_size = A4 if page_size.lower() == 'a4' else letter
        self.title = title
        self.author = author
        self.subject = subject
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self) -> None:
        """Configura estilos personalizados para el documento."""
        # Estilo para el título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para información
        self.styles.add(ParagraphStyle(
            name='InfoText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=6
        ))
        
        # Estilo para expresiones matemáticas
        self.styles.add(ParagraphStyle(
            name='MathExpression',
            parent=self.styles['Code'],
            fontSize=11,
            textColor=colors.HexColor('#2980b9'),
            fontName='Courier-Bold'
        ))
    
    def export_history(
        self,
        history_entries: List[Dict],
        filename: str,
        include_statistics: bool = True,
        include_summary: bool = True
    ) -> str:
        """
        Exporta el historial de cálculos a un archivo PDF.
        
        Args:
            history_entries: Lista de entradas del historial
            filename: Nombre del archivo PDF de salida
            include_statistics: Incluir estadísticas
            include_summary: Incluir resumen
            
        Returns:
            Ruta del archivo generado
            
        Raises:
            ValueError: Si no hay entradas para exportar
        """
        if not history_entries:
            raise ValueError("No hay entradas para exportar")
        
        # Asegurar extensión .pdf
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        # Crear documento
        doc = SimpleDocTemplate(
            filename,
            pagesize=self.page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
            title=self.title,
            author=self.author,
            subject=self.subject
        )
        
        # Construir contenido
        story = []
        
        # Título
        story.append(Paragraph(self.title, self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Información del documento
        info_text = f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        story.append(Paragraph(info_text, self.styles['InfoText']))
        story.append(Paragraph(f"Total de cálculos: {len(history_entries)}", self.styles['InfoText']))
        story.append(Spacer(1, 20))
        
        # Resumen si se solicita
        if include_summary:
            story.extend(self._create_summary(history_entries))
            story.append(Spacer(1, 20))
        
        # Tabla de historial
        story.append(Paragraph("Historial de Cálculos", self.styles['CustomHeading']))
        story.append(Spacer(1, 12))
        story.extend(self._create_history_table(history_entries))
        
        # Estadísticas si se solicitan
        if include_statistics:
            story.append(PageBreak())
            story.extend(self._create_statistics(history_entries))
        
        # Generar PDF
        doc.build(story)
        
        return filename
    
    def _create_summary(self, entries: List[Dict]) -> List:
        """
        Crea un resumen del historial.
        
        Args:
            entries: Lista de entradas del historial
            
        Returns:
            Lista de elementos para el documento
        """
        elements = []
        
        elements.append(Paragraph("Resumen", self.styles['CustomHeading']))
        
        # Contar por modo
        modes = {}
        errors = 0
        
        for entry in entries:
            mode = entry.get('mode', 'basic')
            modes[mode] = modes.get(mode, 0) + 1
            if entry.get('error'):
                errors += 1
        
        # Crear tabla de resumen
        data = [['Modo', 'Cantidad']]
        for mode, count in sorted(modes.items()):
            data.append([mode.capitalize(), str(count)])
        
        if errors > 0:
            data.append(['Errores', str(errors)])
        
        table = Table(data, colWidths=[2*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_history_table(self, entries: List[Dict]) -> List:
        """
        Crea la tabla del historial.
        
        Args:
            entries: Lista de entradas del historial
            
        Returns:
            Lista de elementos para el documento
        """
        elements = []
        
        # Encabezados
        data = [['#', 'Fecha/Hora', 'Expresión', 'Resultado', 'Modo']]
        
        # Agregar entradas
        for i, entry in enumerate(entries, 1):
            timestamp = entry.get('timestamp', '')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    timestamp = dt.strftime('%d/%m/%Y %H:%M')
                except:
                    pass
            
            expression = entry.get('expression', '')
            result = entry.get('result', '')
            mode = entry.get('mode', 'basic')
            
            # Manejar errores
            if entry.get('error'):
                result = f"Error: {entry['error']}"
            
            # Truncar expresiones largas
            if len(expression) > 40:
                expression = expression[:37] + '...'
            
            data.append([
                str(i),
                timestamp,
                expression,
                str(result),
                mode.capitalize()
            ])
        
        # Crear tabla con ancho de columnas
        col_widths = [0.5*inch, 1.5*inch, 2*inch, 1.5*inch, 1*inch]
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        # Estilo de la tabla
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Contenido
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Número
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # Fecha
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),    # Expresión
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),   # Resultado
            ('ALIGN', (4, 1), (4, -1), 'CENTER'),  # Modo
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            
            # Alternar colores de fila
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_statistics(self, entries: List[Dict]) -> List:
        """
        Crea la sección de estadísticas.
        
        Args:
            entries: Lista de entradas del historial
            
        Returns:
            Lista de elementos para el documento
        """
        elements = []
        
        elements.append(Paragraph("Estadísticas Detalladas", self.styles['CustomTitle']))
        elements.append(Spacer(1, 20))
        
        # Calcular estadísticas
        total = len(entries)
        errors = sum(1 for e in entries if e.get('error'))
        success = total - errors
        
        # Estadísticas por modo
        modes = {}
        for entry in entries:
            mode = entry.get('mode', 'basic')
            modes[mode] = modes.get(mode, 0) + 1
        
        # Tabla de estadísticas generales
        elements.append(Paragraph("Estadísticas Generales", self.styles['CustomHeading']))
        
        data = [
            ['Métrica', 'Valor'],
            ['Total de cálculos', str(total)],
            ['Cálculos exitosos', str(success)],
            ['Errores', str(errors)],
            ['Tasa de éxito', f"{(success/total*100):.1f}%" if total > 0 else "0%"]
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        # Tabla de estadísticas por modo
        elements.append(Paragraph("Uso por Modo", self.styles['CustomHeading']))
        
        data = [['Modo', 'Cantidad', 'Porcentaje']]
        for mode, count in sorted(modes.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            data.append([
                mode.capitalize(),
                str(count),
                f"{percentage:.1f}%"
            ])
        
        table = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10)
        ]))
        
        elements.append(table)
        
        return elements
    
    def export_single_calculation(
        self,
        expression: str,
        result: str,
        filename: str,
        mode: str = 'basic',
        notes: Optional[str] = None
    ) -> str:
        """
        Exporta un solo cálculo a PDF.
        
        Args:
            expression: Expresión matemática
            result: Resultado del cálculo
            filename: Nombre del archivo PDF
            mode: Modo de cálculo
            notes: Notas adicionales
            
        Returns:
            Ruta del archivo generado
        """
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=self.page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Título
        story.append(Paragraph("Cálculo Individual", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Información
        story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", self.styles['InfoText']))
        story.append(Paragraph(f"Modo: {mode.capitalize()}", self.styles['InfoText']))
        story.append(Spacer(1, 20))
        
        # Expresión y resultado
        story.append(Paragraph("Expresión:", self.styles['CustomHeading']))
        story.append(Paragraph(expression, self.styles['MathExpression']))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("Resultado:", self.styles['CustomHeading']))
        story.append(Paragraph(str(result), self.styles['MathExpression']))
        
        # Notas si existen
        if notes:
            story.append(Spacer(1, 20))
            story.append(Paragraph("Notas:", self.styles['CustomHeading']))
            story.append(Paragraph(notes, self.styles['Normal']))
        
        doc.build(story)
        
        return filename
    
    def __str__(self) -> str:
        """Representación en string del modelo."""
        return f"PDFExportModel(page_size={self.page_size}, title='{self.title}')"
    
    def __repr__(self) -> str:
        """Representación detallada del modelo."""
        return f"PDFExportModel(page_size={self.page_size!r}, title={self.title!r}, author={self.author!r})"

# Made with Bob
