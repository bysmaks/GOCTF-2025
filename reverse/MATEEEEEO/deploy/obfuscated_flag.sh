#!/bin/bash

read -p "Enter key: " f
read -p "Enter shift: " s
[[ -z "$f" || -z "$s" ]] && exit 1

enc=""
for ((i=0;i<${#f};i++)); do
  c="${f:$i:1}"
  o=$(printf "%d" "'$c")
  o=$((o+s))
  enc+=$(printf "\\$(printf '%03o' "$o")")
done

b64=$(echo -n "$enc" | base64)

ref="Wmluc2luc2luc2l6c2RUV2R5enNseXpzbFlaU0xZWlNMeXpzbFlaU0x5enNseXpzbFlaU0xYZm16dw=="

if [ "$b64" = "$ref" ]; then
  echo "correct. This is the key to get the flag"
else
  echo "wrong"
fi
