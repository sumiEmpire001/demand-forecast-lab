# C++11 companion implementation

Recursive moving-average forecasts and backtest MAE; Python handles date parsing/CSV/rounding, C++ intentionally handles only validated numeric series.

Build and test with `cmake -S . -B build && cmake --build build && ctest --test-dir build --output-on-failure`.

The original Python implementation remains unchanged; run `python -m unittest discover -s tests -v` to check it. GitHub Actions runs both suites. Input validation rejects invalid values; callers must handle exceptions and enter a safe/no-action state. This is a host-side numerical library, not calibrated sensor firmware, and has not been tested on Arduino Uno or ESP32. For embedded use, add bounded memory, watchdog behavior, sensor fault detection, electrical isolation, and board-specific drivers before operating actuators.
