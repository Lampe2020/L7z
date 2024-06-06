#!/usr/bin/env bash
# -*- coding: utf-8 -*-
pygettext3 -k translate -d l7z ./*.py
mv -vf l7z.pot locales/template.pot