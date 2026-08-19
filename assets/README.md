# Source art assets (not shipped directly)

Drop original, full-resolution images here. The build scripts in `../tools/` convert them into the
formats HOI4 needs.

## Flags — needed by `tools/make_flags.ps1`

Save the flag images here with these exact base names (any image extension works — png/jpg/bmp):

| File | Becomes flag for |
|------|------------------|
| `nusa.png` | NUS — New United States of America |
| `ussr.png` | USR — Union of Sovereign Soviet Republics |

Then run from the repo root:

```
& ".\tools\make_flags.ps1"
```

It generates `NUS.tga` and `USR.tga` at 82×52, 41×26, and 10×7 into `mod/gfx/flags/`,
`mod/gfx/flags/medium/`, and `mod/gfx/flags/small/`.
