# Deobfuscation tools for main.txt/main.lua

This branch adds two helper scripts to safely capture and pre-decode payloads from obfuscated Lua code without executing potentially malicious payloads.

Files added:
- tools/capture.lua  -- sandbox loader; run: lua tools/capture.lua main.txt
- tools/deobf.py     -- post-processing/decoding helper; run: python3 tools/deobf.py captures/capture-01.txt > captures/capture-01.decoded.lua

Quick steps for the owner:
1) Clone repo and checkout this branch:
   git fetch origin deobf-tools && git checkout -b deobf-tools origin/deobf-tools
2) Run the capture (recommended in an offline VM):
   lua tools/capture.lua main.txt
3) Decode the first capture:
   python3 tools/deobf.py captures/capture-01.txt > captures/capture-01.decoded.lua
4) Upload the decoded file and paste the transfer.sh link here, or open an issue/PR with the file attached and I will finish deobfuscation and produce main-deobf.lua for you.

If you want, I can also create a Pull Request that adds the fully deobfuscated file once you upload the decoded capture here or give me permission to fetch and process public raw files. If you prefer I process the raw file directly, tell me and I'll proceed (I will not execute the file; only static decoding).
