# ZEXX Terminal

> A modular retro-inspired terminal environment built with Python.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Textual](https://img.shields.io/badge/Textual-8.2.8-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)

---

## 🖥️ Overview

**ZEXX Terminal** is a modular terminal environment inspired by classic DOS systems, CRT interfaces, and retro computer terminals.

The project is being built as a lightweight platform where applications can be discovered, registered, and launched automatically through a simple folder-and-manifest architecture.

The long-term goal is to turn ZEXX into a small extensible terminal ecosystem containing utilities, games, tools, themes, and eventually AI-powered features.

---

## 🚧 Current Status

ZEXX is currently in **early core development**.

The current version has moved beyond the initial project foundation and now includes:

- Application discovery
- Manifest-based application definitions
- Application registry
- Application launcher
- Textual-based terminal UI
- Keyboard-based application selection
- Application launching from the TUI
- System information utility
- Basic command architecture
- GitHub Actions CI foundation
- Retro-inspired bordered interface

The current focus is improving the core experience, performance, reliability, and preparing the project for the eventual **v1.0.0 stable release**.

---

## ✨ Current Features

### 🔎 Application Discovery

ZEXX automatically searches the `apps/` directory for application manifests.

Each application can define:

```text
name
id
category
entry