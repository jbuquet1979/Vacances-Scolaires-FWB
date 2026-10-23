"""Coordinateur pour l'intégration Vacances Scolaires FWB."""
from datetime import datetime, timedelta
import logging
import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
API_URL = "https://openholidaysapi.org/SchoolHolidays"


class FWBSchoolHolidaysCoordinator(DataUpdateCoordinator):
    """Coordinateur pour récupérer les vacances scolaires de la FWB."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialisation du coordinateur."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=12),
        )

    async def _async_update_data(self):
        """Récupère les données depuis l'API OpenHolidays et filtre pour BE-FR."""
        now = datetime.now()
        start_date = f"{now.year - 1}-07-01"
        end_date = f"{now.year + 1}-08-31"
        
        # On interroge la Belgique entière pour la période
        params = {
            "countryIsoCode": "BE",
            "validFrom": start_date,
            "validTo": end_date,
            "languageIsoCode": "FR",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(API_URL, params=params, timeout=10) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Erreur HTTP: {response.status}")
                    data = await response.json()
                    
                    # Filtrage strict pour ne garder que les vacances de la communauté française (BE-FR)
                    fwb_holidays = []
                    for item in data:
                        groups = item.get("groups", [])
                        if any(group.get("code") == "BE-FR" for group in groups):
                            fwb_holidays.append(item)
                            
                    return fwb_holidays
            except Exception as error:
                raise UpdateFailed(f"Erreur de communication avec l'API: {error}") from error
            