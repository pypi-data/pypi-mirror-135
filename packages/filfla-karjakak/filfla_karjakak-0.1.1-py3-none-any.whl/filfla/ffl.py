# -*- coding: utf-8 -*-
# Copyright (c) 2022, KarjaKAK
# All rights reserved.

import os, stat
import argparse
from enum import Enum, unique


@unique
class FileFlags(Enum):
    HIDDEN = stat.UF_HIDDEN
    APPEND = stat.UF_APPEND
    COMPRESSED = stat.UF_COMPRESSED
    IMMUTABLE = stat.UF_IMMUTABLE
    NODUMP = stat.UF_NODUMP
    NOUNLINK = stat.UF_NOUNLINK
    OPAQUE = stat.UF_OPAQUE

    def __str__(self):
        return self.name


class FilFla:

    def __init__(self, pth: str):
        if os.path.exists(pth):
            self.pth = pth
        else:
            raise FileExistsError(f'{pth}\nis not exist!')
        self.flags = FileFlags._member_names_

    def prt(self, st: int, p1: bool = True, flname: str = None ):

        match p1:
            case True:
                print(
                    f"{self.pth}\n"
                    f"Flag status: {st}"
                )
            case False:
                tx = f"{st} - NORMAL" if flname is None else f"{st} - {flname}"
                print(
                    f"\n{self.pth}\n"
                    f"Status Change: {tx}"
                )

    def _chekers(self):
        st = os.stat(self.pth).st_flags
        try:
            if st:
                return str(FileFlags(st))
            else:
                return None
        except Exception as e:
            print(e)

    def flagger(self, flname: str):

        if flname in self.flags:
            st = None
            flag = FileFlags[flname].value
            if (ck := self._chekers()) is None:
                st = os.stat(self.pth).st_flags
                self.prt(st)
                os.chflags(self.pth, st ^ flag)
            else:
                ck = FileFlags[ck].value
                self.prt(ck)
                os.chflags(self.pth, ck ^ ck)
                if flag != ck:
                    st = os.stat(self.pth).st_flags
                    os.chflags(self.pth, st ^ flag)
                
            match st:
                case 0:
                    self.prt(os.stat(self.pth).st_flags, False, flname)
                case _:
                    self.prt(os.stat(self.pth).st_flags, False)
            del st, flag, ck
        else:
            print("Not implemented!")


def main():
    parser = argparse.ArgumentParser(
        prog="File Flagger", description="File flag status check and change"
    )
    parser.add_argument("-p", "--path", type=str, help="Give file's path")
    args = parser.parse_args()

    match args.path:
        case path if os.path.exists(path):
            cho = input(
                'To check file flag or change file flag? ["C" to check and "A" to change] '
            )
            match cho.upper():
                case "C":
                    try:
                        x = FilFla(path)
                        if st := x._chekers():
                            x.prt(FileFlags[st].value)
                            print(f"Flag: {FileFlags[st].name}")
                        else:
                            print(f"{path}\nFlag: {st}")
                    except Exception as e:
                        print(e)
                case "A":
                    try:
                        flag = input(f"Change flag? {FileFlags._member_names_} ")
                        x = FilFla(path)
                        x.flagger(flag)
                    except Exception as e:
                        print(e)
                case _:
                    print("Abort!")
        case _:
            print(f"{args.path} is not a file!")


if __name__ == "__main__":
    main()