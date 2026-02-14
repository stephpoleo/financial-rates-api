"""Router de API para CETES."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
import psycopg

from app.database import get_db
from app.schemas.cetes import CetesResponse

router = APIRouter(prefix="/cetes", tags=["CETES"])


@router.get("", response_model=list[CetesResponse])
def listar_cetes(
    plazo: int | None = Query(None, description="Filtrar por plazo (28, 91, 182, 364)"),
    db: psycopg.Connection = Depends(get_db),
):
    """
    Lista las tasas de CETES más recientes.

    Si se especifica plazo, filtra por ese plazo.
    """
    with db.cursor() as cur:
        if plazo:
            cur.execute("""
                SELECT id, plazo, tasa, fecha_subasta, fecha_vencimiento
                FROM cetes
                WHERE plazo = %s
                ORDER BY fecha_subasta DESC
                LIMIT 10
            """, (plazo,))
        else:
            # Obtener la última tasa de cada plazo
            cur.execute("""
                SELECT DISTINCT ON (plazo) id, plazo, tasa, fecha_subasta, fecha_vencimiento
                FROM cetes
                ORDER BY plazo, fecha_subasta DESC
            """)

        rows = cur.fetchall()

    return [CetesResponse(**row) for row in rows]


@router.get("/actuales", response_model=list[CetesResponse])
def tasas_actuales(db: psycopg.Connection = Depends(get_db)):
    """Obtiene las tasas más recientes de cada plazo."""
    with db.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT ON (plazo) id, plazo, tasa, fecha_subasta, fecha_vencimiento
            FROM cetes
            ORDER BY plazo, fecha_subasta DESC
        """)
        rows = cur.fetchall()

    return [CetesResponse(**row) for row in rows]


@router.get("/historico", response_model=list[CetesResponse])
def historico_cetes(
    plazo: int = Query(..., description="Plazo (28, 91, 182, 364)"),
    fecha_inicio: date | None = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: date | None = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    limit: int = Query(50, le=200),
    db: psycopg.Connection = Depends(get_db),
):
    """Obtiene el histórico de tasas para un plazo específico."""
    with db.cursor() as cur:
        query = """
            SELECT id, plazo, tasa, fecha_subasta, fecha_vencimiento
            FROM cetes
            WHERE plazo = %s
        """
        params = [plazo]

        if fecha_inicio:
            query += " AND fecha_subasta >= %s"
            params.append(fecha_inicio)

        if fecha_fin:
            query += " AND fecha_subasta <= %s"
            params.append(fecha_fin)

        query += " ORDER BY fecha_subasta DESC LIMIT %s"
        params.append(limit)

        cur.execute(query, params)
        rows = cur.fetchall()

    return [CetesResponse(**row) for row in rows]


@router.get("/{plazo}", response_model=CetesResponse)
def obtener_cete_por_plazo(
    plazo: int,
    db: psycopg.Connection = Depends(get_db),
):
    """Obtiene la tasa más reciente para un plazo específico."""
    if plazo not in [28, 91, 182, 364]:
        raise HTTPException(status_code=400, detail="Plazo debe ser 28, 91, 182 o 364")

    with db.cursor() as cur:
        cur.execute("""
            SELECT id, plazo, tasa, fecha_subasta, fecha_vencimiento
            FROM cetes
            WHERE plazo = %s
            ORDER BY fecha_subasta DESC
            LIMIT 1
        """, (plazo,))
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail=f"No hay datos para CETES {plazo} días")

    return CetesResponse(**row)
