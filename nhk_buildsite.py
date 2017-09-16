#!/usr/bin/env python3

import sqlite3
from jinja2 import Template

def classify(percent):
    if percent >= 90:
        return "green"
    elif percent >= 50:
        return "blue"
    else:
        return "red"

def get_data():
    conn = sqlite3.connect('nhk_stats.db')
    c = conn.cursor()
    rows = c.execute("select url, level, percent from nhk_stats order by percent desc")
    dicks = [{ "url": row[0], "level": row[1], "percent": row[2], "color": classify(row[2]) } for row in rows]
    conn.close()
    return dicks

data = get_data()

for i in range(1, 61):
    template = Template(open("static-site/template.jinja").read())
    out = template.render(
        lines=[row for row in data if row["level"] == i],
        level=i
    )
    open("static-site/level/%s.html" % i, "w").write(out)
