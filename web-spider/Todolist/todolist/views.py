#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 14:40:22 2017

@author: xuwf
"""
from django.shortcuts import render
def todo_list(request):
    return render(request,'base.html')