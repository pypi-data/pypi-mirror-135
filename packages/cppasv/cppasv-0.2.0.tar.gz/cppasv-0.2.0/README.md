# Google C++ Benchmarks in Airspeed Velocity

`cppasv` is a Python module that wraps [Google Benchmark](https://github.com/google/benchmark) benchmarks written in C++ for execution with [Airspeed Velocity](https://asv.readthedocs.io/en/stable/index.html), a tool to run Python benchmarks.

For an example on how to use this module, have a look at the [flatsurf/flatsurf](https://github.com/flatsurf/flatsurf), in particular its [asv configuration](https://github.com/flatsurf/flatsurf/blob/master/asv.conf.json) and the [Python benchmarks that wrap the C++ benchmarks](https://github.com/flatsurf/flatsurf/blob/master/tools/asv/__init__.py).
