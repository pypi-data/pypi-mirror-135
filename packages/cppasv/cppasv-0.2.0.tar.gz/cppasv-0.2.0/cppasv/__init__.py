r"""
This module turns google (C++) benchmarks into Python classes that can be run
by AirSpeedVelocity which provides a nice web interface to see how benchmarks
evolve over time.

If you want to use this module, make sure NOT to add the conda-forge package
'benchmark' (google benchmark) to your asv.conf.json matrix as that is a
reserved key in ASV. Instead add an exact pin such as 'benchmark==1.4.1'.
"""
#*****************************************************************************
#  This file is part of cppasv.
#
#        Copyright (C) 2019-2020 Julian Rüth
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#******************************************************************************

import subprocess

def create_wrappers(benchmark):
    r"""
    Return ASV compatible benchmark classes that contain a `track_time` method
    for each benchmark exported by the Google Benchmark binary `benchmark`.
    """
    benchmarks = subprocess.check_output([benchmark, "--benchmark_list_tests"]).decode('UTF-8').split('\n')

    benchmarks = [benchmark.strip().split('/') for benchmark in benchmarks if benchmark.strip()]

    benchmarks = create_time_methods(benchmark, benchmarks)

    benchmarks = { sanitize_benchmark_name(benchmark): benchmarks[benchmark] for benchmark in benchmarks }

    return {benchmark: create_benchmark_class(benchmark, time_method) for (benchmark, time_method) in benchmarks.items()}

def create_benchmark_class(name, time_method):
    r"""
    Return an ASV compatible benchmark class called `name` that runs the given method as `track_time`.
    """
    class Benchmark:
        track_time = time_method
    Benchmark.__name__ = name

    return Benchmark

def sanitize_benchmark_name(name):
    r"""
    Return the Google Benchmark name `name` rewritten as an identifier that ASV accepts.
    """
    name = name.strip()

    # < and > break resulting HTML output, so we replace them with similarly looking unicode characters.
    name = name.replace("<", "⟨")
    name = name.replace(">", "⟩")

    # :: break resulting HTML output (graphs do not display for such methods) so we replace them with similarly looking unicode characters.
    name = name.replace("::", "∷")

    return name

def create_time_methods(benchmark, benchmarks):
    r"""
    Return a mapping from sanitized benchmark names to Python methods that run that benchmark.
    """
    toplevel = set(b[0] for b in benchmarks)

    time_methods = { name: create_time_method(benchmark, name) for name in toplevel }
    
    params = { name: [tuple(b[1:]) for b in benchmarks if b[0] == name] for name in toplevel }

    for name in toplevel:
        if len(params[name]) > 1:
            time_methods[name].params = [ ", ".join(p) for p in params[name] ]

    return time_methods

def create_time_method(benchmark, name):
    r"""
    Return a method that runs the benchmark binary `benchmark` on the Google Benchmark called `name`.
    """
    def run_benchmark(self, params=None):
        filter = f"{name}"
        if params:
            filter = f"{name}/{params.replace(', ', '/')}"
        out = subprocess.check_output([benchmark, f"--benchmark_filter={filter}", "--benchmark_format=json"])

        import json
        out = json.loads(out)

        assert(len(out["benchmarks"]) == 1)
        time = out["benchmarks"][0]["cpu_time"]
        unit = out["benchmarks"][0]["time_unit"]

        if unit == "s":
            time *= 1000
            unit = "ms"
        if unit == "ms":
            time *= 1000
            unit = "us"
        if unit == "us":
            time *= 1000
            unit = "ns"

        assert(unit == "ns")

        return time

    run_benchmark.unit = "ns"

    # We cannot compute a version number of this benchmark yet since we cannot hash its original C++ source code easily.
    run_benchmark.version = 0

    # Google Benchmark already takes care of sampling for us, so we only run the benchmarks once.
    run_benchmark.repeat = 1
    run_benchmark.number = 1
    run_benchmark.min_run_count = 1

    # Show the original benchmark name in ASV output
    # Unfortunately, this breaks ASV's HTML output.
    # run_benchmark.name = name
    # run_benchmark.pretty_name = name

    return run_benchmark
