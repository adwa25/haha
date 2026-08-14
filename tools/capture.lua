-- capture.lua
-- Safe loader that captures strings passed to load/loadstring
-- Usage: lua capture.lua main.txt
local infile = arg[1] or "main.txt"
local capture_dir = "captures"
-- create capture dir (works on *nix)
local ok = os.execute and os.execute("mkdir -p " .. capture_dir) or nil

local capture_count = 0
local function save_capture(s)
  if type(s) ~= "string" then return end
  capture_count = capture_count + 1
  local fn = string.format("%s/capture-%02d.txt", capture_dir, capture_count)
  local f = io.open(fn, "wb")
  if not f then
    io.stderr:write("Failed to open " .. fn .. "\n")
    return
  end
  f:write(s)
  f:close()
  print("Wrote", fn, "("..#s.." bytes)")
end

local function capture_loader(s, ...)
  if type(s) == "string" then
    save_capture(s)
  end
  -- Return harmless function so execution can continue without running payload
  return function() end
end

local safe_env = {
  assert = assert, error = error, ipairs = ipairs, next = next, pairs = pairs,
  pcall = pcall, xpcall = xpcall, select = select, tonumber = tonumber,
  tostring = tostring, type = type, unpack = table.unpack or unpack,
  math = math, string = string, table = table, coroutine = coroutine,
  bit32 = bit32,
  load = capture_loader,
  loadstring = capture_loader,
  loadfile = function() error("loadfile disabled in sandbox") end,
  dofile = function() error("dofile disabled in sandbox") end,
  require = function() error("require disabled in sandbox") end,
  package = {},
  os = setmetatable({}, { __index = function(_,k) error("os."..tostring(k).." disabled") end }),
  io = setmetatable({}, { __index = function(_,k) error("io."..tostring(k).." disabled") end }),
  print = function() end,
}

local chunk, err = loadfile(infile, "t", safe_env)
if not chunk then
  io.stderr:write("Failed to load file: "..tostring(err).."\n")
  os.exit(2)
end

local ok, runerr = pcall(chunk)
if not ok then
  io.stderr:write("Script ran but returned error (this can be OK): "..tostring(runerr).."\n")
else
  print("Script executed in sandbox (payloads captured, not executed).")
end

print("Done. Captures directory:", capture_dir)
