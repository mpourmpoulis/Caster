import json
import os

from copy import deepcopy

from dragonfly import (MappingRule, Choice, Dictation, Grammar,Repeat, Function,RunCommand,FocusWindow)
from dragonfly import *

from castervoice.lib import settings, utilities, context, contexts
from castervoice.lib.actions import Key, Text
from castervoice.lib.const import CCRType
from castervoice.lib.context import AppContext
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

from castervoice.lib.sublime import send_sublime,SublimeCommand
from castervoice.lib.sublime_snippets import Snippet,SnippetVariant,DisplaySnippetVariants,snippet_state

from castervoice.lib.sublime_snippets_additional import grammars_with_snippets



initial = {
        "variant <n>":
            R(Key("c-z") + SnippetVariant(n="n")),
        "display variants":
            R(Key("c-z") + DisplaySnippetVariants()),
}

# 941
# global controll grammar WIP
#


last_keys = set()
last_rule = None

class SublimeSnippetAdditionalControllRule(BaseSelfModifyingRule):
    pronunciation = "sublime snippet additional control"
    observer = None
    last = None
    def __init__(self, *args, **kwargs):
        def printr(*args):
            print(args)
        SublimeSnippetAdditionalControllRule.last = self 
        super(SublimeSnippetAdditionalControllRule, self).__init__(os.path.join(settings.SETTINGS["paths"]["USER_DIR"],"nothing.toml"),"sublime snippet additional control")


    def _deserialize(self):
        self._smr_mapping = initial.copy()
        self._smr_extras =  [IntegerRefST("n",1,10)]
        self._smr_defaults =  {}

        names = snippet_state["extra_data"].keys()
        if last_rule:
            # print(grammars_with_snippets[last_rule])
            for e in grammars_with_snippets[last_rule]:
                if isinstance(e,Choice) and e.name in names:
                    self._smr_mapping["variant <"+e.name+">"] = R(Key("c-z") + SnippetVariant(**{e.name:e.name}))
                    self._smr_extras.append(e)
        print(self._smr_mapping)

    
    def _refresh(self,rule = None,*args):
        # print("The refreshing snippets",snippet_state)
        global last_keys,last_rule
        if type(rule) not in grammars_with_snippets:
            # print(rule,grammars_with_snippets.keys())
            return 
        if last_keys == set(snippet_state["extra_data"].keys()) and type(rule)==last_rule:
            return 0
        else:
            # Text("refreshed").execute()
            last_keys = set(snippet_state["extra_data"].keys())
            last_rule = type(rule)
            self.reset()
        # self.reset()try : 
#dear
#---------------------------------------------------------------------------std::cerr<<  << " " <<  << " " <<  << std::endl;
refresh_after_command_callback = lambda words,rule: SublimeSnippetAdditionalControllRule.last._refresh(rule) if SublimeSnippetAdditionalControllRule.last else None
# refresh_after_command_callback = lambda words,rule:SublimeSnippetAdditionalControllRule.last._refresh() if SublimeSnippetAdditionalControllRule.last else None

# this is not working
if SublimeSnippetAdditionalControllRule.observer:
    print("disaster")
    print(SublimeSnippetAdditionalControllRule.observer)
    SublimeSnippetAdditionalControllRule.observer.unregister()


SublimeSnippetAdditionalControllRule.observer = register_post_recognition_callback(refresh_after_command_callback)



def get_rule():
    return SublimeSnippetAdditionalControllRule, RuleDetails(ccrtype=CCRType.SELFMOD, executable=["sublime_text"])
    

    

    
