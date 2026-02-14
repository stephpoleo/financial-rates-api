"""Router de API para comparación de instrumentos."""

from fastapi import APIRouter, Depends
import psycopg

from app.database import get_db

router = APIRouter(prefix="/comparar", tags=["Comparación"])


@router.get("")
def comparar_instrumentos(db: psycopg.Connection = Depends(get_db)):
    """
    Compara rendimientos actuales de CETES, SOFIPOs y ETFs.

    Retorna un resumen de los mejores instrumentos en cada categoría.
    """
    with db.cursor() as cur:
        # Obtener CETES actuales
        cur.execute("""
            SELECT DISTINCT ON (plazo) plazo, tasa, fecha_subasta
            FROM cetes
            ORDER BY plazo, fecha_subasta DESC
        """)
        cetes = cur.fetchall()

        # Obtener top 5 SOFIPOs
        cur.execute("""
            SELECT nombre, gat_nominal, gat_real
            FROM sofipos
            WHERE gat_nominal IS NOT NULL
            ORDER BY gat_nominal DESC
            LIMIT 5
        """)
        sofipos = cur.fetchall()

        # Obtener top 5 ETFs por rendimiento
        cur.execute("""
            SELECT ticker, nombre, precio_actual, rendimiento_ytd
            FROM fondos_etfs
            WHERE precio_actual IS NOT NULL
            ORDER BY rendimiento_ytd DESC NULLS LAST
            LIMIT 5
        """)
        fondos = cur.fetchall()

    # Calcular mejor opción
    mejor_cete = max(cetes, key=lambda x: float(x["tasa"])) if cetes else None
    mejor_sofipo = sofipos[0] if sofipos else None
    mejor_fondo = fondos[0] if fondos else None

    return {
        "cetes": [
            {
                "plazo": c["plazo"],
                "tasa": float(c["tasa"]),
                "fecha": str(c["fecha_subasta"]),
            }
            for c in cetes
        ],
        "sofipos_top": [
            {
                "nombre": s["nombre"],
                "gat_nominal": float(s["gat_nominal"]) if s["gat_nominal"] else None,
                "gat_real": float(s["gat_real"]) if s["gat_real"] else None,
            }
            for s in sofipos
        ],
        "fondos_top": [
            {
                "ticker": f["ticker"],
                "nombre": f["nombre"],
                "precio": float(f["precio_actual"]) if f["precio_actual"] else None,
                "rendimiento_ytd": float(f["rendimiento_ytd"]) if f["rendimiento_ytd"] else None,
            }
            for f in fondos
        ],
        "resumen": {
            "mejor_cete": {
                "plazo": mejor_cete["plazo"],
                "tasa": float(mejor_cete["tasa"]),
            } if mejor_cete else None,
            "mejor_sofipo": {
                "nombre": mejor_sofipo["nombre"],
                "gat_nominal": float(mejor_sofipo["gat_nominal"]),
            } if mejor_sofipo else None,
            "mejor_fondo": {
                "ticker": mejor_fondo["ticker"],
                "rendimiento_ytd": float(mejor_fondo["rendimiento_ytd"]) if mejor_fondo and mejor_fondo["rendimiento_ytd"] else None,
            } if mejor_fondo else None,
            "nota": "CETES y SOFIPOs son inversiones de bajo riesgo. ETFs tienen mayor riesgo pero potencialmente mayor rendimiento.",
        },
    }
