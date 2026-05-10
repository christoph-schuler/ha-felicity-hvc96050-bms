from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import FelicityBMSCoordinator

SENSOR_DESCRIPTIONS: dict[str, SensorEntityDescription] = {
    # Pack overview
    "HV_Pack_SOC": SensorEntityDescription(
        key="HV_Pack_SOC",
        name="State of Charge",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    "HV_Pack_SOH": SensorEntityDescription(
        key="HV_Pack_SOH",
        name="State of Health",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-heart-variant",
        suggested_display_precision=1,
    ),
    "HV_Pack_Spannung": SensorEntityDescription(
        key="HV_Pack_Spannung",
        name="Pack Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    "HV_Pack_Strom": SensorEntityDescription(
        key="HV_Pack_Strom",
        name="Pack Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    # Charge/discharge limits
    "Max Lade Spannung": SensorEntityDescription(
        key="Max Lade Spannung",
        name="Max Charge Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=1,
    ),
    "Min Entlade Spannung": SensorEntityDescription(
        key="Min Entlade Spannung",
        name="Min Discharge Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=1,
    ),
    "Max Lade Strom": SensorEntityDescription(
        key="Max Lade Strom",
        name="Max Charge Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=1,
    ),
    "Max Entlade Strom": SensorEntityDescription(
        key="Max Entlade Strom",
        name="Max Discharge Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=1,
    ),
    # Cell extremes
    "Zelle_Hoechste_Spannung": SensorEntityDescription(
        key="Zelle_Hoechste_Spannung",
        name="Cell Voltage Maximum",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
    "Zelle_Niedrigste_Spannung": SensorEntityDescription(
        key="Zelle_Niedrigste_Spannung",
        name="Cell Voltage Minimum",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
    # Temperatures
    "Hoechste_Zell_Temperatur": SensorEntityDescription(
        key="Hoechste_Zell_Temperatur",
        name="Cell Temperature Maximum",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    "Niedrigste_Zell_Temperatur": SensorEntityDescription(
        key="Niedrigste_Zell_Temperatur",
        name="Cell Temperature Minimum",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    "Umgebungstemperatur": SensorEntityDescription(
        key="Umgebungstemperatur",
        name="Ambient Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    "Pack_Temp_NTC1": SensorEntityDescription(
        key="Pack_Temp_NTC1",
        name="Pack Temperature NTC1",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=1,
    ),
    "Pack_Temp_NTC2": SensorEntityDescription(
        key="Pack_Temp_NTC2",
        name="Pack Temperature NTC2",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=1,
    ),
    "Pack_Temp_NTC3": SensorEntityDescription(
        key="Pack_Temp_NTC3",
        name="Pack Temperature NTC3",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=1,
    ),
    "Hoechste_Zell_Temp_Modul": SensorEntityDescription(
        key="Hoechste_Zell_Temp_Modul",
        name="Hottest Cell: Module #",
        icon="mdi:map-marker",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    "Hoechste_Zell_Temp_Sensor": SensorEntityDescription(
        key="Hoechste_Zell_Temp_Sensor",
        name="Hottest Cell: Sensor #",
        icon="mdi:map-marker",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    "Niedrigste_Zell_Temp_Modul": SensorEntityDescription(
        key="Niedrigste_Zell_Temp_Modul",
        name="Coldest Cell: Module #",
        icon="mdi:map-marker",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    "Niedrigste_Zell_Temp_Sensor": SensorEntityDescription(
        key="Niedrigste_Zell_Temp_Sensor",
        name="Coldest Cell: Sensor #",
        icon="mdi:map-marker",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    # Module voltages
    "Modul_1_Spannung": SensorEntityDescription(
        key="Modul_1_Spannung", name="Cell Group 1 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_2_Spannung": SensorEntityDescription(
        key="Modul_2_Spannung", name="Cell Group 2 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_3_Spannung": SensorEntityDescription(
        key="Modul_3_Spannung", name="Cell Group 3 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_4_Spannung": SensorEntityDescription(
        key="Modul_4_Spannung", name="Cell Group 4 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_5_Spannung": SensorEntityDescription(
        key="Modul_5_Spannung", name="Cell Group 5 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_6_Spannung": SensorEntityDescription(
        key="Modul_6_Spannung", name="Cell Group 6 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_7_Spannung": SensorEntityDescription(
        key="Modul_7_Spannung", name="Cell Group 7 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_8_Spannung": SensorEntityDescription(
        key="Modul_8_Spannung", name="Cell Group 8 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_9_Spannung": SensorEntityDescription(
        key="Modul_9_Spannung", name="Cell Group 9 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_10_Spannung": SensorEntityDescription(
        key="Modul_10_Spannung", name="Cell Group 10 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_11_Spannung": SensorEntityDescription(
        key="Modul_11_Spannung", name="Cell Group 11 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    "Modul_12_Spannung": SensorEntityDescription(
        key="Modul_12_Spannung", name="Cell Group 12 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    # System
    "BMS_Zyklen": SensorEntityDescription(
        key="BMS_Zyklen",
        name="Cycle Count",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
        suggested_display_precision=0,
    ),
    "BMS_Modus": SensorEntityDescription(
        key="BMS_Modus",
        name="BMS Mode",
        icon="mdi:cog",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    # Fault / alarm
    "BMS_Fault_Code": SensorEntityDescription(
        key="BMS_Fault_Code",
        name="Fault Code",
        icon="mdi:alert-circle",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    "BMS_Alarm_Flag": SensorEntityDescription(
        key="BMS_Alarm_Flag",
        name="Alarm Flag",
        icon="mdi:bell-alert",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    # Cell balance location — only valid during active balancing, otherwise garbage
    "Zelle_Max_Modul": SensorEntityDescription(
        key="Zelle_Max_Modul",
        name="Balancing: Highest Cell Module #",
        icon="mdi:battery-high",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    "Zelle_Max_Zelle": SensorEntityDescription(
        key="Zelle_Max_Zelle",
        name="Balancing: Highest Cell #",
        icon="mdi:battery-high",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    "Zelle_Min_Modul": SensorEntityDescription(
        key="Zelle_Min_Modul",
        name="Balancing: Lowest Cell Module #",
        icon="mdi:battery-low",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    "Zelle_Min_Zelle": SensorEntityDescription(
        key="Zelle_Min_Zelle",
        name="Balancing: Lowest Cell #",
        icon="mdi:battery-low",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
}


def _device_info(entry: ConfigEntry) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name="Felicity HVC96050 BMS",
        manufacturer="Felicity Solar",
        model="HVC96050 (Unofficial Integration)",
        configuration_url=f"http://{entry.data['host']}",
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: FelicityBMSCoordinator = hass.data[DOMAIN][entry.entry_id]
    device = _device_info(entry)
    entities = []
    for key, info in coordinator.sensors.items():
        desc = SENSOR_DESCRIPTIONS.get(info.name)
        entities.append(FelicityBMSSensor(coordinator, key, info, desc, device))
    async_add_entities(entities)


class FelicityBMSSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: FelicityBMSCoordinator,
        key: int,
        info: object,
        desc: SensorEntityDescription | None,
        device: DeviceInfo,
    ) -> None:
        self._coordinator = coordinator
        self._key = key
        self._attr_device_info = device
        self._attr_unique_id = f"{DOMAIN}_{key}"
        if desc is not None:
            self.entity_description = desc
        else:
            self._attr_name = getattr(info, "name", str(key))
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
        value = self._coordinator.get_state(self._key)
        if value is not None:
            self._attr_native_value = round(value, 4)
        self.async_write_ha_state()

    @property
    def native_value(self):
        value = self._coordinator.get_state(self._key)
        return round(value, 4) if value is not None else None

    @property
    def available(self) -> bool:
        return self._coordinator.available
