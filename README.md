# Felicity HVC96050 BMS — Unofficial Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Unofficial HACS custom integration for the **Felicity ESS HVC96050** high-voltage battery pack (8-module, ~424 V LFP) via an ESPHome ESP32 Modbus bridge.

> **Not affiliated with Felicity Solar.** This is a community project.

## What it does

Connects to the ESPHome native API on the Waveshare ESP32-S3 relay board and exposes all BMS data as Home Assistant entities under a single **Felicity HVC96050 BMS** device:

| Entity | Description |
|--------|-------------|
| State of Charge | Pack SOC in % |
| State of Health | Pack SOH in % |
| Pack Voltage | Total pack voltage (~424 V) |
| Pack Current | Charge (+) / discharge (−) current |
| Cell Voltage Maximum / Minimum | Highest and lowest cell voltage |
| Cell Temperature Maximum / Minimum | Hottest and coldest cell |
| Ambient Temperature | BMS board temperature |
| Pack Temperature NTC 1–3 | Internal NTC sensors |
| Module 1–8 Voltage | Per-module voltage (~53 V each) |
| Max Charge / Discharge Voltage | BMS charge limits |
| Max Charge / Discharge Current | BMS current limits |
| Cycle Count | Total charge cycles |
| BMS Mode | Operating mode (2 = Battery Mode) |
| Fault Code / Alarm Flag | Error and alarm status |
| Relay 1–6 | Control switches for the relay board |

## Requirements

- Home Assistant 2024.1+
- [ESPHome](https://esphome.io/) flashed to a Waveshare ESP32-S3 6-relay board connected to the BMS via RS485
- The ESPHome YAML from this project: [relay.yaml](https://github.com/christoph-schuler/ha-felicity-hvc96050-bms/blob/main/relay.yaml)

## Installation via HACS

1. Open HACS → Integrations → ⋮ → Custom repositories
2. Add `https://github.com/christoph-schuler/ha-felicity-hvc96050-bms` as **Integration**
3. Install "Felicity HVC96050 BMS (Unofficial)"
4. Restart Home Assistant

## Configuration

After installation, go to **Settings → Devices & Services → Add Integration** and search for "Felicity".

Enter:
- **Host**: IP address of your ESP32 (e.g. `192.168.178.180`)
- **Port**: `6053` (ESPHome native API default)
- **Password**: leave empty if your `relay.yaml` has no API password

## ESPHome setup

1. Copy `secrets.yaml.example` to `secrets.yaml` next to `relay.yaml`
2. Fill in your WiFi credentials and the desired static IP for the ESP32
3. Flash with `esphome run relay.yaml`

`secrets.yaml` is in `.gitignore` and will never be committed. `relay.yaml` itself contains no credentials.

## Hardware setup

```
Felicity ESS HVC96050
  └── RS485 port
        └── Waveshare ESP32-S3 6-Relay Board (GPIO17=TX, GPIO18=RX)
              └── WiFi → Home Assistant
```

Relay 6 connects/disconnects the RS485 bus and should remain ON.

## License

MIT
