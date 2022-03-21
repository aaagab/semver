#!/usr/bin/env python3

if __name__ == "__main__":
    from pprint import pprint
    import importlib
    import os
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


    results=pkg.semver(versions)

    """
    <valid semver> ::= <version core>
        | <version core> "-" <pre-release>
        | <version core> "+" <build>
        | <version core> "-" <pre-release> "+" <build>
    """


    # version_core precedence: compare major then minor then patch
    # version_core-pre has lower precedence than version_core
    # version_core has same precedence has version_core-build
    # version_core-pre has same precedence has version_core-pre-build
    # version_core-pre numeric identifiers have lower precedence than non-numeric identifiers
    # A larger set of pre-release fields has a higher precedence than a smaller set, if all of the preceding identifiers are equal.

    expected=[
        [
            "0.1.0-3",
        ],
        [
            "0.1.0",
            "0.1.0",
        ],
        [
            "1.0.0-0.3.7",
        ],
        [
            "1.0.0-alpha",
            "1.0.0-alpha",
            "1.0.0-alpha+001",
        ],
        [
            "1.0.0-alpha.1",
            "1.0.0-alpha.1",
        ],
        [
            "1.0.0-alpha.beta",
        ],
        [
            "1.0.0-x.7.z.92",
        ],
        [
            "1.0.0-x-y-z.-",
        ],
        [
            "1.0.0-beta",
            "1.0.0-beta+exp.sha.5114f85",
        ],
        [
            "1.0.0-beta.2",
        ],
        [
            "1.0.0-beta.11",
        ],
        [
            "1.0.0-rc.1",
        ],
        [
            "1.0.0",
            "1.0.0+20130313144700",
            "1.0.0+21AF26D3--117B344092BD",
        ],
        [
            "1.9.3",
        ],
        [
            "5.0.0--",
        ],
        [
            "5.0.0",
            "5.0.0+-",

        ],
        [
            "12.0.1",
        ],
        [
            "12.5.0",
        ],
        [
            "12.5.1-alpha",
            "12.5.1-alpha+build",
        ],
        [
            "12.5.1",
        ],
    ]

    results_flatten=[]
    for lst in results:
        for elem in lst:
            results_flatten.append(elem)

    results_flatten.sort()

    # results_flatten.append("3.4.6")
    # results_flatten.append("3.4.6")
    # del results_flatten[-2]
    # del results_flatten[-1]
    # del results_flatten[0]
    # del results_flatten[-3:]
    # del results_flatten[3]
    # results_flatten=[]

    def print_details(label, data):
        print("{}:".format(label))
        pprint(data)
        print()

    tmp_versions=sorted(versions)

    for i, tmp_version in enumerate(tmp_versions):
        is_end_versions=i+1>=len(tmp_versions)
        is_end_results_flatten=i+1>=len(results_flatten)

        try:
            result_flatten=results_flatten[i]
            if tmp_version != result_flatten:
                print_details("versions", tmp_versions)
                print_details("results_flatten", results_flatten)
                print("Error mismatch: tmp_versions[{}]='{}' != results_flatten[{}]='{}'".format(i, tmp_version, i, result_flatten))
                sys.exit(1)
        except IndexError:
            print("error")
            print_details("versions", tmp_versions)
            print_details("results_flatten", results_flatten)
            print_details("Missing results_flatten elems", tmp_versions[i:])
            sys.exit(1)

        if is_end_versions is True and is_end_results_flatten is False:
            print_details("versions", tmp_versions)
            print_details("results_flatten", results_flatten)
            print_details("Excess results_flatten elems", results_flatten[i+1:])
            sys.exit(1)

    # results.append(["3.4.6"])
    # results.append(["3.4.6"])
    # del results[-2]
    # del results[-1]
    # del results[0]
    # del results[1][1]
    # del results[-3:]
    # del results[3]
    # results=[]

    for i, lst_expecteds in enumerate(expected):
        is_end_expected=i+1>=len(expected)
        is_end_results=i+1>=len(results)

        try:
            lst_results=results[i]

            for j, lst_expected in enumerate(lst_expecteds):
                    is_end_lst_expecteds=j+1>=len(lst_expecteds)
                    is_end_lst_results=j+1>=len(lst_results)

                    try:
                        lst_result=lst_results[j]

                        if lst_expected != lst_result:
                            print_details("expected", expected)
                            print_details("results", results)
                            print_details("lst_expecteds", lst_expecteds)
                            print_details("lst_results", lst_results)
                            print("Error mismatch at index '{}': lst_expected[{}]='{}' != lst_results[{}]='{}'".format(i, j, lst_expected, j, lst_result))
                            sys.exit(1)
            
                    except IndexError:
                        print_details("expected", expected)
                        print_details("results", results)
                        print_details("lst_expecteds", lst_expecteds)
                        print_details("lst_results", lst_results)
                        print_details("Missing lst_results elems", lst_expecteds[j:])
                        sys.exit(1)

                    if is_end_lst_expecteds is True and is_end_lst_results is False:
                        print_details("expected", expected)
                        print_details("results", results)
                        print_details("lst_expecteds", lst_expecteds)
                        print_details("lst_results", lst_results)
                        print_details("Excess lst_results elems", lst_results[j+1:])
                        sys.exit(1)
 
        except IndexError:
            print_details("expected", expected)
            print_details("results", results)
            print_details("Missing results elems", expected[i:])
            sys.exit(1)

        if is_end_expected is True and is_end_results is False:
            print_details("expected", expected)
            print_details("results", results)
            print_details("Excess results elems", results[i+1:])
            sys.exit(1)

    print("Success:")
    print_details("versions", versions)
    print_details("expected", expected)
    print_details("results", results)
