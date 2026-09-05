Actúa como un desarrollador senior experto en Python, Streamlit, Pandas y visualización de datos.
2
 
3
Necesito construir una aplicación web profesional en Streamlit para analizar un archivo Excel llamado "NO PROGRAMADOS SEPTIEMBRE 2026".
4
 
5
Objetivo:
6
Permitir a supervisores, coordinadores y gerentes consultar, filtrar y analizar el personal que tiene días no programados.
7
 
8
Tecnologías:
9
- Python 3.12
10
- Streamlit
11
- Pandas
12
- Plotly Express
13
- OpenPyXL
14
- Streamlit AgGrid (opcional)
15
 
16
La aplicación debe incluir:
17
 
18
=================================
19
1. CARGA DE ARCHIVOS
20
=================================
21
 
22
- Permitir cargar archivos .xls y .xlsx.
23
- Validar estructura.
24
- Mostrar cantidad total de registros cargados.
25
- Mostrar fecha y hora de carga.
26
 
27
=================================
28
2. LIMPIEZA DE DATOS
29
=================================
30
 
31
Normalizar:
32
- Nombres de columnas
33
- Espacios en blanco
34
- Valores nulos
35
- Mayúsculas y minúsculas
36
 
37
Convertir:
38
- Identificaciones a texto
39
- Fechas a formato datetime
40
 
41
=================================
42
3. DASHBOARD EJECUTIVO
43
=================================
44
 
45
Mostrar las siguientes métricas:
46
 
47
Total empleados no programados
48
 
49
Total regionales
50
 
51
Total clientes
52
 
53
Total cargos
54
 
55
Top regional con mayor cantidad de casos
56
 
57
Top cliente con mayor cantidad de casos
58
 
59
Utilizar tarjetas KPI.
60
 
61
=================================
62
4. FILTROS
63
=================================
64
 
65
Filtros laterales:
66
 
67
- Regional
68
- Delegación
69
- Cliente
70
- Cargo
71
- Convenio
72
- Cédula
73
- Nombre
74
 
75
Los filtros deben ser combinables.
76
 
77
=================================
78
5. TABLA INTERACTIVA
79
=================================
80
 
81
Mostrar:
82
 
83
- Regional
84
- Delegación
85
- Identificación
86
- Nombre
87
- Cargo
88
- Cliente
89
- Convenio
90
- Días no programados
91
 
92
Funcionalidades:
93
 
94
- Buscar
95
- Ordenar
96
- Filtrar
97
- Descargar Excel
98
- Descargar CSV
99
 
100
=================================
101
6. ANÁLISIS POR REGIONAL
102
=================================
103
 
104
Generar:
105
 
106
- Cantidad de empleados por regional
107
- Gráfico de barras horizontal
108
- Porcentaje de participación
109
 
110
Ordenado de mayor a menor.
111
 
112
=================================
113
7. ANÁLISIS POR CLIENTE
114
=================================
115
 
116
Mostrar:
117
 
118
Top 20 clientes con más personal no programado.
119
 
120
Visualización:
121
 
122
- Barras
123
- Treemap
124
- Tabla resumen
125
 
126
=================================
127
8. ANÁLISIS POR CARGO
128
=================================
129
 
130
Mostrar:
131
 
132
- Guarda de Seguridad
133
- Supervisor
134
- Operador de Monitoreo
135
- Escolta
136
- Otros
137
 
138
Generar:
139
 
140
- Gráfico de pastel
141
- Gráfico de barras
142
 
143
=================================
144
9. RANKING DE PERSONAL
145
=================================
146
 
147
Mostrar los empleados con mayor cantidad de días no programados.
148
 
149
Columnas:
