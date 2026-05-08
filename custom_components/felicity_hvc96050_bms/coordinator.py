from __future__ import annotations

import asyncio
import logging
from typing import Callable

import aioesphomeapi

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from .const import CONF_HOST, CONF_PASSWORD, CONF_PORT, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)

RECONNECT_INTERVAL = 30


class FelicityBMSCoordinator:
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self._host: str = entry.data[CONF_HOST]
        self._port: int = entry.data.get(CONF_PORT, DEFAULT_PORT)
        self._password: str | None = entry.data.get(CONF_PASSWORD) or None
        self._client: aioesphomeapi.APIClient | None = None
        self._sensor_info: dict[int, aioesphomeapi.SensorInfo] = {}
        self._switch_info: dict[int, aioesphomeapi.SwitchInfo] = {}
        self._states: dict[int, float | bool] = {}
        self._listeners: list[Callable[[], None]] = []
        self._reconnect_task: asyncio.Task | None = None
        self.available = False

    async def async_connect(self) -> None:
        self._client = aioesphomeapi.APIClient(
            self._host, self._port, self._password
        )
        await self._client.connect(login=True)
        entities, _ = await self._client.list_entities_services()
        for entity in entities:
            if isinstance(entity, aioesphomeapi.SensorInfo):
                self._sensor_info[entity.key] = entity
            elif isinstance(entity, aioesphomeapi.SwitchInfo):
                self._switch_info[entity.key] = entity
        self._client.subscribe_states(self._on_state)
        self._client.on_disconnect = self._on_disconnect
        self.available = True
        _LOGGER.debug("Connected to Felicity BMS at %s:%s", self._host, self._port)

    @callback
    def _on_state(self, state: aioesphomeapi.EntityState) -> None:
        self._states[state.key] = state.state
        for listener in self._listeners:
            listener()

    @callback
    def _on_disconnect(self, expected: bool) -> None:
        self.available = False
        _LOGGER.warning("Felicity BMS disconnected (expected=%s), reconnecting…", expected)
        for listener in self._listeners:
            listener()
        self._reconnect_task = self.hass.async_create_task(self._reconnect())

    async def _reconnect(self) -> None:
        while True:
            await asyncio.sleep(RECONNECT_INTERVAL)
            try:
                await self.async_connect()
                _LOGGER.info("Felicity BMS reconnected")
                return
            except Exception as err:
                _LOGGER.debug("Reconnect failed: %s", err)

    async def async_disconnect(self) -> None:
        if self._reconnect_task:
            self._reconnect_task.cancel()
        if self._client:
            await self._client.disconnect()

    def add_listener(self, listener: Callable[[], None]) -> Callable[[], None]:
        self._listeners.append(listener)

        def remove() -> None:
            self._listeners.remove(listener)

        return remove

    def get_state(self, key: int) -> float | bool | None:
        return self._states.get(key)

    @property
    def sensors(self) -> dict[int, aioesphomeapi.SensorInfo]:
        return self._sensor_info

    @property
    def switches(self) -> dict[int, aioesphomeapi.SwitchInfo]:
        return self._switch_info

    async def async_switch_command(self, key: int, state: bool) -> None:
        if self._client:
            await self._client.switch_command(key, state)
