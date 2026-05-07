# Segmentación de Clientes con K-Means

Proyecto de aprendizaje automático no supervisado desarrollado como trabajo práctico universitario. Implementa el algoritmo **K-Means Clustering** sobre el dataset *Mall Customers* para identificar segmentos de clientes de un centro comercial, con visualización interactiva mediante una aplicación web en **Flask**.

---

## Integrantes

| Nombre | Rol |
|--------|-----|
| _(Integrante 1)_ | Modelado y clustering |
| _(Integrante 2)_ | Desarrollo web / Flask |
| _(Integrante 3)_ | Análisis y visualización |

---

## Descripción del proyecto

El objetivo principal es aplicar técnicas de **aprendizaje no supervisado** para agrupar clientes de un centro comercial según sus características demográficas y de comportamiento de compra. A partir del análisis de tres variables — edad, ingreso anual y puntaje de gasto —, el modelo K-Means identifica cinco segmentos de clientes con perfiles diferenciados, lo cual permite derivar estrategias de marketing dirigidas para cada grupo.

La aplicación web presenta de forma didáctica todo el flujo del proyecto:

- Descripción del problema y contexto
- Explicación del dataset y sus variables
- Etapa de preparación de datos (limpieza, selección, normalización)
- Fundamentos teóricos del algoritmo K-Means
- Ejecución del modelo y parámetros utilizados
- Visualizaciones interactivas de los clústeres y centroides
- Método del codo para la selección de *k*
- Interpretación de los segmentos obtenidos
- Tabla completa de resultados con búsqueda y paginación

---

## Dataset

**Mall Customers Dataset**
- **Fuente:** [GitHub – gakudo-ai/open-datasets](https://raw.githubusercontent.com/gakudo-ai/open-datasets/refs/heads/main/Mall_Customers.csv)
- **Registros:** 200 clientes
- **Variables:** CustomerID, Gender, Age, Annual Income (k$), Spending Score (1-100)
- **Variables usadas en el modelo:** Age, Annual Income (k$), Spending Score (1-100)

---

## Tecnologías utilizadas

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.12 | Lenguaje principal |
| Flask | ≥ 3.0 | Framework web |
| scikit-learn | ≥ 1.4 | Algoritmo K-Means y StandardScaler |
| pandas | ≥ 2.0 | Carga y manipulación de datos |
| Bootstrap | 5.3 | Estilos e interfaz web |
| Chart.js | 4.4 | Visualizaciones interactivas |
| python-dotenv | ≥ 1.0 | Variables de entorno |

---

## Estructura del proyecto

```
flask_app/
│
├── app.py                  # Punto de entrada de la aplicación
├── cluster.py              # Lógica de clustering (limpieza, modelo, codo)
├── config.py               # Configuración por entornos
├── requirements.txt        # Dependencias Python
│
├── routes/
│   ├── __init__.py
│   ├── main.py             # Ruta principal (renderiza el template)
│   └── api.py              # Endpoint de estado /api/status
│
├── templates/
│   └── index.html          # Template único con toda la aplicación
│
├── static/
│   ├── css/styles.css
│   └── js/main.js
│
├── .env.example            # Plantilla de variables de entorno
└── .gitignore
```

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd flask_app
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con los valores correspondientes
```

### 5. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:8000**

> **Nota:** La primera carga puede tardar unos segundos mientras se descarga el dataset y se entrena el modelo.

---

## Variables de entorno

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `SECRET_KEY` | Clave secreta de Flask | `dev-secret-key-changeme` |
| `DEBUG` | Modo depuración | `True` |

---

## Resultados obtenidos

El modelo identifica **5 segmentos** de clientes con k=5, seleccionado mediante el método del codo:

| Segmento | Perfil | Clientes |
|---|---|---|
| Clientes Premium | Ingresos altos, gasto alto | ~20% |
| Conservadores Adinerados | Ingresos altos, gasto bajo | ~20% |
| Gastadores Impulsivos | Ingresos bajos, gasto alto | ~27% |
| Ahorradores Cuidadosos | Ingresos bajos, gasto bajo | ~10% |
| Clientes Estándar | Ingresos y gasto medios | ~23% |
