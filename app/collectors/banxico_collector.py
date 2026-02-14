"""
Collector para obtener tasas de CETES desde la API de Banxico SIE.

Series de CETES:
- SF43936: CETES 28 días
- SF43939: CETES 91 días
- SF43942: CETES 182 días
- SF43945: CETES 364 días
"""

from datetime import datetime, timedelta
from decimal import Decimal

import requests
from loguru import logger

from app.config import settings
from app.database import get_connection


# Series de CETES en Banxico SIE
CETES_SERIES = {
    28: "SF43936",
    91: "SF43939",
    182: "SF43942",
    364: "SF43945",
}

BASE_URL = "https://www.banxico.org.mx/SieAPIRest/service/v1/series"


class BanxicoCollector:
    """Recopilador de datos de CETES desde Banxico."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.BANXICO_API_KEY
        if not self.api_key:
            raise ValueError("BANXICO_API_KEY no configurada")

        self.headers = {
            "Bmx-Token": self.api_key,
            "Accept": "application/json",
        }

    def fetch_serie(self, serie_id: str, dias: int = 30) -> list[dict]:
        """
        Obtiene datos de una serie de Banxico.

        Args:
            serie_id: ID de la serie (ej: SF43936)
            dias: Días hacia atrás para consultar

        Returns:
            Lista de registros con fecha y valor
        """
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=dias)

        url = f"{BASE_URL}/{serie_id}/datos/{fecha_inicio:%Y-%m-%d}/{fecha_fin:%Y-%m-%d}"

        logger.debug(f"Consultando Banxico: {url}")

        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Extraer datos de la respuesta
        series = data.get("bmx", {}).get("series", [])
        if not series:
            logger.warning(f"No hay datos para serie {serie_id}")
            return []

        datos = series[0].get("datos", [])
        return datos

    def fetch_all_cetes(self, dias: int = 30) -> dict[int, list[dict]]:
        """
        Obtiene datos de todas las series de CETES.

        Returns:
            Diccionario {plazo: [datos]}
        """
        resultados = {}

        for plazo, serie_id in CETES_SERIES.items():
            try:
                datos = self.fetch_serie(serie_id, dias)
                resultados[plazo] = datos
                logger.info(f"CETES {plazo} días: {len(datos)} registros obtenidos")
            except requests.RequestException as e:
                logger.error(f"Error obteniendo CETES {plazo} días: {e}")
                resultados[plazo] = []

        return resultados

    def save_to_db(self, plazo: int, datos: list[dict]) -> int:
        """
        Guarda los datos de CETES en la base de datos.

        Args:
            plazo: Plazo en días (28, 91, 182, 364)
            datos: Lista de registros de Banxico

        Returns:
            Número de registros insertados
        """
        if not datos:
            return 0

        insertados = 0

        with get_connection() as conn:
            with conn.cursor() as cur:
                for registro in datos:
                    # Parsear fecha (formato: dd/mm/yyyy)
                    fecha_str = registro.get("fecha", "")
                    valor_str = registro.get("dato", "")

                    if not fecha_str or valor_str == "N/E":
                        continue

                    try:
                        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
                        tasa = Decimal(valor_str)
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Error parseando registro: {registro} - {e}")
                        continue

                    # Insertar con ON CONFLICT para evitar duplicados
                    try:
                        cur.execute("""
                            INSERT INTO cetes (plazo, tasa, fecha_subasta)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (plazo, fecha_subasta) DO NOTHING
                        """, (plazo, tasa, fecha))

                        if cur.rowcount > 0:
                            insertados += 1
                    except Exception as e:
                        logger.error(f"Error insertando CETES: {e}")
                        conn.rollback()
                        continue

                conn.commit()

        logger.info(f"CETES {plazo} días: {insertados} registros nuevos insertados")
        return insertados

    def collect(self, dias: int = 30) -> int:
        """
        Recopila y guarda todos los datos de CETES.

        Args:
            dias: Días hacia atrás para consultar

        Returns:
            Total de registros insertados
        """
        logger.info("Iniciando recopilación de CETES...")

        todos_los_datos = self.fetch_all_cetes(dias)
        total_insertados = 0

        for plazo, datos in todos_los_datos.items():
            insertados = self.save_to_db(plazo, datos)
            total_insertados += insertados

        logger.info(f"Recopilación de CETES completada: {total_insertados} registros nuevos")
        return total_insertados


def run_collector():
    """Ejecuta el collector de CETES."""
    try:
        collector = BanxicoCollector()
        collector.collect()
    except ValueError as e:
        logger.error(f"Error de configuración: {e}")
    except Exception as e:
        logger.exception(f"Error ejecutando collector: {e}")


if __name__ == "__main__":
    run_collector()
