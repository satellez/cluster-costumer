import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

URL_DATASET = "https://raw.githubusercontent.com/gakudo-ai/open-datasets/refs/heads/main/Mall_Customers.csv"

COLORES = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]


def _etiqueta(income, score):
    if income > 65 and score > 60:
        return ("Clientes Premium",
                "Ingresos altos con alto puntaje de gasto. Segmento más valioso: compradores frecuentes y de alto valor.")
    if income > 65 and score <= 60:
        return ("Conservadores Adinerados",
                "Altos ingresos pero gasto moderado. Gran potencial de conversión con estrategias de fidelización.")
    if income <= 45 and score > 60:
        return ("Gastadores Impulsivos",
                "Ingresos bajos pero alto puntaje de gasto. Posible riesgo financiero; responden bien a promociones.")
    if income <= 45 and score <= 60:
        return ("Ahorradores Cuidadosos",
                "Ingresos y gasto bajos. Clientes cautelosos; sensibles al precio y a descuentos.")
    return ("Clientes Estándar",
            "Ingresos y comportamiento de gasto moderados. Segmento más numeroso y estable del mall.")


def ObtenerDatos():
    df = pd.read_csv(URL_DATASET)
    df.columns = df.columns.str.strip()
    return df


def LimpiarYSeleccionar():
    df = ObtenerDatos()

    reporte = {
        "filas_originales": len(df),
        "columnas": list(df.columns),
    }

    # ── Nulos ──
    nulos = df.isnull().sum()
    reporte["nulos"] = {col: int(v) for col, v in nulos.items()}
    reporte["total_nulos"] = int(nulos.sum())

    # ── Duplicados ──
    reporte["duplicados"] = int(df.duplicated().sum())

    # ── Limpieza ──
    df_clean = df.drop_duplicates().dropna().reset_index(drop=True)
    reporte["filas_limpias"] = len(df_clean)
    reporte["filas_eliminadas"] = reporte["filas_originales"] - reporte["filas_limpias"]

    # ── Outliers por IQR ──
    features = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
    outliers_info = []
    for col in features:
        Q1    = float(df_clean[col].quantile(0.25))
        Q3    = float(df_clean[col].quantile(0.75))
        IQR   = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        n_out = int(((df_clean[col] < lower) | (df_clean[col] > upper)).sum())
        outliers_info.append({
            "col":        col,
            "Q1":         round(Q1, 1),
            "Q3":         round(Q3, 1),
            "IQR":        round(IQR, 1),
            "lower":      round(lower, 1),
            "upper":      round(upper, 1),
            "n_outliers": n_out,
            "accion":     "Conservados — valores extremos válidos en contexto comercial"
                          if n_out > 0 else "Sin valores atípicos detectados",
        })
    reporte["outliers"] = outliers_info

    # ── Variables excluidas ──
    reporte["vars_excluidas"] = [
        {
            "nombre": "CustomerID",
            "tipo":   "int (identificador)",
            "razon":  "Identificador único sin valor predictivo. No aporta información sobre comportamiento ni perfil del cliente.",
        },
        {
            "nombre": "Gender",
            "tipo":   "str (categórica nominal)",
            "razon":  "Variable categórica binaria. Su codificación numérica introduciría un sesgo artificial en la distancia euclidiana que usa K-Means.",
        },
    ]

    # ── Variables seleccionadas ──
    reporte["vars_seleccionadas"] = [
        {
            "nombre":     "Age",
            "rango":      f"{int(df_clean['Age'].min())}–{int(df_clean['Age'].max())} años",
            "media":      round(float(df_clean["Age"].mean()), 1),
            "significado":"Edad del cliente",
            "razon":      "Captura diferencias generacionales en hábitos, frecuencia y tipo de compra. Clientes jóvenes y mayores tienen comportamientos distintos.",
        },
        {
            "nombre":     "Annual Income (k$)",
            "rango":      f"{int(df_clean['Annual Income (k$)'].min())}–{int(df_clean['Annual Income (k$)'].max())} k$",
            "media":      round(float(df_clean["Annual Income (k$)"].mean()), 1),
            "significado":"Ingreso anual en miles de dólares",
            "razon":      "Determina la capacidad económica real del cliente y su disposición potencial al gasto en el mall.",
        },
        {
            "nombre":     "Spending Score (1-100)",
            "rango":      f"{int(df_clean['Spending Score (1-100)'].min())}–{int(df_clean['Spending Score (1-100)'].max())}",
            "media":      round(float(df_clean["Spending Score (1-100)"].mean()), 1),
            "significado":"Puntaje de comportamiento de compra (1=bajo, 100=alto)",
            "razon":      "Refleja el comportamiento de compra observado y asignado por el mall. Es la variable más directamente relacionada con el valor del cliente.",
        },
    ]

    # ── Normalización ──
    reporte["normalizacion"] = {
        "metodo":  "StandardScaler (Z-score)",
        "formula": "z = (x − μ) / σ",
        "razon":   (
            "Las tres variables tienen escalas muy distintas: Age (18–70), "
            "Income (15–137 k$) y Score (1–100). Sin normalizar, Income dominaría "
            "la distancia euclidiana por su mayor magnitud, distorsionando los clústeres. "
            "StandardScaler transforma cada variable a media=0 y desviación estándar=1."
        ),
    }

    return df_clean, reporte


def RealizarClustering(nClusters=5):
    df, reporte_limpieza = LimpiarYSeleccionar()
    features = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
    X = df[features].values

    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    modelo = KMeans(n_clusters=nClusters, random_state=42, n_init=10)
    df["Cluster"] = modelo.fit_predict(X_scaled).astype(int)

    centroides_orig = scaler.inverse_transform(modelo.cluster_centers_)

    clusters = []
    for cid in range(nClusters):
        subset   = df[df["Cluster"] == cid]
        puntos   = subset[["Annual Income (k$)", "Spending Score (1-100)", "Age"]].rename(
            columns={"Annual Income (k$)": "x", "Spending Score (1-100)": "y", "Age": "age"}
        ).to_dict("records")
        c        = centroides_orig[cid]
        income_c = round(float(c[1]), 1)
        score_c  = round(float(c[2]), 1)
        nombre, descripcion = _etiqueta(income_c, score_c)
        clusters.append({
            "id":          cid,
            "label":       f"Cluster {cid + 1}",
            "nombre":      nombre,
            "descripcion": descripcion,
            "color":       COLORES[cid % len(COLORES)],
            "count":       len(subset),
            "puntos":      puntos,
            "centroide": {
                "age":    round(float(c[0]), 1),
                "income": income_c,
                "score":  score_c,
            },
        })

    df_t  = df.copy()
    df_t["ClusterNum"] = df_t["Cluster"] + 1
    tabla = df_t[["CustomerID", "Gender", "Age",
                  "Annual Income (k$)", "Spending Score (1-100)", "ClusterNum"]].rename(
        columns={"Annual Income (k$)": "Income",
                 "Spending Score (1-100)": "Score",
                 "ClusterNum": "Cluster"}
    ).to_dict("records")

    stats = {
        "age_mean":    round(float(df["Age"].mean()), 1),
        "age_min":     int(df["Age"].min()),
        "age_max":     int(df["Age"].max()),
        "income_mean": round(float(df["Annual Income (k$)"].mean()), 1),
        "income_min":  int(df["Annual Income (k$)"].min()),
        "income_max":  int(df["Annual Income (k$)"].max()),
        "score_mean":  round(float(df["Spending Score (1-100)"].mean()), 1),
        "score_min":   int(df["Spending Score (1-100)"].min()),
        "score_max":   int(df["Spending Score (1-100)"].max()),
        "genero_f":    int((df["Gender"] == "Female").sum()),
        "genero_m":    int((df["Gender"] == "Male").sum()),
    }

    return {
        "clusters":         clusters,
        "nClusters":        nClusters,
        "total":            len(df),
        "tabla":            tabla,
        "stats":            stats,
        "inertia":          round(float(modelo.inertia_), 2),
        "reporte_limpieza": reporte_limpieza,
    }


def MetodoDelCodo(max_k=10):
    df, _ = LimpiarYSeleccionar()
    features = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
    X = StandardScaler().fit_transform(df[features].values)
    inertias = []
    for k in range(1, max_k + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X)
        inertias.append(round(float(km.inertia_), 2))
    return {"k": list(range(1, max_k + 1)), "inertia": inertias}
