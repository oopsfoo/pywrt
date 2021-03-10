#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class VarTable:

    def __init__(self):
        self.table={}
    
    def hasKey(self, key):
        return key in self.table 

    def getValue(self, key):
        return self.table.get(key, None) 

    def put(self, key, value):
        self.table[key] = value 

class RuleTable:

    def __init__(self):
        self.table={}
    
    def addDeps(self, target, depTarget):
        rule = self.getByTarget(target)
        rule['deps'].append(depTarget)
    
    def getByTarget(self, target):
        if target not in self.table:
            self.table[target] = {'target': target, 'deps':[]}
        return self.table[target]

    def printRule(self, target):
        targetStr = ''
        if target in self.table:
            rule = self.table[target]
            targetStr += rule['target']
            targetStr += ':'
            for depTarget in rule['deps']:
                targetStr += ' '
                targetStr += depTarget
        print(targetStr)

    def dump(self):
        for target in self.table.keys():
            self.printRule(target)

varTable = VarTable()
ruleTable = RuleTable()
