#!/usr/bin/env python3

if __name__ == "__main__":
    from pprint import pprint
    import importlib
    import os
    import re
    import sys
    direpa_script=os.path.dirname(os.path.realpath(__file__))
    direpa_script_parent=os.path.dirname(direpa_script)
    module_name=os.path.basename(direpa_script)
    sys.path.insert(0, direpa_script_parent)
    pkg = importlib.import_module(module_name)
    del sys.path[0]

    versions=[
        "0.1.0",
        "0.1.0",
        "0.1.0-3",
        "1.9.3",
        "1.0.0-alpha",
        "1.0.0-alpha.1",
        "1.0.0-0.3.7",
        "1.0.0-x.7.z.92",
        "1.0.0-x-y-z.-",
        "12.5.1-alpha+build",
        "12.5.0",
        "12.5.1",
        "12.5.1-alpha",
        "12.0.1",
        "5.0.0+-",
        "1.0.0-alpha+001",
        "1.0.0+20130313144700",
        "1.0.0-beta+exp.sha.5114f85",
        "5.0.0--",
        "1.0.0+21AF26D3--117B344092BD",
        "1.0.0-alpha",
        "5.0.0",
        "1.0.0-alpha.1",
        "1.0.0-alpha.beta",
        "1.0.0-beta",
        "1.0.0-beta.2",
        "1.0.0-beta.11",
        "1.0.0-rc.1",
        "1.0.0",
    ]

    print("raw results:")
    results=pkg.semver(versions)
    pprint(results)
    print()

    print("flattened:")
    results=pkg.semver(versions, flatten=True)
    pprint(results)
    print()

    print("no duplicates:")
    results=pkg.semver(versions, no_duplicates=True)
    pprint(results)
    print()

    print("flattened with no duplicates:")
    results=pkg.semver(versions, flatten=True, no_duplicates=True)
    pprint(results)
    print()

    print("Test version regex:")
    try:
        pkg.semver(["not-a-version"], flatten=True, no_duplicates=True)
    except pkg.NotSemanticVersion as e:
        print("Error syntax '{}'".format(e))
        print()
    
    print("Get groupdicts flattened with no_duplicates:")
    results=pkg.semver(versions, get_groupdicts=True, flatten=True, no_duplicates=True)
    pprint(results)
    print()

    reg=re.match(pkg.get_reg_semver(), "1.2.3")
    if reg is not None:
        print(reg.groupdict())
        print()

    print("Test Semver class:")
    try:
        pkg.SemVer("not-a-version")
    except pkg.NotSemanticVersion as e:
        print("Error syntax '{}'".format(e))
        print()

    sv=pkg.SemVer("1.2.3-alpha+build")
    pprint(vars(sv))
