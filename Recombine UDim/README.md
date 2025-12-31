Recombine UDim

Minimal scaffold for a Substance Painter plugin that:
- Calls the programmatic export API (`substance_painter.export`) to export per-textureset maps.
- Uses `substance_painter.textureset` to detect UDIM tiles.
- Recombines exported images per UDIM tile into single UDIM images (recomposition implementation pending).

Files:
- plugins/recombine_udim.py — plugin entry
- modules/recombine_udim/recombine_manager.py — core logic (skeleton)
- modules/recombine_udim/ui_manager.py — minimal UI dock widget

Next steps:
- Implement JSON config handling and export orchestration.
- Implement image recomposition using Pillow or OpenImageIO inside Painter (verify availability).
- Add progress/events handling and error reporting.
