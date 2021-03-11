#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import db
from include import subdir as subdir

# curdir:=target
# $(curdir)/subtargets:=install
# $(curdir)/builddirs:=linux sdk imagebuilder toolchain
# $(curdir)/builddirs-default:=linux
# $(curdir)/builddirs-install:=linux $(if $(CONFIG_SDK),sdk) $(if $(CONFIG_IB),imagebuilder) $(if $(CONFIG_MAKE_TOOLCHAIN),toolchain)
curdir = 'target'
db.set_var('target/subtargets', ['install'])
db.set_var('target/builddirs', ['linux', 'sdk', 'imagebuilder', 'toolchain'])
db.set_var('target/builddirs-default', ['linux'])

# TODO check vars
db.set_var('target/builddirs-install', ['linux', 'sdk', 'imagebuilder', 'toolchain'])

# $(curdir)/sdk/install:=$(curdir)/linux/install
# $(curdir)/imagebuilder/install:=$(curdir)/linux/install
db.set_var('target/sdk/install', 'target/linux/install')
db.set_var('target/imagebuilder/install', 'target/linux/install')

# $(eval $(call stampfile,$(curdir),target,prereq,.config))
subdir.stampfile('target', 'target', 'prereq', '.config')
# $(eval $(call stampfile,$(curdir),target,compile,$(TMP_DIR)/.build))
subdir.stampfile('target', 'target', 'compile', '%s/.build' % db.get_val("TMP_DIR"))
# $(eval $(call stampfile,$(curdir),target,install,$(TMP_DIR)/.build))
subdir.stampfile('target', 'target', 'install', '%s/.build' % db.get_val("TMP_DIR"))

# 14 $($(curdir)/stamp-install): $($(curdir)/stamp-compile)

# 16 $(eval $(call subdir,$(curdir)))
subdir.subdir('target')

def info():
    pass
