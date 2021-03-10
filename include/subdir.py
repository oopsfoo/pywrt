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


def stampfile(subdir, name, target, depends, config_options, stampfile_location):
    staging_dir = db.varTable.getValue('STAGING_DIR')
    tmp_dir = db.varTable.getValue('TMP_DIR')

    #   $(1)/stamp-$(3):=$(if $(6),$(6),$(STAGING_DIR))/stamp/.$(2)_$(3)$(5)
    stamp_var = '%s/stamp-%s' % (subdir, target)
    stamp_val = ''
    if stampfile_location is '':
        stamp_val += staging_dir
    else:
        stamp_val += stampfile_location
    stamp_val += '/stamp/.%s_%s%s' % (name, target, config_options)
    db.varTable.put(stamp_var, stamp_val)

    #   $$($(1)/stamp-$(3)): $(TMP_DIR)/.build $(4)
    #       @+$(SCRIPT_DIR)/timestamp.pl -n $$($(1)/stamp-$(3)) $(1) $(4) || \
    #       $(MAKE) $(if $(QUIET),--no-print-directory) $$($(1)/flags-$(3)) $(1)/$(3)
    #       @mkdir -p $$$$(dirname $$($(1)/stamp-$(3)))
    #       @touch $$($(1)/stamp-$(3))
    db.ruleTable.addDeps(stamp_val, '%s/.build %s' % (tmp_dir, depends))
    #TODO db.ruleTable.addCmds(clean_target, 'script/timestamp.pl' )
    #TODO db.ruleTable.addCmds(clean_target, 'make' )
    #TODO db.ruleTable.addCmds(clean_target, 'mkdir' )
    #TODO db.ruleTable.addCmds(clean_target, 'touch' )

    #TODO   $$(if $(call debug,$(1),v),,.SILENT: $$($(1)/stamp-$(3)))
    #TODO   .PRECIOUS: $$($(1)/stamp-$(3)) # work around a make bug 
    
    #   $(1)//clean:=$(1)/stamp-$(3)/clean
    clean_var = '%s//clean' % subdir
    clean_val = '%s/stamp-%s/clean' % (subdir, target)
    db.varTable.put(clean_var, clean_val)

    #   $(1)/stamp-$(3)/clean: FORCE
    #       @rm -f $$($(1)/stamp-$(3))
    clean_target = '%s/clean' % stamp_var
    db.ruleTable.addDeps(clean_target, 'FORCE')
    #TODO db.ruleTable.addCmds(clean_target, '@rm -f %s' %)


def vars_join(a, b):
    s = []
    if a is not None:
        s += a
    if b is not None:
        s += b
    return s

def test_subdir():
    db.varTable.reset()
    db.ruleTable.reset()
    db.varTable.put('SUBTARGETS', ['clean', 'download', 'prepare', 'compile', 'update', 'refresh', 'prereq', 'dist', 'distcheck', 'configure', 'check', 'check-depends'])
    db.varTable.put('target/subtargets', ['install'])
    db.varTable.put('target/builddirs', ['linux', 'sdk', 'imagebuilder', 'toolchain'])
    db.varTable.put('target/builddirs-default', ['linux'])
    db.varTable.put('target/builddirs-install', ['linux', 'sdk', 'imagebuilder', 'toolchain'])
    subdir('target')
    db.ruleTable.dump()

def test_stampfile():
    db.varTable.reset()
    db.ruleTable.reset()
    db.varTable.put('STAGING_DIR', '$ROOT/staging_dir/target-x86_64_musl')
    db.varTable.put('TMP_DIR', '$ROOT/tmp')
    stampfile('target', 'target', 'compile', 'tmp/.build', '', '')
    db.varTable.dump()
    print('---------------------------')
    db.ruleTable.dump()

if __name__ == '__main__':
    print('#### subdir ####\n')
    test_subdir()
    print('#### stampfile ####\n')
    test_stampfile()
