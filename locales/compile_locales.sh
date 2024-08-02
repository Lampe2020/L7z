#!/usr/bin/env bash
# -*- coding: utf-8 -*-

for file in *.ts; do
    lrelease "$file"
done