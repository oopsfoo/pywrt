#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import db

def subtarget_default(workdir, target):
    target_key = '%s/builddirs-%s'%(workdir, target) 
    default_key = '%s/builddirs-default' % workdir
    the_key = '%s/builddirs' % workdir

    scan_keys = [target_key, default_key, the_key]

    for key in scan_keys:
        if db.varTable.hasKey(key):
            subtargets = []
            for subtarget in db.varTable.getValue(key):
                if subtarget is not '.':
                    subtargets.append(subtarget)
            return subtargets

def subtarget(workdir, target):
    target_name = '%s/%s' % (workdir, target)
    for subtarget in subtarget_default(workdir, target):
        db.ruleTable.addDeps(target_name, '%s/%s/%s' % (workdir, subtarget, target))


def subdir(workdir):
    build_dirs = '%s/builddirs' % workdir

    default_subtargets = db.varTable.getValue('SUBTARGETS')
    workdir_subtargets = db.varTable.getValue('%s/subtargets' % workdir)
    subtargets = vars_join(default_subtargets, workdir_subtargets)

    for bd in db.varTable.getValue(build_dirs):
        for target in subtargets:
            pass #64-79

    for target in subtargets:
        subtarget(workdir, target)


def stampfile():
    pass


def vars_join(a, b):
    s = []
    if a is not None:
        s += a
    if b is not None:
        s += b
    return s

def test_subdir_target():
    db.varTable.put('SUBTARGETS', ['clean', 'download', 'prepare', 'compile', 'update', 'refresh', 'prereq', 'dist', 'distcheck', 'configure', 'check', 'check-depends'])
    db.varTable.put('target/subtargets', ['install'])
    db.varTable.put('target/builddirs', ['linux', 'sdk', 'imagebuilder', 'toolchain'])
    db.varTable.put('target/builddirs-default', ['linux'])
    db.varTable.put('target/builddirs-install', ['linux', 'sdk', 'imagebuilder', 'toolchain'])
    subdir('target')
    db.ruleTable.dump()

if __name__ == "__main__":
    test_subdir_target()
