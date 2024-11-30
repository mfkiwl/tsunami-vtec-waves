# Measuring the Influence of Tsunamis on the Ionosphere 🌊📡

[![Open in GitHub Codespace](https://github.com/codespaces/badge.svg)](https://codespaces.new/d33pk3rn3l/tsunami-vtec-waves)

## Overview

This project investigates how tsunamis impact the ionosphere by analyzing VTEC (Vertical Total Electron Content) wave patterns from GNSS (Global Navigation Satellite System) data. By identifying key differences in VTEC signals between earthquakes that generate tsunamis and those that do not, we aim to develop early tsunami detection methods. This project builds upon previous studies that have demonstrated the capability of GPS TEC data to detect ionospheric disturbances caused by tsunamis.

## Objectives

- **Identify and analyze** VTEC wave patterns associated with tsunami and non-tsunami earthquakes.
- **Define key parameters** for early tsunami detection using GNSS data.
- Contribute to **improved natural hazard monitoring** through VTEC analysis.

## Methodology

1. **Event Selection**: Compare two earthquakes — one generating a tsunami (e.g., 2011 Tōhoku) and one that did not.
2. **Data Acquisition**: Collect GNSS VTEC LoS data from open sources like the Madrigal Database, focusing on the same time window for both events.
3. **Data Preprocessing**: Extract relevant measurements, filter noise, and correct biases.
4. **VTEC Analysis**: Use time-series and spatial mapping to calculate VTEC and identify key differences.
5. **Wave Propagation Analysis**: Visualize TEC propagation along Line-of-Sight (LOS) and measure wave speeds to detect tsunami-specific signatures.
6. **Parameter Identification**: Perform statistical analysis to define parameters that distinguish tsunami-induced waves.
7. **Validation**: Supplementary comparison across different events to validate the identified parameters.

## Expected Results

We anticipate observing differences in:
- **Wave propagation speed**
- **Spatial patterns**
- **Amplitude and frequency content** 

These variations in VTEC waveforms, propagation characteristics, and spatial distribution will help us define parameters associated with tsunami events, ultimately leading to improved early detection systems.

## Data 
Japan: 
2011-03-11 05:46:23 UTC M 9.1 -Tohoku TSUNAMI
2015-05-30 11:23:02 UTC M 7.8 - EARTHQUAKE

Japan24:
2024-01-01 07:10:09 (UTC) M 7.5 - 2024 Noto Peninsula, Japan Earthquake TSUNAMI
2024-08-08 07:42:55 (UTC)M 7.1 - 2024 Hyuganada Sea, Japan Earthquake EARTHQUAKE

Alaska:
2021-07-29 06:15:49 (UTC) M 8.2 - Alaska Peninsula TSUNAMI (small)
2021-08-14 11:57:43 (UTC) M 6.9 - 125 km SE of Perryville, Alaska EARTHQUAKE (no docu about tsunami)




TOO OLD FOR DATA

Salomonen:
2007-04-01 20:39:58 (UTC) M 8.1 - 45 km SSE of Gizo, Solomon Islands TSUNAMI
2009-10-07 22:18:51 (UTC) M 7.8 - 196 km NW of Sola, Vanuatu EARTHQUAKE

Samoa:
2009-09-29 17:48:10 (UTC) M 8.1 - 168 km SSW of Matavai, Samoa TSUNAMI
2009-03-19 18:17:40 (UTC) M 7.6 - 191 km S of ‘Ohonua, Tonga EARTHQUAKE

Sumatra:
2016-03-02 12:49:48 (UTC) M 7.8 - southwest of Sumatra, Indonesia EARTHQUAKE 
2004-12-26 00:58:53 (UTC)  M 9.1 - 2004 Sumatra - Andaman Islands Earthquake TSUNAMI


----------------------------------------------------------
~~
Water-Land aber gute doku

Chile:
2019-08-01 18:28:07 (UTC) (M6.8 - 96 km SW of San Antonio, Chile) TSUNAMI
2019-09-26 16:36:18 (UTC) (M 6.1 - 30 km W of Villa La Angostura, Argentina) Earthquake on land

Wasser Land, schlechte Doku

Timor
2021-12-29 (M 7.3 - 125 km NNE of Lospalos, Timor Leste) EARTHQUAKE
2021-12-14 (M 7.3 - Flores Sea) TSUNAMI~~
-----------------------------------------------------------

## References

- Komjathy, A., et al. (2016). *Review of ionospheric disturbances caused by tsunamis*.
- Galvan, D.A., et al. (2011). *2009 Samoa and Tonga tsunami: Ionospheric observations*.
- Rideout W., Cariglia K. CEDAR Madrigal Database URL: http://cedar.openmadrigal.org
