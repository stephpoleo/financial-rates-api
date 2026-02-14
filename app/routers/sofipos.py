"""Router de API para SOFIPOs."""

from fastapi import APIRouter, Depends, HTTPException, Query
import psycopg

from app.database import get_db
from app.schemas.sofipos import SofipoResponse

router = APIRouter(prefix="/sofipos", tags=["SOFIPOs"])


@router.get("", response_model=list[SofipoResponse])
def listar_sofipos(
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    ordenar_por: str = Query("gat_nominal", regex="^(gat_nominal|gat_real|nombre)$"),
    db: psycopg.Connection = Depends(get_db),
):
    """
    Lista todas las SOFIPOs con paginación.

    Ordenar por: gat_nominal, gat_real, nombre
    """
    with db.cursor() as cur:
        cur.execute(f"""
            SELECT id, nombre, gat_nominal, gat_real, fecha_actualizacion
            FROM sofipos
            ORDER BY {ordenar_por} DESC NULLS LAST
            LIMIT %s OFFSET %s
        """, (limit, offset))
        rows = cur.fetchall()

    return [SofipoResponse(**row) for row in rows]


@router.get("/top", response_model=list[SofipoResponse])
def top_sofipos(
    limit: int = Query(10, le=50),
    db: psycopg.Connection = Depends(get_db),
):
    """Obtiene las SOFIPOs con mejor GAT nominal."""
    with db.cursor() as cur:
        cur.execute("""
            SELECT id, nombre, gat_nominal, gat_real, fecha_actualizacion
            FROM sofipos
            WHERE gat_nominal IS NOT NULL
            ORDER BY gat_nominal DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()

    return [SofipoResponse(**row) for row in rows]


@router.get("/{sofipo_id}", response_model=SofipoResponse)
def obtener_sofipo(
    sofipo_id: int,
    db: psycopg.Connection = Depends(get_db),
):
    """Obtiene una SOFIPO por su ID."""
    with db.cursor() as cur:
        cur.execute("""
            SELECT id, nombre, gat_nominal, gat_real, fecha_actualizacion
            FROM sofipos
            WHERE id = %s
        """, (sofipo_id,))
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="SOFIPO no encontrada")

    return SofipoResponse(**row)
