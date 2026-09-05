import streamlit as st
2
import pandas as pd
3
import plotly.express as px
4
from io import BytesIO
5
 
6
# ==========================================
7
# CONFIGURACIÓN
8
# ==========================================
9
st.set_page_config(
10
page_title="No Programados",
11
page_icon="📊",
12
layout="wide"
13
)
14
 
15
st.title("📊 Dashboard Personal No Programado")
16
st.markdown("---")
17
 
18
 
19
# ==========================================
20
# FUNCIONES
21
# ==========================================
22
@st.cache_data
23
def cargar_archivo(uploaded_file):
24
if uploaded_file.name.endswith(".xlsx"):
25
df = pd.read_excel(uploaded_file, engine="openpyxl")
26
else:
27
df = pd.read_excel(uploaded_file)
28
 
29
df.columns = (
30
df.columns
31
.str.strip()
32
.str.upper()
33
.str.replace(" ", "_")
34
)
35
 
36
return df
37
 
38
 
39
def convertir_excel(df):
40
output = BytesIO()
41
 
42
with pd.ExcelWriter(
43
output,
44
engine="openpyxl"
45
) as writer:
46
df.to_excel(
47
writer,
48
index=False,
49
sheet_name="Datos"
50
)
51
 
52
output.seek(0)
53
 
54
return output
55
 
56
 
57
# ==========================================
58
# CARGA DE ARCHIVO
59
# ==========================================
60
uploaded_file = st.file_uploader(
61
"Seleccione archivo Excel",
62
type=["xls", "xlsx"]
63
)
64
 
65
if uploaded_file is None:
66
st.info("Cargue un archivo para comenzar.")
67
st.stop()
68
 
69
# ==========================================
70
# LECTURA
71
# ==========================================
72
try:
73
df = cargar_archivo(uploaded_file)
74
 
75
except Exception as e:
76
st.error(f"Error leyendo archivo: {e}")
77
st.stop()
78
 
79
st.success("Archivo cargado correctamente")
80
 
81
# ==========================================
82
# VALIDACIÓN COLUMNAS
83
# ==========================================
84
columnas_requeridas = [
85
"REGIONAL",
86
"NOMBRE",
87
"CLIENTE"
88
]
89
 
90
faltantes = [
91
c for c in columnas_requeridas
92
if c not in df.columns
93
]
94
 
95
if faltantes:
96
st.error(
97
f"Faltan columnas requeridas: {faltantes}"
98
)
99
st.stop()
100
 
101
# ==========================================
102
# NORMALIZACIÓN
103
# ==========================================
104
for col in df.select_dtypes(include="object").columns:
105
df[col] = (
106
df[col]
107
.astype(str)
108
.str.strip()
109
)
110
 
111
# ==========================================
112
# SIDEBAR FILTROS
113
# ==========================================
114
st.sidebar.header("Filtros")
115
 
116
regional = st.sidebar.multiselect(
117
"Regional",
118
sorted(df["REGIONAL"].dropna().unique())
119
)
120
 
121
if regional:
122
df = df[df["REGIONAL"].isin(regional)]
123
 
124
# Cliente
125
if "CLIENTE" in df.columns:
126
 
127
cliente = st.sidebar.multiselect(
128
"Cliente",
129
sorted(df["CLIENTE"].dropna().unique())
130
)
131
 
132
if cliente:
133
df = df[df["CLIENTE"].isin(cliente)]
134
 
135
# Cargo
136
cargo_col = None
137
 
138
for c in df.columns:
139
if "CATEGORIA" in c:
140
cargo_col = c
141
break
142
 
143
if cargo_col:
144
 
145
cargo = st.sidebar.multiselect(
146
"Cargo",
147
sorted(df[cargo_col].dropna().unique())
148
)
149
 
150
if cargo:
151
df = df[df[cargo_col].isin(cargo)]
152
 
153
# Nombre
154
nombre_busqueda = st.sidebar.text_input(
155
"Buscar empleado"
156
)
157
 
158
if nombre_busqueda:
159
 
160
df = df[
161
df["NOMBRE"]
162
.str.contains(
163
nombre_busqueda,
164
case=False,
165
na=False
166
)
167
]
168
 
169
# ==========================================
170
# KPIs
171
# ==========================================
172
total_registros = len(df)
173
 
174
total_regionales = (
175
df["REGIONAL"]
176
.nunique()
177
)
178
 
179
total_clientes = (
180
df["CLIENTE"]
181
.nunique()
182
)
183
 
184
total_cargos = (
185
df[cargo_col].nunique()
186
if cargo_col
187
else 0
188
)
189
 
190
c1, c2, c3, c4 = st.columns(4)
191
 
192
c1.metric(
193
"Empleados",
194
f"{total_registros:,}"
195
)
196
 
197
c2.metric(
198
"Regionales",
199
total_regionales
200
)
201
 
202
c3.metric(
203
"Clientes",
204
total_clientes
205
)
206
 
207
c4.metric(
208
"Cargos",
209
total_cargos
210
)
211
 
212
st.markdown("---")
213
 
214
# ==========================================
215
# TABS
216
# ==========================================
217
tab1, tab2, tab3, tab4, tab5 = st.tabs(
218
[
219
"Dashboard",
220
"Regionales",
221
"Clientes",
222
"Cargos",
223
"Datos"
224
]
225
)
226
 
227
# ==========================================
228
# DASHBOARD
229
# ==========================================
230
with tab1:
231
 
232
st.subheader("Resumen General")
233
 
234
regional_count = (
235
df["REGIONAL"]
236
.value_counts()
237
.reset_index()
238
)
239
 
240
regional_count.columns = [
241
"Regional",
242
"Cantidad"
243
]
244
 
245
fig = px.bar(
246
regional_count,
247
x="Cantidad",
248
y="Regional",
249
orientation="h",
250
title="Personal No Programado por Regional",
251
color="Cantidad"
252
)
253
 
254
st.plotly_chart(
255
fig,
256
use_container_width=True
257
)
258
 
259
# ==========================================
260
# REGIONALES
261
# ==========================================
262
with tab2:
263
 
264
st.subheader(
265
"Análisis por Regional"
266
)
267
 
268
regionales = (
269
df["REGIONAL"]
270
.value_counts()
271
.reset_index()
272
)
273
 
274
regionales.columns = [
275
"Regional",
276
"Cantidad"
277
]
278
 
279
regionales["Porcentaje"] = (
280
regionales["Cantidad"]
281
/ regionales["Cantidad"].sum()
282
* 100
283
).round(2)
284
 
285
st.dataframe(
286
regionales,
287
use_container_width=True
288
)
289
 
290
fig = px.pie(
291
regionales,
292
names="Regional",
293
values="Cantidad",
294
title="Participación Regional"
295
)
296
 
297
st.plotly_chart(
298
fig,
299
use_container_width=True
300
)
301
 
302
# ==========================================
303
# CLIENTES
304
# ==========================================
305
with tab3:
306
 
307
st.subheader(
308
"Top Clientes"
309
)
310
 
311
clientes = (
312
df["CLIENTE"]
313
.value_counts()
314
.head(20)
315
.reset_index()
316
)
317
 
318
clientes.columns = [
319
"Cliente",
320
"Cantidad"
321
]
322
 
323
st.dataframe(
324
clientes,
325
use_container_width=True
326
)
327
 
328
fig = px.bar(
329
clientes,
330
x="Cantidad",
331
y="Cliente",
332
orientation="h",
333
color="Cantidad",
334
title="Top 20 Clientes"
335
)
336
 
337
st.plotly_chart(
338
fig,
339
use_container_width=True
340
)
341
 
342
# ==========================================
343
# CARGOS
344
# ==========================================
345
with tab4:
346
 
347
st.subheader(
348
"Distribución por Cargo"
349
)
350
 
351
if cargo_col:
352
 
353
cargos = (
354
df[cargo_col]
355
.value_counts()
356
.reset_index()
357
)
358
 
359
cargos.columns = [
360
"Cargo",
361
"Cantidad"
362
]
363
 
364
col1, col2 = st.columns(2)
365
 
366
with col1:
367
 
368
fig1 = px.pie(
369
cargos,
370
names="Cargo",
371
values="Cantidad"
372
)
373
 
374
st.plotly_chart(
375
fig1,
376
use_container_width=True
377
)
378
 
379
with col2:
380
 
381
fig2 = px.bar(
382
cargos,
383
x="Cargo",
384
y="Cantidad",
385
color="Cantidad"
386
)
387
 
388
st.plotly_chart(
389
fig2,
390
use_container_width=True
391
)
392
 
393
else:
394
st.warning(
395
"No se encontró columna de cargos."
396
)
397
 
398
# ==========================================
399
# DATOS
400
# ==========================================
401
with tab5:
402
 
403
st.subheader(
404
"Detalle de Registros"
405
)
406
 
407
st.dataframe(
408
df,
409
use_container_width=True,
410
height=600
411
)
412
 
413
excel_file = convertir_excel(df)
414
 
415
st.download_button(
416
label="📥 Descargar Excel",
417
data=excel_file,
418
file_name="no_programados_filtrado.xlsx",
419
mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
420
)
421
 
422
st.download_button(
423
label="📥 Descargar CSV",
424
data=df.to_csv(index=False),
425
file_name="no_programados_filtrado.csv",
426
mime="text/csv"
427
)
428
 
429
# ==========================================
430
# INSIGHTS
431
# ==========================================
432
st.markdown("---")
433
st.subheader("🤖 Insights Automáticos")
434
 
435
top_regional = (
436
df["REGIONAL"]
437
.value_counts()
438
.idxmax()
439
)
440
 
441
top_regional_q = (
442
df["REGIONAL"]
443
.value_counts()
444
.max()
445
)
446
 
447
top_cliente = (
448
df["CLIENTE"]
449
.value_counts()
450
.idxmax()
451
)
452
 
453
top_cliente_q = (
454
df["CLIENTE"]
455
.value_counts()
456
.max()
457
)
458
 
459
st.info(
460
f"""
461
✅ Regional con más personal no programado: **{top_regional}**
462
({top_regional_q} registros)
463
 
464
✅ Cliente con más casos: **{top_cliente}**
465
({top_cliente_q} registros)
466
 
467
✅ Total personal analizado:
468
**{len(df):,} empleados**
469
"""
470
)
