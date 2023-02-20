#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json

parser = argparse.ArgumentParser(description=' =: Generate Match and Replace BurpSuite Options :=')
parser.add_argument('-f', '--file', help='Parameters/Variables to be Matched', dest='file')
parser.add_argument('-c', '--comment', help='Comment or Bug Class [SSRF, RCE, XSS ..etc]', dest='comment')
parser.add_argument('-r', '--rule', help='Rule Type [request_header,request_body ...etc]', dest='rule')
parser.add_argument('-s', '--replace', help='Literal String to Replace', dest='replace')
parser.add_argument('-x', '--tmp',action="store_true",default=False, help='replace with regex and add a temp var', dest='regrep')
parser.add_argument('-o', '--output', help='Option JSON file', dest='output')
args = parser.parse_args()

params = str(args.file)
comment = str(args.comment)
rule = str(args.rule)
replace = str(args.replace)
output = str(args.output)
tmp = args.regrep
 
def matchReplace(func):
    obj = { "proxy":{
            "match_replace_rules":
                func
            
        }
    }
    return(json.dumps(obj,indent=4, sort_keys=True))



def innerReplace(param, comment, rule, replace):
    mObj = []
    try:
        param = open(param,'r')
        for par in param:
            if tmp:
                mObj.append({
                            "comment":""+comment+"",
                            "enabled":True,
                            "is_simple_match":False,
                            "rule_type":""+rule+"",
                            "string_match":"^"+par.strip()+".*$",
                            "string_replace":""+par.strip()+"="+par.strip()+"."+replace+"&tmp"
                        })
            else:
                mObj.append({
                        "comment":""+comment+"",
                        "enabled":True,
                        "is_simple_match":True,
                        "rule_type":""+rule+"",
                        "string_match":""+par.strip()+"",
                        "string_replace":""+par.strip()+"."+replace+""
                    })
    except:
        parser.print_help()

    return(mObj)


iCall = innerReplace(params,comment,rule,replace)
mCall = matchReplace(iCall)

with open(output,'w') as output_file:
    output_file.write(mCall)
