#!/usr/bin/env bash
# -*- coding: utf-8 -*-

rm -vf locales/template.ts
pylupdate6 l7z.py --no-obsolete -ts locales/template.ts
