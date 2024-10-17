# Measuring the Influence of Tsunamis on the Ionosphere 🌊📡

[![Open in GitHub Codespace](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?repository=tsunami-vtec-waves)

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

## References

- Komjathy, A., et al. (2016). *Review of ionospheric disturbances caused by tsunamis*.
- Galvan, D.A., et al. (2011). *2009 Samoa and Tonga tsunami: Ionospheric observations*.
- Rideout W., Cariglia K. CEDAR Madrigal Database URL: http://cedar.openmadrigal.org
