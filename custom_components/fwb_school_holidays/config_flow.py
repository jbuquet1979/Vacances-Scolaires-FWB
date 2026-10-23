"""Config flow pour l'intégration Vacances Scolaires FWB."""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

DOMAIN = "fwb_school_holidays"
DEFAULT_NAME = "Vacances Scolaires FWB"

class FWBConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gère le flux de configuration de l'intégration."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Gère l'étape initiale de configuration par l'utilisateur."""
        if user_input is not None:
            return self.async_create_entry(
                title=DEFAULT_NAME, data={}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )
    