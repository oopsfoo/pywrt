#!/usr/bin/env python3
# -*- coding: utf-8 -*-
var_table = {}
rule_table = {}


def has_var(var: str):
    return var in var_table


def get_val(var: str):
    return var_table.get(var, None)


def set_var(var, val):
    var_table[var] = val


def dump_all_vars():
    for var in var_table.keys():
        print('%s := %s' % (var, get_val(var)))


def empty_vars():
    global var_table
    var_table = {}


def add_rule(target: str) -> None:
    global rule_table
    rule_table[target] = {
        'target': target,
        'prerequisites': [],
        'recipes': []
    }


def rule_by_target(target: str, creat: bool = True) -> dict:
    global rule_table
    if target not in rule_table:
        if creat is False:
            return None
        add_rule(target)
    return rule_table[target]


def add_prerequisites(target: str, *prerequisites: str) -> None:
    rule = rule_by_target(target, True)
    for prerequisite in prerequisites:
        rule['prerequisites'].append(prerequisite)


def get_prerequisites(target: str) -> list:
    rule = rule_by_target(target, False)
    if rule is not None:
        return rule['prerequisites']


def add_recipes(target: str, *recipes: str) -> None:
    rule = rule_by_target(target, True)
    for recipe in recipes:
        rule['recipes'].append(recipe)


def get_recipes(target: str) -> list:
    rule = rule_by_target(target, False)
    if rule is not None:
        return rule['recipes']


def empty_rules():
    global rule_table
    rule_table = {}


def dump_rule(target: str) -> None:
    dump_str = target + ': '
    rule = rule_by_target(target, False)
    if rule is None:
        return
    for prerequisite in get_prerequisites(target):
        dump_str += prerequisite + ' '
    dump_str += '\n'
    for recipe in get_recipes(target):
        dump_str += '\t%s\n' % recipe
    print(dump_str, '\n')


def dump_rules(*targets: str) -> None:
    for target in targets:
        dump_rule(target)


def dump_all_rules():
    global rule_table
    for target in rule_table.keys():
        dump_rule(target)


def reset():
    empty_vars()
    empty_rules()


def dump():
    dump_all_vars()
    dump_all_rules()


def test_var():
    set_var('var1', 'val1')
    print('1=====================')
    print('var1 = %s' % get_val('var1'))
    print('var1 exist = %s' % has_var('var1'))
    print('var2 = %s' % get_val('var2'))
    print('var2 exist = %s' % has_var('var2'))
    print('var3 = %s' % get_val('var3'))
    print('var3 exist = %s' % has_var('var3'))
    dump_all_vars()

    set_var('var2', 'val2')
    print('2=====================')
    print('var1 = %s' % get_val('var1'))
    print('var1 exist = %s' % has_var('var1'))
    print('var2 = %s' % get_val('var2'))
    print('var2 exist = %s' % has_var('var2'))
    print('var3 = %s' % get_val('var3'))
    print('var3 exist = %s' % has_var('var3'))
    dump_all_vars()

    set_var('var3', 'var3')
    print('2=====================')
    print('var1 = %s' % get_val('var1'))
    print('var1 exist = %s' % has_var('var1'))
    print('var2 = %s' % get_val('var2'))
    print('var2 exist = %s' % has_var('var2'))
    print('var3 = %s' % get_val('var3'))
    print('var3 exist = %s' % has_var('var3'))
    dump_all_vars()

    print('ALL#####################')
    dump_all_vars()

    print('OVERWRITE#####################')
    set_var('var3', 'var4')
    dump_all_vars()

    print('CLEAR#####################')
    empty_vars()
    dump_all_vars()


def test_rule():
    add_prerequisites('target1', 'pre1', 'pre2')
    add_recipes('target1', 'do sth1', 'do sth2')
    print('1=====================')
    dump_rules('target1', 'target2', 'target3')

    add_prerequisites('target2', 'pre1', 'pre2')
    print('2=====================')
    dump_rules('target1', 'target2', 'target3')

    add_rule('target3')
    print('3=====================')
    dump_rules('target1', 'target2', 'target3')

    print('ALL#####################')
    dump_all_rules()

    print('CLEAR#####################')
    empty_rules()
    dump_all_rules()


if __name__ == '__main__':
    test_var()
    test_rule()
