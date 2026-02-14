"""
Collector para obtener datos de ETFs y fondos usando Alpha Vantage.

Límite gratuito: 25 requests/día
"""

import time
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import json

import requests
from loguru import logger

from app.config import settings
from app.database import get_connection


# Límites de API
MAX_DAILY_CALLS = 25
CALLS_FILE = Path(__file__).parent / ".api_calls.json"

# Lista de ETFs a monitorear (limitada a 20 para dejar margen)
ETFS_LIST = [
    # ETFs de Estados Unidos - Índices principales
    {"ticker": "SPY", "nombre": "SPDR S&P 500 ETF", "tipo": "ETF", "mercado": "US"},
    {"ticker": "QQQ", "nombre": "Invesco QQQ Trust (Nasdaq 100)", "tipo": "ETF", "mercado": "US"},
    {"ticker": "VOO", "nombre": "Vanguard S&P 500 ETF", "tipo": "ETF", "mercado": "US"},
    {"ticker": "VTI", "nombre": "Vanguard Total Stock Market ETF", "tipo": "ETF", "mercado": "US"},
    {"ticker": "IWM", "nombre": "iShares Russell 2000 ETF", "tipo": "ETF", "mercado": "US"},

    # ETFs de Bonos
    {"ticker": "BND", "nombre": "Vanguard Total Bond Market ETF", "tipo": "ETF", "mercado": "US"},
    {"ticker": "TLT", "nombre": "iShares 20+ Year Treasury Bond ETF", "tipo": "ETF", "mercado": "US"},

    # ETFs Internacionales
    {"ticker": "VEA", "nombre": "Vanguard FTSE Developed Markets ETF", "tipo": "ETF", "mercado": "GLOBAL"},
    {"ticker": "VWO", "nombre": "Vanguard FTSE Emerging Markets ETF", "tipo": "ETF", "mercado": "GLOBAL"},
    {"ticker": "EWW", "nombre": "iShares MSCI Mexico ETF", "tipo": "ETF", "mercado": "MX"},

    # ETFs de Sectores
    {"ticker": "XLK", "nombre": "Technology Select Sector SPDR", "tipo": "ETF", "mercado": "US"},
    {"ticker": "XLF", "nombre": "Financial Select Sector SPDR", "tipo": "ETF", "mercado": "US"},
    {"ticker": "XLE", "nombre": "Energy Select Sector SPDR", "tipo": "ETF", "mercado": "US"},

    # ETFs de Oro y Commodities
    {"ticker": "GLD", "nombre": "SPDR Gold Shares", "tipo": "ETF", "mercado": "US"},
    {"ticker": "SLV", "nombre": "iShares Silver Trust", "tipo": "ETF", "mercado": "US"},

    # Otros populares
    {"ticker": "ARKK", "nombre": "ARK Innovation ETF", "tipo": "ETF", "mercado": "US"},
    {"ticker": "VNQ", "nombre": "Vanguard Real Estate ETF", "tipo": "ETF", "mercado": "US"},
    {"ticker": "SCHD", "nombre": "Schwab US Dividend Equity ETF", "tipo": "ETF", "mercado": "US"},
]

BASE_URL = "https://www.alphavantage.co/query"


class APILimitExceeded(Exception):
    """Excepción cuando se excede el límite de llamadas."""
    pass


class ETFCollector:
    """Recopilador de datos de ETFs desde Alpha Vantage."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.ALPHA_VANTAGE_API_KEY
        if not self.api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY no configurada")

        self.calls_today = self._load_calls_count()

    def _load_calls_count(self) -> int:
        """Carga el contador de llamadas del día."""
        try:
            if CALLS_FILE.exists():
                data = json.loads(CALLS_FILE.read_text())
                if data.get("date") == str(date.today()):
                    return data.get("calls", 0)
        except Exception:
            pass
        return 0

    def _save_calls_count(self):
        """Guarda el contador de llamadas."""
        try:
            data = {"date": str(date.today()), "calls": self.calls_today}
            CALLS_FILE.write_text(json.dumps(data))
        except Exception as e:
            logger.warning(f"Error guardando contador de llamadas: {e}")

    def _check_limit(self):
        """Verifica si se puede hacer otra llamada."""
        if self.calls_today >= MAX_DAILY_CALLS:
            raise APILimitExceeded(
                f"Límite de {MAX_DAILY_CALLS} llamadas diarias alcanzado. "
                f"Reintenta mañana."
            )

    def _increment_calls(self):
        """Incrementa el contador de llamadas."""
        self.calls_today += 1
        self._save_calls_count()

    def get_remaining_calls(self) -> int:
        """Retorna llamadas restantes hoy."""
        return max(0, MAX_DAILY_CALLS - self.calls_today)

    def fetch_etf_data(self, ticker: str) -> dict | None:
        """
        Obtiene datos de un ETF usando Alpha Vantage GLOBAL_QUOTE.

        Args:
            ticker: Símbolo del ETF

        Returns:
            Diccionario con datos del ETF o None si hay error
        """
        self._check_limit()

        try:
            logger.debug(f"Obteniendo datos de {ticker} (llamadas restantes: {self.get_remaining_calls()})")

            # GLOBAL_QUOTE da precio actual
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": ticker,
                "apikey": self.api_key,
            }

            response = requests.get(BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            self._increment_calls()

            data = response.json()

            # Verificar errores de API
            if "Error Message" in data:
                logger.error(f"Error de API para {ticker}: {data['Error Message']}")
                return None

            if "Note" in data:
                logger.warning(f"Límite de API alcanzado: {data['Note']}")
                raise APILimitExceeded("Límite de Alpha Vantage alcanzado")

            quote = data.get("Global Quote", {})
            if not quote:
                logger.warning(f"Sin datos para {ticker}")
                return None

            precio = self._to_decimal(quote.get("05. price"))
            precio_anterior = self._to_decimal(quote.get("08. previous close"))
            cambio_pct = self._to_decimal(quote.get("10. change percent", "0").replace("%", ""))

            return {
                "precio_actual": precio,
                "rendimiento_anual": None,  # GLOBAL_QUOTE no da rendimiento anual
                "rendimiento_ytd": cambio_pct,  # Usamos cambio diario como aproximación
            }

        except APILimitExceeded:
            raise
        except requests.RequestException as e:
            logger.error(f"Error de red para {ticker}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error obteniendo datos de {ticker}: {e}")
            return None

    def _to_decimal(self, value) -> Decimal | None:
        """Convierte un valor a Decimal."""
        if value is None:
            return None
        try:
            return Decimal(str(value)).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError):
            return None

    def save_to_db(self, etf_info: dict, data: dict) -> bool:
        """
        Guarda datos de un ETF en la base de datos.

        Args:
            etf_info: Información del ETF (ticker, nombre, tipo, mercado)
            data: Datos obtenidos (precio, rendimientos)

        Returns:
            True si se insertó correctamente
        """
        fecha_hoy = date.today()

        with get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO fondos_etfs
                        (ticker, nombre, tipo, mercado, precio_actual,
                         rendimiento_anual, rendimiento_ytd, fecha_actualizacion)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (ticker, fecha_actualizacion) DO UPDATE SET
                            precio_actual = EXCLUDED.precio_actual,
                            rendimiento_anual = EXCLUDED.rendimiento_anual,
                            rendimiento_ytd = EXCLUDED.rendimiento_ytd
                    """, (
                        etf_info["ticker"],
                        etf_info["nombre"],
                        etf_info["tipo"],
                        etf_info["mercado"],
                        data.get("precio_actual"),
                        data.get("rendimiento_anual"),
                        data.get("rendimiento_ytd"),
                        fecha_hoy,
                    ))
                    conn.commit()
                    return True

                except Exception as e:
                    logger.error(f"Error guardando {etf_info['ticker']}: {e}")
                    conn.rollback()
                    return False

    def collect(self, max_etfs: int | None = None) -> int:
        """
        Recopila y guarda datos de ETFs.

        Args:
            max_etfs: Máximo de ETFs a procesar (None = todos los posibles)

        Returns:
            Número de ETFs procesados exitosamente
        """
        restantes = self.get_remaining_calls()
        logger.info(f"Llamadas API restantes hoy: {restantes}/{MAX_DAILY_CALLS}")

        if restantes == 0:
            logger.warning("No hay llamadas disponibles hoy. Reintenta mañana.")
            return 0

        # Limitar a las llamadas disponibles
        etfs_a_procesar = ETFS_LIST[:min(len(ETFS_LIST), restantes)]
        if max_etfs:
            etfs_a_procesar = etfs_a_procesar[:max_etfs]

        logger.info(f"Procesando {len(etfs_a_procesar)} ETFs...")

        exitosos = 0

        for etf_info in etfs_a_procesar:
            ticker = etf_info["ticker"]

            try:
                data = self.fetch_etf_data(ticker)

                if data:
                    if self.save_to_db(etf_info, data):
                        exitosos += 1
                        logger.info(f"{ticker}: ${data.get('precio_actual')}")
                else:
                    logger.warning(f"{ticker}: Sin datos disponibles")

                # Pausa para evitar rate limiting
                time.sleep(1)

            except APILimitExceeded as e:
                logger.warning(str(e))
                break

        logger.info(f"Recopilación completada: {exitosos} ETFs guardados")
        logger.info(f"Llamadas restantes: {self.get_remaining_calls()}/{MAX_DAILY_CALLS}")
        return exitosos


def run_collector():
    """Ejecuta el collector de ETFs."""
    try:
        collector = ETFCollector()
        collector.collect()
    except ValueError as e:
        logger.error(f"Error de configuración: {e}")
    except Exception as e:
        logger.exception(f"Error ejecutando collector: {e}")


if __name__ == "__main__":
    run_collector()
