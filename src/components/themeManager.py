def setTheme(theme):
    return open(f"assets/themes/{theme}.qss", encoding='utf-8').read()