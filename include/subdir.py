#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import db
import os


def subtarget_default(subdir: str, target: str):
    target_key = '%s/builddirs-%s' % (subdir, target)
    default_key = '%s/builddirs-default' % subdir
    the_key = '%s/builddirs' % subdir

    scan_keys = [target_key, default_key, the_key]

    for key in scan_keys:
        if db.has_var(key):
            subtargets = []
            for subtarget in db.get_val(key):
                if subtarget is not '.':
                    subtargets.append(subtarget)
            return subtargets


def subtarget(subdir, target):
    target_name = '%s/%s' % (subdir, target)
    for subtarget in subtarget_default(subdir, target):
        db.add_prerequisites(target_name, '%s/%s/%s' % (subdir, subtarget, target))


def subdir(workdir):
    build_dirs = '%s/builddirs' % workdir

    default_subtargets = db.get_val('SUBTARGETS')
    workdir_subtargets = db.get_val('%s/subtargets' % workdir)
    subtargets = vars_join(default_subtargets, workdir_subtargets)

    for bd in db.get_val(build_dirs):
        for target in subtargets:
            pass  # 64-79

    for target in subtargets:
        subtarget(workdir, target)


def stampfile(subdir, name, target, depends, config_options='', stampfile_location=''):
    staging_dir = db.get_val('STAGING_DIR')
    tmp_dir = db.get_val('TMP_DIR')

    #   $(1)/stamp-$(3):=$(if $(6),$(6),$(STAGING_DIR))/stamp/.$(2)_$(3)$(5)
    stampfile_var = '%s/stamp-%s' % (subdir, target)
    stampfile_full = ''
    if stampfile_location is '':
        stampfile_full += staging_dir
    else:
        stampfile_full += stampfile_location
    stampfile_full += '/stamp/.%s_%s%s' % (name, target, config_options)
    db.set_var(stampfile_var, stampfile_full)

    #   $$($(1)/stamp-$(3)): $(TMP_DIR)/.build $(4)
    #       @+$(SCRIPT_DIR)/timestamp.pl -n $$($(1)/stamp-$(3)) $(1) $(4) || \
    #       $(MAKE) $(if $(QUIET),--no-print-directory) $$($(1)/flags-$(3)) $(1)/$(3)
    #       @mkdir -p $$$$(dirname $$($(1)/stamp-$(3)))
    #       @touch $$($(1)/stamp-$(3))
    db.add_prerequisites(stampfile_full, '%s/.build %s' % (tmp_dir, depends))
    db.add_recipes(stampfile_full, 'script/timestamp.pl -n %s %s %s || \\' % (stampfile_full, subdir, depends))
    make_flags_var = '%s/flags-%s' % (subdir, target)
    make_flags = db.get_val(make_flags_var)
    db.add_recipes(stampfile_full, 'make %s %s/%s # ${%s}' % (make_flags, subdir, target, make_flags_var))
    mkdir = os.path.dirname(stampfile_full)
    db.add_recipes(stampfile_full, 'mkdir %s' % mkdir)
    db.add_recipes(stampfile_full, 'touch %s' % stampfile_full)

    # TODO   $$(if $(call debug,$(1),v),,.SILENT: $$($(1)/stamp-$(3)))
    # TODO   .PRECIOUS: $$($(1)/stamp-$(3)) # work around a make bug

    #   $(1)//clean:=$(1)/stamp-$(3)/clean
    clean_var = '%s//clean' % subdir
    clean_val = '%s/stamp-%s/clean' % (subdir, target)
    db.set_var(clean_var, clean_val)

    #   $(1)/stamp-$(3)/clean: FORCE
    #       @rm -f $$($(1)/stamp-$(3))
    clean_target = '%s/clean' % stampfile_var
    db.add_prerequisites(clean_target, 'FORCE')
    db.add_recipes(clean_target, '@rm -f %s' % stampfile_full)


def vars_join(a, b):
    s = []
    if a is not None:
        s += a
    if b is not None:
        s += b
    return s


def test_subdir():
    db.reset()
    db.set_var('SUBTARGETS',
               ['clean', 'download', 'prepare', 'compile', 'update', 'refresh', 'prereq', 'dist', 'distcheck',
                'configure', 'check', 'check-depends'])
    db.set_var('target/subtargets', ['install'])
    db.set_var('target/builddirs', ['linux', 'sdk', 'imagebuilder', 'toolchain'])
    db.set_var('target/builddirs-default', ['linux'])
    db.set_var('target/builddirs-install', ['linux', 'sdk', 'imagebuilder', 'toolchain'])
    subdir('target')
    db.dump()


def test_stampfile():
    db.reset()
    db.set_var('STAGING_DIR', '$ROOT/staging_dir/target-x86_64_musl')
    db.set_var('TMP_DIR', '$ROOT/tmp')
    db.set_var('target/flags-compile', '$ROOT/tmp')
    stampfile('target', 'target', 'compile', '$ROOT/tmp/.build', '', '')
    db.dump()


if __name__ == '__main__':
    print('#### subdir ####\n')
    test_subdir()
    print('#### stampfile ####\n')
    test_stampfile()
