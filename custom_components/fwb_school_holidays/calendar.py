"""Support pour le calendrier des vacances scolaires FWB."""
from datetime import datetime, timedelta, date
import logging

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configure la plateforme calendrier FWB."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([FWBSchoolCalendar(coordinator)])


class FWBSchoolCalendar(CoordinatorEntity, CalendarEntity):
    """Représentation du calendrier des vacances scolaires FWB."""

    def __init__(self, coordinator) -> None:
        """Initialise le calendrier."""
        super().__init__(coordinator)
        self._attr_name = "Vacances Scolaires FWB"
        self._attr_unique_id = f"{DOMAIN}_calendar"

    def _parse_events(self) -> list[CalendarEvent]:
        """Convertit les données brutes de l'API en événements CalendarEvent."""
        events = []
        if not self.coordinator.data:
            return events

        for item in self.coordinator.data:
            # Filtrage strict de sécurité pour ne garder que BE-FR
            groups = item.get("groups", [])
            if not any(group.get("code") == "BE-FR" for group in groups):
                continue

            start_str = item.get("startDate")
            end_str = item.get("endDate")

            if not start_str or not end_str:
                continue

            # Extraction robuste du nom en français
            summary = "Vacances scolaires"
            name_data = item.get("name")
            if isinstance(name_data, list):
                for entry_name in name_data:
                    if entry_name.get("language") == "FR":
                        summary = entry_name.get("text", summary)
                        break
                else:
                    if name_data:
                        summary = name_data[0].get("text", summary)

            try:
                # OpenHolidays fournit des dates de type YYYY-MM-DD
                start_d = datetime.fromisoformat(start_str).date()
                end_d = datetime.fromisoformat(end_str).date()
                
                # Pour Home Assistant, la date de fin d'un événement all-day doit être exclusive (+1 jour)
                end_d_exclusive = end_d + timedelta(days=1)

                events.append(
                    CalendarEvent(
                        summary=summary,
                        start=start_d,
                        end=end_d_exclusive,
                        description="Vacances scolaires officielles FWB (OpenHolidays API)",
                    )
                )
            except Exception as err:
                _LOGGER.error("Erreur lors du parsing de la période %s: %s", summary, err)

        return events

    @property
    def event(self) -> CalendarEvent | None:
        """Retourne l'événement en cours ou le prochain."""
        events = self._parse_events()
        if not events:
            return None

        today = date.today()
        current_or_next = None
        min_diff = None

        for ev in events:
            # ev.start et ev.end sont des objets date. 
            # Note: ev.end est exclusif, donc l'événement englobe aujourd'hui si start <= today < end
            if ev.start <= today < ev.end:
                return ev
            if ev.start > today:
                diff = (ev.start - today).days
                if min_diff is None or diff < min_diff:
                    min_diff = diff
                    current_or_next = ev

        return current_or_next

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Retourne tous les événements sur une période donnée pour l'UI calendrier."""
        events = self._parse_events()
        matched_events = []
        
        start_d = start_date.date()
        end_d = end_date.date()

        for ev in events:
            # Intersection entre la plage demandée et l'événement (avec ev.end exclusif)
            if ev.start < end_d and ev.end > start_d:
                matched_events.append(ev)

        return matched_events
    