# -*- coding: utf-8 -*-
# Copyright (c) 2022, KarjaKAK
# All rights reserved.

import os, sys
import stat
import subprocess as sp
import argparse
from pathlib import Path

# Reference:
# https://www.macinstruct.com/tutorials/how-to-set-file-permissions-on-a-mac/


class FilePermission:
    """
    File Permission changer and checking status permission
    """

    def __init__(self, filep: str):
        match filep:
            case filep if not os.path.exists(filep):
                raise TypeError(f"{filep} Is not exist!")
            case _:
                self.filep = filep
        self.seq = None
        self.seqp = []

    def _chkseq(self, seq: int, sil: bool = False):
        """
        Sequence mode checking
        """

        ck = [str(n) for n in range(1,8)]
        match seq:
            case seq if not isinstance(seq, int):
                raise TypeError(f"{seq} is not integer!")
            case seq if not isinstance(sil, bool):
                raise TypeError(f"{sil} is not bool type!")
            case 0:
                warn = input(
                    "WARNING: file will be locked and any undesire behaviour may happen! [n/y] "
                ) if sil is False else 'Y'
                match warn.lower():
                    case 'y':
                        self.seq = 000
                    case _:
                        sys.exit()
            case seq if not len(str(seq)) == 3:
                raise ValueError(f"{seq} is invalid!")
            case _:
                for i in str(seq):
                    if not i in ck:
                        match i:
                            case '0':
                                warn = input(
                                    f"WARNING: file will be locked for some users and any undesire" 
                                    f" behaviour may happen! [n/y] "
                                ) if sil is False else 'Y'
                                match warn.lower():
                                    case 'y':
                                        self.seq = seq
                                    case _:
                                        sys.exit()
                            case _:
                                raise ValueError(
                                    f"{i} is not permission sequence mode for file!"
                                )
                else:
                    self.seq = seq
        del ck

    def changeperm(self, nums: int, sil: bool = False):
        """
        File permission changer
        """
        self._chkseq(nums, sil)

        pnam = [
            "chmod",
            f"{self.seq}",
            f"{self.filep}",
        ]
        with sp.Popen(
            pnam,
            stdout=sp.PIPE,
            stderr=sp.STDOUT,
            bufsize=1,
            universal_newlines=True,
            text=True,
        ) as p:
            if not (pr := p.stdout.read()):
                print(
                    f"The permission of {Path(self.filep).name} has been changed!"
                )
            else:
                print(pr)

    def getpermst(self):
        """
        Getting file permission status
        """

        a = stat.filemode(os.stat(self.filep).st_mode)
        attm = {
            "x": "1",
            "w": "2",
            "wx": "3",
            "r": "4",
            "rx": "5",
            "rw": "6",
            "rwx": "7",
            "": "0",
        }
        n = [-9, -6, -3]

        for i in n:
            if i == -3:
                self.seqp.append(attm.get(a[i:].replace("-", "")))
            else:
                self.seqp.append(attm.get(a[i : (i + 3)].replace("-", "")))
        print(f'Permission: {a}\nmode: {"".join(self.seqp)}')
        del a, attm, n
        self.seqp = []


def main():
    parser = argparse.ArgumentParser(
        prog="File Permission", description="File Permission status check and change"
    )
    parser.add_argument("-p", "--path", type=str, help="Give file's path")
    args = parser.parse_args()

    match args.path:
        case path if os.path.exists(path):
            cho = input(
                'To check file permission or change file permission? ["C" to check and "A" to change] '
            )
            match cho.upper():
                case "C":
                    try:
                        x = FilePermission(path)
                        x.getpermst()
                    except Exception as e:
                        print(e)
                case "A":
                    try:
                        num = int(input("Sequence Mode? [must be number order!] "))
                        x = FilePermission(path)
                        x.changeperm(num)
                        x.getpermst()
                    except Exception as e:
                        print(e)
                case _:
                    print("Abort!")
        case _:
            print(f"{args.path} is not a file!")


if __name__ == "__main__":
    main()
