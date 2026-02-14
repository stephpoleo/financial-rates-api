"""Router de API para Fondos/ETFs."""

from fastapi import APIRouter, Depends, HTTPException, Query
import psycopg

from app.database import get_db
from app.schemas.fondos import FondoResponse

router = APIRouter(prefix="/fondos", tags=["Fondos/ETFs"])


@router.get("", response_model=list[FondoResponse])
def listar_fondos(
    tipo: str | None = Query(None, description="Filtrar por tipo (ETF, MUTUAL_FUND)"),
    mercado: str | None = Query(None, description="Filtrar por mercado (US, MX, GLOBAL)"),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: psycopg.Connection = Depends(get_db),
):
    """Lista todos los fondos/ETFs con filtros opcionales."""
    with db.cursor() as cur:
        query = """
            SELECT id, ticker, nombre, tipo, mercado, precio_actual,
                   rendimiento_anual, rendimiento_ytd, fecha_actualizacion
            FROM fondos_etfs
            WHERE 1=1
        """
        params = []

        if tipo:
            query += " AND tipo = %s"
            params.append(tipo)

        if mercado:
            query += " AND mercado = %s"
            params.append(mercado)

        query += " ORDER BY ticker LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cur.execute(query, params)
        rows = cur.fetchall()

    return [FondoResponse(**row) for row in rows]


@router.get("/buscar", response_model=list[FondoResponse])
def buscar_fondos(
    q: str = Query(..., min_length=1, description="Buscar por ticker o nombre"),
    limit: int = Query(10, le=50),
    db: psycopg.Connection = Depends(get_db),
):
    """Busca fondos por ticker o nombre."""
    with db.cursor() as cur:
        cur.execute("""
            SELECT id, ticker, nombre, tipo, mercado, precio_actual,
                   rendimiento_anual, rendimiento_ytd, fecha_actualizacion
            FROM fondos_etfs
            WHERE ticker ILIKE %s OR nombre ILIKE %s
            ORDER BY ticker
            LIMIT %s
        """, (f"%{q}%", f"%{q}%", limit))
        rows = cur.fetchall()

    return [FondoResponse(**row) for row in rows]


@router.get("/top", response_model=list[FondoResponse])
def top_fondos(
    limit: int = Query(10, le=50),
    db: psycopg.Connection = Depends(get_db),
):
    """Obtiene los fondos con mejor rendimiento YTD."""
    with db.cursor() as cur:
        cur.execute("""
            SELECT id, ticker, nombre, tipo, mercado, precio_actual,
                   rendimiento_anual, rendimiento_ytd, fecha_actualizacion
            FROM fondos_etfs
            WHERE rendimiento_ytd IS NOT NULL
            ORDER BY rendimiento_ytd DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()

    return [FondoResponse(**row) for row in rows]


@router.get("/{ticker}", response_model=FondoResponse)
def obtener_fondo(
    ticker: str,
    db: psycopg.Connection = Depends(get_db),
):
    """Obtiene un fondo/ETF por su ticker."""
    with db.cursor() as cur:
        cur.execute("""
            SELECT id, ticker, nombre, tipo, mercado, precio_actual,
                   rendimiento_anual, rendimiento_ytd, fecha_actualizacion
            FROM fondos_etfs
            WHERE ticker = %s
            ORDER BY fecha_actualizacion DESC
            LIMIT 1
        """, (ticker.upper(),))
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail=f"Fondo {ticker} no encontrado")

    return FondoResponse(**row)
