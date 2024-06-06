#!/usr/bin/env bash
# -*- coding: utf-8 -*-
pygettext3 -d l7z ./*.py
mv -vf l7z.pot locales/template.pot