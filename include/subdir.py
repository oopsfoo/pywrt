#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import db

def subtarget_default(workdir, target):
    target_key = '%s/builddirs-%s'%(workdir, target) 
    default_key = '%s/builddirs-default' % workdir
    the_key = '%s/builddirs' %workdir

    scan_keys = [target_key, default_key, the_key]

    for key in scan_keys:
        if db.varTable.hasKey(key):
            return db.varTable.getValue(key)

def subtarget(workdir, target):
    target_name = '%s/%s' % (workdir, target)
    for subtarget in subtarget_default(workdir, target):
        db.ruleTable.addDeps(target_name, '%s/%s/%s' % (workdir, subtarget, target))


db.varTable.put('target/builddirs-clean', ['clean_dir', 'clean_dir2'])
db.varTable.put('target/builddirs-default', ['default', 'default2'])
db.varTable.put('target/builddirs', ['dir', 'dir2'])

db.varTable.put('target2/builddirs-clean', ['clean_dir', 'clean_dir2'])
db.varTable.put('target2/builddirs', ['dir', 'dir2'])

print(db.varTable.table)

print('<target, clean>:', subtarget_default('target', 'clean'))
print('<target, compile>:', subtarget_default('target', 'compile'))
print('<target2, clean>:', subtarget_default('target2', 'clean'))
print('<target2, compile>:', subtarget_default('target2', 'compile'))

subtarget('target', 'clean')

print(db.ruleTable.getByTarget('target/clean'))

db.ruleTable.dump()
