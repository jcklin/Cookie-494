# Cookie-494
## Description

Web extension for parsing cookie banners, selecting options (allow all vs. reject all), and compiling acquired cookie results.

## Install

This project uses [selenium](https://www.selenium.dev/).

```bash
pip install selenium
```

## Usage

Collect button text

```bash
py collect_button.py
```

Collect cookies for websites listed in button_text.csv

```bash
py collect_cookie.py
```