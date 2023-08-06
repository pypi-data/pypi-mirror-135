# Fact Explorer

Welcome to fact_explorer. You can find more extensive documentation over at [readthedocs](https://fact-explorer.readthedocs.io/en/latest/).

This is a companion project to `factcast <https://github.com/factcast/factcast>`_ an event store written in Java.
You can also check out other event sourcing related project in python over at `pyfactcast <https://pypi.org/project/pyfactcast/>`_
as well as `cryptoshred <https://pypi.org/project/cryptoshred/>`_.

This project arose mainly out of the necessity to work with events directly instead of through projections. This is useful to:

- Enable searching for 'random' events quickly during debugging
- Checking events during migrations
- Many other things (you should probably not do if you are an event purist)

Contributions are welcome. Just get in touch.

## Quickstart

Simply `pip install fact-exporter` and get going. The cli is available as `fact-exporter` and
you can run `fact-exporter --help` to get up to speed on what you can do.

## Development

This project uses `poetry` for dependency management and `pre-commit` for local checks.
