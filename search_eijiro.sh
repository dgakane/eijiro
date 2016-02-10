#!/usr/bin/env bash                                                                                                    

EIJIRO_TEXT=./EIJI-144-utf8.TXT
# nkfなどでutf8に変換済みの英辞郎のテキストファイル
# nkf -w EIJI-144.TXT >EIJI-144-utf8.TXT

WORD=$1

grep -iE "^■$WORD" ${EIJIRO_TEXT} |  \
sed -e 's/^■//'  | \ # 行頭の■を削除
sed -e 's/｛[^｝]*｝//g' # ふりがなを削除
