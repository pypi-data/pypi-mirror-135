# Hestia Engine Models

[![Pipeline Status](https://gitlab.com/hestia-earth/hestia-engine-models/badges/master/pipeline.svg)](https://gitlab.com/hestia-earth/hestia-engine-models/commits/master)
[![Coverage Report](https://gitlab.com/hestia-earth/hestia-engine-models/badges/master/coverage.svg)](https://gitlab.com/hestia-earth/hestia-engine-models/commits/master)

Hestia's set of models for running calculations or retrieving data using external datasets and internal lookups.

## Documentation

Documentation for every model can be found in the [Hestia API Documentation](https://hestia.earth/docs/#hestia-calculation-models).

## Install

1. Install python `3` (we recommend using python `3.6` minimum)
2. Install the module:
```bash
pip install hestia_earth.models
```
3. Set the following environment variables:
```
API_URL=https://api.hestia.earth
WEB_URL=https://hestia.earth
```

### Usage

```python
from hestia_earth.models.pooreNemecek2018 import run

# cycle is a JSONLD node Cycle
run('no3ToGroundwaterSoilFlux', cycle_data)
```
