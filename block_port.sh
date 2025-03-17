#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "error: insufficient arguments"
    echo "usage: "
    echo "./block_port.sh <port>"
    exit 1
fi

trap "rm ./block.py -f" SIGINT

encodeCmd="aW1wb3J0IHNvY2tldApkZWYgYmxvY2tfdWRwX3BvcnQocG9ydCk6CiAgICBzZXJ2ZXJfc29ja2V0ID0gc29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCwgc29ja2V0LlNPQ0tfREdSQU0pCiAgICBzZXJ2ZXJfc29ja2V0LnNldHNvY2tvcHQoc29ja2V0LlNPTF9TT0NLRVQsIHNvY2tldC5TT19SRVVTRUFERFIsIDEpCiAgICB0cnk6CiAgICAgICAgc2VydmVyX3NvY2tldC5iaW5kKCgiMC4wLjAuMCIsIHBvcnQpKQogICAgICAgIHByaW50KGYiWytdVURQIFBvcnQge3BvcnR9IGlzIG5vdyBibG9ja2VkIikKICAgICAgICB3aGlsZSBUcnVlOgogICAgICAgICAgICBkYXRhLCBhZGRyID0gc2VydmVyX3NvY2tldC5yZWN2ZnJvbSgxMDI0KQogICAgICAgICAgICBwcmludChmIlsrXUNvbm5lY3Rpb24gYXR0ZW1wdCBmcm9tIHthZGRyfSBibG9ja2VkIHdpdGggZGF0YToge2RhdGF9IikKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICBwcmludChmIlstXUZhaWxlZCB0byBiaW5kIHRvIFVEUCBwb3J0IHtwb3J0fToge2V9IikKaWYgX19uYW1lX18gPT0gIl9fbWFpbl9fIjoKICAgIGJsb2NrX3VkcF9wb3J0KGZsNGcp"
echo $encodeCmd | base64 -d > block.py

port=$1
sed -i "s/fl4g/$port/g" ./block.py
chmod +x block.py

python3 block.py
