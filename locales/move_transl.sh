#!/usr/bin/env bash
# -*- coding: utf-8 -*-
for lang in de sv
do
    mkdir --parents "$lang/LC_MESSAGES/"
    for file in "${lang}"*.mo "${lang}"*.po
    do
        if [ -e "$file" ]; then
            ext="${file##*.}"
            mv -vf "$file" "$lang/LC_MESSAGES/l7z.$ext"
        fi
    done
done
