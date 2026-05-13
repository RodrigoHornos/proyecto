#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de Memoria
Gestiona el sistema de memoria de la calculadora
"""


class MemoryModel:
    """
    Modelo que encapsula la lógica del sistema de memoria
    Responsable de:
    - Almacenar valores en memoria
    - Recuperar valores de memoria
    - Operaciones de suma y resta en memoria
    - Limpiar memoria
    """
    
    def __init__(self):
        """Inicializa el modelo de memoria"""
        self._memory = 0
    
    @property
    def value(self):
        """Obtiene el valor actual de la memoria"""
        return self._memory
    
    def add(self, value):
        """
        Suma un valor a la memoria
        
        Args:
            value: Valor numérico a sumar
        
        Returns:
            float: Nuevo valor de la memoria
        """
        self._memory += float(value)
        return self._memory
    
    def subtract(self, value):
        """
        Resta un valor de la memoria
        
        Args:
            value: Valor numérico a restar
        
        Returns:
            float: Nuevo valor de la memoria
        """
        self._memory -= float(value)
        return self._memory
    
    def recall(self):
        """
        Recupera el valor almacenado en memoria
        
        Returns:
            float: Valor actual de la memoria
        """
        return self._memory
    
    def clear(self):
        """
        Limpia la memoria (establece a 0)
        
        Returns:
            float: Nuevo valor de la memoria (0)
        """
        self._memory = 0
        return self._memory
    
    def store(self, value):
        """
        Almacena un valor directamente en memoria (reemplaza el valor actual)
        
        Args:
            value: Valor numérico a almacenar
        
        Returns:
            float: Nuevo valor de la memoria
        """
        self._memory = float(value)
        return self._memory

# Made with Bob
