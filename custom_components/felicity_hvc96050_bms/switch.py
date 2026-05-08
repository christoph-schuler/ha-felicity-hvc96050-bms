from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import FelicityBMSCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: FelicityBMSCoordinator = hass.data[DOMAIN][entry.entry_id]
    device = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name="Felicity HVC96050 BMS",
        manufacturer="Felicity Solar",
        model="HVC96050 (Unofficial Integration)",
        configuration_url=f"http://{entry.data['host']}",
    )
    entities = [
        FelicityBMSSwitch(coordinator, key, info, device)
        for key, info in coordinator.switches.items()
    ]
    async_add_entities(entities)


class FelicityBMSSwitch(SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: FelicityBMSCoordinator, key: int, info: object, device: DeviceInfo) -> None:
        self._coordinator = coordinator
        self._key = key
        self._attr_name = getattr(info, "name", str(key))
        self._attr_unique_id = f"{DOMAIN}_switch_{key}"
        self._attr_device_info = device
        self._unsubscribe: callable | None = None

    async def async_added_to_hass(self) -> None:
        self._unsubscribe = self._coordinator.add_listener(self._handle_update)
        self._handle_update()

    async def async_will_remove_from_hass(self) -> None:
        if self._unsubscribe:
            self._unsubscribe()

    @callback
    def _handle_update(self) -> None:
        self._attr_available = self._coordinator.available
        state = self._coordinator.get_state(self._key)
        if state is not None:
            self._attr_is_on = bool(state)
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool | None:
        state = self._coordinator.get_state(self._key)
        return bool(state) if state is not None else None

    @property
    def available(self) -> bool:
        return self._coordinator.available

    async def async_turn_on(self, **kwargs) -> None:
        await self._coordinator.async_switch_command(self._key, True)

    async def async_turn_off(self, **kwargs) -> None:
        await self._coordinator.async_switch_command(self._key, False)
