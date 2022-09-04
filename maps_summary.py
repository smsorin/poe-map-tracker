import math

def _get_color(stat, avg):
    if stat.ratio < avg * 0.9: return "green"
    if stat.ratio > avg * 1.1: return "red"
    return "#BB0"

def BuildSummary(mapsDB):
    global_avg = mapsDB._total.ratio
    html = []
    html.append(f"""<div>Ran {mapsDB._total.runs} maps,
        died {mapsDB._total.deaths} times,
        or {mapsDB._total.deaths/mapsDB._total.runs:0.2f} deaths/map</div>""")
    for tier, data in sorted(mapsDB._tiers.items()):
        color = _get_color(data, global_avg)
        html.append("<li>")
        html.append(f"Tier {tier},")
        html.append(f"ran {data.runs} maps,")
        html.append(f"died {data.deaths} times or")
        html.append(f"<span style='color:{color}'>{data.ratio:0.2f} deaths/run</span>")
        if data.run_sec:
            avg_run_sec = sum(data.run_sec)*1.0 / len(data.run_sec)
            second, minute = math.modf(avg_run_sec/60.)
            second *= 60
            html.append(f"average runtime {minute:02.0f}:{second:02.0f}")

    html.append("<br/><br/>")
    html.append("<div>Top10 Deadliest mods</div>")
    for mod, data in sorted(mapsDB._mods.items(), key=lambda x: x[1].deaths, reverse=True)[:10]:
        html.append(f"<li>{data.runs} maps, died {data.deaths} times or {data.ratio:0.2f} deaths/run: {mod}")
    
    html.append("<br/><br/><div>(maybe)Rare deadly mods</div>")
    for mod, data in sorted(mapsDB._mods.items(), key=lambda x: x[1].ratio, reverse=True)[:10]:
        html.append(f"<li>{data.runs} maps, died {data.deaths} times or {data.ratio:0.2f} deaths/run: {mod}")
    return ' '.join(html)


