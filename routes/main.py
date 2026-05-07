from flask import Blueprint, render_template
from cluster import RealizarClustering, MetodoDelCodo
import json

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    datos = RealizarClustering(nClusters=5)
    codo  = MetodoDelCodo(max_k=10)
    return render_template(
        'index.html',
        clusters_json    = json.dumps(datos["clusters"]),
        clusters         = datos["clusters"],
        total            = datos["total"],
        nClusters        = datos["nClusters"],
        tabla            = datos["tabla"],
        stats            = datos["stats"],
        inertia          = datos["inertia"],
        codo_json        = json.dumps(codo),
        reporte          = datos["reporte_limpieza"],
    )
