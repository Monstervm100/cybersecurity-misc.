# Small Cybersecurity Projects

A collection of small educational cybersecurity demos and tools.

## Projects

### Caesar Cipher (`caesar-cipher/`)
An interactive browser-based Caesar Cipher tool. Open `caesar-cipher.html` directly in any browser — no setup needed.
- Encrypt and decrypt messages with a configurable shift (1–25)
- Live alphabet mapping preview (click to reveal)
- Copy-to-clipboard support

### Keylogger Demo (`keylogger/`)
Educational Python demos showing how keyboard and input capture works at the OS/framework level.

- **`keylogger_demo.py`** — Demonstrates tkinter keyboard event binding (`<KeyPress>` / `<KeyRelease>`). Only captures keys while the window is focused.
- **`input_capture_demo.py`** — Two-panel demo showing how `StringVar` traces in tkinter mirror input in real time.

**Requirements:** Python 3.x (tkinter is included with standard Python on Windows)

```
python keylogger_demo.py
python input_capture_demo.py
```
