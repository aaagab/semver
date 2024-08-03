#!/usr/bin/env python3
from pprint import pprint
import os
import sys
import re

class NotSemanticVersion(Exception):
        pass

class SemVer():
    def __init__(self, version:str):
        self.version: str =version
        reg=re.match(get_reg_semver(), self.version)
        self.major: int
        self.minor: int
        self.patch: int
        self.pre: str
        self.build: str
        if reg:
            dy_reg=reg.groupdict()
            self.major=int(dy_reg["major"])
            self.minor=int(dy_reg["minor"])
            self.patch=int(dy_reg["patch"])
            
            self.pre=dy_reg["prerelease"]
            if self.pre is None:
                self.pre=""
            else:
                self.pre=f"-{self.pre}"

            self.build=dy_reg["buildmetadata"]
            if self.build is None:
                self.build=""
            else:
                self.build=f"+{self.build}"
        else:
            raise NotSemanticVersion(version)

def get_reg_semver():
    return r"""
    ^
        (?P<major>0|[1-9]\d*)\.
        (?P<minor>0|[1-9]\d*)\.
        (?P<patch>0|[1-9]\d*)
        (?:-
            (?P<prerelease>
                (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
                (?:\.
                    (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
                )*
            )
        )?
        (?:\+
            (?P<buildmetadata>[0-9a-zA-Z-]+
                (?:\.[0-9a-zA-Z-]+)*
            )
        )?
    $
    """.replace(" ", "").replace("\n", "")

def semver(
    versions,
    flatten=False,
    no_duplicates=False,
    get_groupdicts=False,
):
    consts=dict(
        build="[build]",
        end="[end]",
        int="[int]",
        pre="[pre]",
        str="[str]",
    )

    rule=get_reg_semver()
    
    dys=dict()
    dy_count=dict()
    dy_groupdicts=dict()
    for version in versions:
        reg=re.match(rule, version)
        if reg:
            if no_duplicates is False:
                if version in dy_count:
                    dy_count[version]+=1
                else:
                    dy_count[version]=1

            dy_reg=reg.groupdict()
            major=int(dy_reg["major"])
            minor=int(dy_reg["minor"])
            patch=int(dy_reg["patch"])
            pre=dy_reg["prerelease"]
            build=dy_reg["buildmetadata"]

            if get_groupdicts is True:
                if version not in dy_groupdicts:
                    dy_groupdicts[version]=dict(
                        build=None,
                        major=major,
                        minor=minor,
                        patch=patch,
                        pre_release=None,
                        version=version,
                    )
                    if build is not None:
                        dy_groupdicts[version]["build"]="+{}".format(build)
                    if pre is not None:
                        dy_groupdicts[version]["pre_release"]="-{}".format(pre)


            if major not in dys:
                dys[major]=dict()
            if minor not in dys[major]:
                dys[major][minor]=dict()
            if patch not in dys[major][minor]:
                dys[major][minor][patch]=dict()

            if pre is None and build is None:
                dys[major][minor][patch][consts["end"]]=dict()
            else:
                if pre is not None:
                    if consts["pre"] not in dys[major][minor][patch]:
                        dys[major][minor][patch][consts["pre"]]=dict()
                    tmpdy=dys[major][minor][patch][consts["pre"]]
                    tmpdy=set_values(
                        consts,
                        pre.split("."),
                        tmpdy,
                        endTmpdy=build is None,
                    )

                    if build is not None:
                        if consts["build"] not in tmpdy:
                            tmpdy[consts["build"]]=dict()
                        tmpdy=tmpdy[consts["build"]]
                        set_values(
                            consts,
                            build.split("."),
                            tmpdy,
                            endTmpdy=True,
                        )

                elif build is not None:
                    if consts["build"] not in dys[major][minor][patch]:
                        dys[major][minor][patch][consts["build"]]=dict()
                    tmpdy=dys[major][minor][patch][consts["build"]]
                    tmpdy=set_values(
                        consts,
                        build.split("."),
                        tmpdy,
                        endTmpdy=True,
                    )
        else:
            raise NotSemanticVersion(version)

    lst_versions=[]
    sort_versions(
        consts,
        dy_count,
        dy_groupdicts,
        dys,
        lst_versions,
        flatten,
        no_duplicates,
        get_groupdicts,
    )

    return lst_versions

def set_values(
    consts,
    values,
    tmpdy,
    endTmpdy,
):
    index=0
    for value in values:
        if re.match(r"^(0|[1-9]\d*)$", value):
            value=int(value)
            if consts["int"]  not in tmpdy:
                tmpdy[consts["int"]]=dict()
            tmpdy=tmpdy[consts["int"]] 
        else:
            if consts["str"]  not in tmpdy:
                tmpdy[consts["str"]]=dict()
            tmpdy=tmpdy[consts["str"]] 

        if value not in tmpdy:
            tmpdy[value]=dict()
        tmpdy=tmpdy[value]

        index+=1

        if index == len(values):
            if endTmpdy is True:
                tmpdy[consts["end"]]=dict()

    return tmpdy


def sort_versions(
    consts,
    dy_count,
    dy_groupdicts,
    dys,
    lst_versions,
    flatten,
    no_duplicates,
    get_groupdicts,
    level="major",
    is_build=False,
    is_pre=False,
    concat="",
    has_dot=False,
):
    if level in ["major", "minor", "patch"]:
        next_level=None
        if level == "major":
            next_level="minor"
        elif level == "minor":
            next_level="patch"
        elif level == "patch":
            next_level="afterpatch"
        for elem in sorted(dys):
            tmp_concat=None
            if level == "major":
                tmp_concat="{}".format(elem)
            else:
                tmp_concat="{}.{}".format(concat, elem)

            sort_versions(
                consts,
                dy_count,
                dy_groupdicts,
                dys[elem],
                lst_versions=lst_versions,
                flatten=flatten,
                no_duplicates=no_duplicates,
                get_groupdicts=get_groupdicts,
                level=next_level,
                is_build=False,
                is_pre=False,
                concat=tmp_concat,
                has_dot=False,
            )
    elif level == "afterpatch":
        if consts["pre"] in dys:
            next_level="pre"
            tmp_concat="{}-".format(concat)
            sort_versions(
                consts,
                dy_count,
                dy_groupdicts,
                dys[consts["pre"]],
                lst_versions=lst_versions,
                flatten=flatten,
                no_duplicates=no_duplicates,
                get_groupdicts=get_groupdicts,
                level=next_level,
                is_build=False,
                is_pre=False,
                concat=tmp_concat,
                has_dot=False,
            )

        if consts["end"] in dys:
            if flatten is False:
                lst_versions.append([])
            insert_lst_versions(no_duplicates, flatten, dy_count, dy_groupdicts, get_groupdicts, concat, lst_versions)

        if consts["build"] in dys:
            next_level="build"
            tmp_concat="{}+".format(concat)
            sort_versions(
                consts,
                dy_count,
                dy_groupdicts,
                dys[consts["build"]],
                lst_versions=lst_versions,
                flatten=flatten,
                no_duplicates=no_duplicates,
                get_groupdicts=get_groupdicts,
                level=next_level,
                is_build=False,
                is_pre=False,
                concat=tmp_concat,
                has_dot=False,
            )


    elif level == "pre":
        if consts["end"] in dys:
            if flatten is False:
                lst_versions.append([])
            insert_lst_versions(no_duplicates, flatten, dy_count, dy_groupdicts, get_groupdicts, concat, lst_versions)

        if consts["build"] in dys:
            next_level="build"
            tmp_concat="{}+".format(concat)
            sort_versions(
                consts,
                dy_count,
                dy_groupdicts,
                dys[consts["build"]],
                lst_versions=lst_versions,
                flatten=flatten,
                no_duplicates=no_duplicates,
                get_groupdicts=get_groupdicts,
                level=next_level,
                is_build=False,
                is_pre=False,
                concat=tmp_concat,
                has_dot=False,
            )

        if consts["int"] in dys:
            for elem in dys[consts["int"]]:
                tmp_concat=concat
                if has_dot is True:
                    tmp_concat="{}.".format(concat);
                tmp_concat="{}{}".format(tmp_concat, elem)
                sort_versions(
                    consts,
                    dy_count,
                    dy_groupdicts,
                    dys[consts["int"]][elem],
                    lst_versions=lst_versions,
                    flatten=flatten,
                    no_duplicates=no_duplicates,
                    get_groupdicts=get_groupdicts,
                    level=level,
                    is_build=False,
                    is_pre=False,
                    concat=tmp_concat,
                    has_dot=True,
                )

        if consts["str"] in dys:
            for elem in dys[consts["str"]]:
                tmp_concat=concat
                if has_dot is True:
                    tmp_concat="{}.".format(concat);
                tmp_concat="{}{}".format(tmp_concat, elem)
                sort_versions(
                    consts,
                    dy_count,
                    dy_groupdicts,
                    dys[consts["str"]][elem],
                    lst_versions=lst_versions,
                    flatten=flatten,
                    no_duplicates=no_duplicates,
                    get_groupdicts=get_groupdicts,
                    level=level,
                    is_build=False,
                    is_pre=False,
                    concat=tmp_concat,
                    has_dot=True,
                )

    elif level == "build":
        if consts["end"] in dys:
            if flatten is False:
                if len(lst_versions) == 0:
                    lst_versions.append([])
            insert_lst_versions(no_duplicates, flatten, dy_count, dy_groupdicts, get_groupdicts, concat, lst_versions)

        if consts["int"] in dys:
            for elem in dys[consts["int"]]:
                tmp_concat=concat
                if has_dot is True:
                    tmp_concat="{}.".format(concat);
                tmp_concat="{}{}".format(tmp_concat, elem)
                sort_versions(
                    consts,
                    dy_count,
                    dy_groupdicts,
                    dys[consts["int"]][elem],
                    lst_versions=lst_versions,
                    flatten=flatten,
                    no_duplicates=no_duplicates,
                    get_groupdicts=get_groupdicts,
                    level=level,
                    is_build=False,
                    is_pre=False,
                    concat=tmp_concat,
                    has_dot=True,
                )
    
        if consts["str"] in dys:
            for elem in dys[consts["str"]]:
                tmp_concat=concat
                if has_dot is True:
                    tmp_concat="{}.".format(concat);
                tmp_concat="{}{}".format(tmp_concat, elem)
                sort_versions(
                    consts,
                    dy_count,
                    dy_groupdicts,
                    dys[consts["str"]][elem],
                    lst_versions=lst_versions,
                    flatten=flatten,
                    no_duplicates=no_duplicates,
                    get_groupdicts=get_groupdicts,
                    level=level,
                    is_build=False,
                    is_pre=False,
                    concat=tmp_concat,
                    has_dot=True,
                )

def insert_lst_versions(
    no_duplicates,
    flatten,
    dy_count,
    dy_groupdicts,
    get_groupdicts,
    concat,
    lst_versions,
):
    if no_duplicates is True:
        if flatten is True:
            if get_groupdicts is True:
                lst_versions.append(dy_groupdicts[concat])
            else:
                lst_versions.append(concat)
        else:
            if get_groupdicts is True:
                lst_versions[-1].append(dy_groupdicts[concat])
            else:
                lst_versions[-1].append(concat)
    else:
        for i in range(dy_count[concat]):
            if flatten is True:
                if get_groupdicts is True:
                    lst_versions.append(dy_groupdicts[concat])
                else:
                    lst_versions.append(concat)
            else:
                if get_groupdicts is True:
                    lst_versions[-1].append(dy_groupdicts[concat])
                else:
                    lst_versions[-1].append(concat)

