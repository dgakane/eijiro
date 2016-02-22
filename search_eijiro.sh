#!/usr/bin/env bash

EIJIRO_TEXT=~/Dropbox/eijiro/EIJI-144-utf8.TXT
# nkfなどでutf8に変換済みの英辞郎のテキストファイル
# nkf -w EIJI-144.TXT >EIJI-144-utf8.TXT

WORD=$1

grep -iE "^■$WORD" ${EIJIRO_TEXT} |  \
sed -e 's/^■//'  | \
sed -e 's/｛[^｝]*｝//g'
# 行頭の■を削除
# ふりがなを削除
