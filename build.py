#!/usr/bin/env python3
"""Fitstack generator v2 — data-rich, AEO-optimized static pages."""
import json, os, re, html, datetime

ROOT=os.path.dirname(os.path.abspath(__file__))
DATA=os.path.join(ROOT,"data","gym_software.json")
OUT=os.path.join(ROOT,"site")
BRAND="GymSoftwareHQ"; DOMAIN="gymsoftwarehq.com"
YEAR=datetime.date.today().year
os.makedirs(OUT,exist_ok=True)

def esc(s): return html.escape(str(s)) if s is not None else ""
def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
D=json.load(open(DATA,encoding="utf-8"))
TOOLS=[t for t in D["tools"] if t.get("name")]
BY={t["slug"]:t for t in TOOLS}
SUB=D["sub_niches_for_best_for_pages"]

CSS=""":root{--bg:#0b1220;--card:#131c2e;--ink:#e8edf6;--muted:#9fb0c8;--accent:#3ba3ff;--good:#2ec26b;--warn:#ffb020;--line:#243247}
*{box-sizing:border-box}body{margin:0;font:16px/1.68 -apple-system,Segoe UI,Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink)}
.wrap{max-width:820px;margin:0 auto;padding:26px 20px 80px}header.site{border-bottom:1px solid var(--line);background:#0a101c}
header.site .wrap{padding:14px 20px;display:flex;justify-content:space-between;align-items:center}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:29px;line-height:1.25;margin:.2em 0 .3em}h2{font-size:21px;margin:1.7em 0 .5em;border-left:3px solid var(--accent);padding-left:10px}
h3{font-size:17px;margin:1.2em 0 .3em}.sub{color:var(--muted);font-size:18px;margin-bottom:8px}
p{margin:.7em 0}.disclosure{font-size:13px;color:var(--muted);background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:14px 0}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
th{background:#0f1727;color:var(--accent)}tr:nth-child(even) td{background:#0e1524}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:15px 17px;margin:13px 0}
.badge{display:inline-block;font-size:12px;padding:2px 8px;border-radius:20px;border:1px solid var(--line);margin:2px 4px 2px 0;color:var(--muted)}
.badge.rec{color:var(--good);border-color:#1c5b38}.badge.bounty{color:var(--warn);border-color:#5b481c}
.cta{display:block;background:linear-gradient(90deg,#1b6fd6,#3ba3ff);color:#fff;font-weight:600;text-align:center;padding:12px;border-radius:10px;margin:10px 0}
.cta:hover{text-decoration:none;filter:brightness(1.08)}.complaint{color:#ffd7d7}.muted{color:var(--muted)}
ul{padding-left:20px}li{margin:4px 0}.method{font-size:14px;color:var(--muted);border-top:1px dashed var(--line);margin-top:26px;padding-top:12px}
.related{background:#0f1727;border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:18px 0}
footer{border-top:1px solid var(--line);margin-top:36px;color:var(--muted);font-size:13px}"""

DISC='<div class="disclosure">Disclosure: some links are affiliate links — if you sign up through them we may earn a commission at no cost to you. Rankings are based on features, real pricing, and aggregated owner feedback, never payout size.</div>'
METHOD=f'<p class="method"><strong>How we research:</strong> {BRAND} compiles published pricing, feature sets, and recurring themes from public owner reviews and community discussions (Reddit, G2, Capterra). Pricing changes often — figures were last checked {D["_meta"]["last_verified"]}; always confirm on the vendor site before buying.</p>'

def price(t):
    if t.get("price_min_month") is not None and t.get("price_max_month"):
        lo=t["price_min_month"]; return (f"${lo}–${t['price_max_month']}/mo" if lo else f"free–${t['price_max_month']}/mo")
    return t.get("price_note","Quote-based")
def badge(t):
    a=t.get("affiliate",{}).get("type")
    return '<span class="badge rec">recurring commission</span>' if a=="recurring" else ('<span class="badge bounty">signup bounty</span>' if a=="bounty" else "")
def cta(t):
    aff=t.get("affiliate_link")
    if aff:
        return f'<a class="cta" href="{esc(aff)}" rel="sponsored nofollow">Check {esc(t["name"])} pricing &amp; book a free demo →</a>'
    web=t.get("website")
    if web:
        return f'<a class="cta" href="{esc(web)}" rel="nofollow" target="_blank">Visit {esc(t["name"])} &amp; check current pricing →</a>'
    return ''
def faq_ld(qas): return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}
def shell(title,desc,body,ld=None):
    s=f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="icon" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTUiIGZpbGw9IiMwZjE4MzAiLz48dGV4dCB4PSIzMiIgeT0iNDUiIGZvbnQtZmFtaWx5PSJEZWphVnUgU2FucyIgZm9udC1zaXplPSIzMyIgZm9udC13ZWlnaHQ9IjcwMCIgZmlsbD0iIzNiYTNmZiIgdGV4dC1hbmNob3I9Im1pZGRsZSI+SFE8L3RleHQ+PC9zdmc+"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="https://{DOMAIN}/{slug(title)}.html"><style>{CSS}</style>{s}</head><body>
<header class="site"><div class="wrap"><a href="index.html" style="font-weight:800;letter-spacing:2px;font-size:19px;color:#e8edf6;text-decoration:none">GYMSOFTWARE<span style="color:#3ba3ff">HQ</span></a><a href="finder.html" style="color:var(--accent);font-weight:600">&#128269; Find your software</a> <span class="muted">· {YEAR}</span></div></header>
<main class="wrap">{body}<footer>© {YEAR} {BRAND}. Independent — not affiliated with any vendor. · <a href="about.html">About</a> · <a href="affiliate-disclosure.html">Disclosure</a> · <a href="privacy-policy.html">Privacy</a></footer></main></body></html>'''

def cost_para(t):
    rn=t.get("real_spend_note")
    base=f"{t['name']}'s published pricing starts around {price(t)}."
    if rn: base+=f" But the number that hits your bank account is usually higher: {rn}. Budget for that gap, not the sticker price."
    return base
def complaint_para(t):
    cs=t.get("common_complaints",[])
    if not cs: return f"{t['name']} draws relatively few recurring complaints in the owner discussions we reviewed — a point in its favour."
    return f"The recurring gripes owners raise about {t['name']}: " + ", ".join(cs) + ". Weigh these against your own priorities before committing to an annual contract."
def fit_line(t): return ", ".join(t.get("best_for",[])) or t.get("target_segment","—")

# related best-for links for a tool
def related_for(t):
    links=[sn for sn in SUB if any(sn.split()[0].lower() in b.lower() for b in t.get("best_for",[]))][:3]
    if not links: return ""
    items="".join(f'<li><a href="{slug("Best gym software for "+sn+" ("+str(YEAR)+")")}.html">Best software for {esc(sn)}</a></li>' for sn in links)
    return f'<div class="related"><strong>Related guides:</strong><ul>{items}</ul></div>'

pages=[]
def add(title,desc,body,ld=None): pages.append((title,shell(title,desc,body,ld)))

# ---- VS ----
def vs(a,b,sn=None):
    ta,tb=BY[a],BY[b]; focus=f" for {sn}" if sn else ""
    title=f"{ta['name']} vs {tb['name']}{focus} ({YEAR})"
    desc=f"{ta['name']} vs {tb['name']}: real pricing, hidden costs, who each fits, and what owners complain about{focus}. Independent {YEAR} comparison."
    rows=[("Starting price",price(ta),price(tb)),("Real-world cost",ta.get("real_spend_note","—"),tb.get("real_spend_note","—")),
          ("Best for",fit_line(ta),fit_line(tb)),("Segment",ta.get("target_segment","—"),tb.get("target_segment","—")),
          ("Affiliate/referral",ta.get("affiliate",{}).get("terms","—"),tb.get("affiliate",{}).get("terms","—"))]
    table="<table><tr><th>Criterion</th><th>%s</th><th>%s</th></tr>%s</table>"%(esc(ta['name']),esc(tb['name']),"".join(f"<tr><td>{esc(c)}</td><td>{esc(x)}</td><td>{esc(y)}</td></tr>" for c,x,y in rows))
    body=f'''<h1>{esc(title)}</h1><p class="sub">{esc(desc)}</p>{DISC}
<p>If you run {esc(sn or "a gym or studio")}, the choice between {esc(ta["name"])} and {esc(tb["name"])} usually comes down to price transparency and workflow fit. We put the two side by side on the factors that actually decide the monthly bill.</p>
{table}
<h2>Real cost, not sticker price</h2><p>{esc(cost_para(ta))}</p><p>{esc(cost_para(tb))}</p>
<h2>What owners actually complain about</h2><h3>{esc(ta["name"])}</h3><p class="complaint">{esc(complaint_para(ta))}</p><h3>{esc(tb["name"])}</h3><p class="complaint">{esc(complaint_para(tb))}</p>
<h2>Which should you choose{esc(focus)}?</h2>
<div class="card"><strong>Choose {esc(ta["name"])}</strong> {badge(ta)}<br>if you match: {esc(fit_line(ta))}. Starting {esc(price(ta))}.{cta(ta)}</div>
<div class="card"><strong>Choose {esc(tb["name"])}</strong> {badge(tb)}<br>if you match: {esc(fit_line(tb))}. Starting {esc(price(tb))}.{cta(tb)}</div>
{related_for(ta)}{METHOD}'''
    qas=[(f"Is {ta['name']} or {tb['name']} cheaper?",f"{ta['name']} starts at {price(ta)}; {tb['name']} at {price(tb)}. Real spend is often higher once payment processing and add-ons are included."),
         (f"Which is better for {sn or 'small gyms'}?",f"For {sn or 'small gyms'}: {ta['name']} suits {fit_line(ta)}; {tb['name']} suits {fit_line(tb)}."),
         (f"Do {ta['name']} and {tb['name']} lock you into a contract?",f"Check current terms on each vendor's site — annual contracts and setup fees are common in this category and are a frequent source of owner frustration.")]
    add(title,desc,body,faq_ld(qas))

# ---- BEST FOR ----
def best_for(sn):
    title=f"Best gym software for {sn} ({YEAR})"
    desc=f"The best gym/studio software for {sn} in {YEAR}, ranked by workflow fit, real pricing, and owner-reported issues. Independent comparison."
    picks=[t for t in TOOLS if any(sn.split()[0].lower() in b.lower() or sn.lower() in b.lower() for b in t.get("best_for",[]))]
    if len(picks)<3: picks=(picks+[t for t in TOOLS if t.get("role","").startswith("alternative") and t not in picks])[:4]
    rows="".join(f"<tr><td><strong>{esc(t['name'])}</strong> {badge(t)}</td><td>{esc(price(t))}</td><td>{esc(fit_line(t))}</td></tr>" for t in picks)
    cards="".join(f'<div class="card"><h3>{esc(t["name"])} {badge(t)}</h3><p class="muted">{esc(price(t))} · fits {esc(fit_line(t))}</p><p>{esc(complaint_para(t))}</p>{cta(t)}</div>' for t in picks)
    body=f'''<h1>{esc(title)}</h1><p class="sub">{esc(desc)}</p>{DISC}
<p>Running {esc(sn)} puts demands on scheduling, billing and member management that generic gym software often handles badly. We compared the platforms owners in this space actually use and ranked them on fit and real cost.</p>
<table><tr><th>Tool</th><th>Price</th><th>Best for</th></tr>{rows}</table>
<h2>Top picks for {esc(sn)}</h2>{cards}
<h2>How much should you budget?</h2><p>For {esc(sn)}, expect anywhere from around $20/mo for a lean solo tool to $400+/mo for a full class-based platform. The trap is the difference between the quoted base price and real spend — payment-processing markups, marketplace commissions and paid add-ons routinely push the true cost well above the headline figure.</p>
{METHOD}'''
    qas=[(f"What is the best software for {sn}?",f"For {sn}, the strongest fits are {', '.join(t['name'] for t in picks[:3])}, chosen on workflow fit and real pricing."),
         (f"How much does software for {sn} cost?","Roughly $20–$400+/month depending on size and features; watch for processing markups and add-ons on top of the base price."),
         (f"Is there free gym software for {sn}?","Some tools (e.g. WodGuru) are free below a small member count, then charge per member — viable for very small operations.")]
    add(title,desc,body,faq_ld(qas))

# ---- PRICING ----
def pricing(t):
    title=f"{t['name']} pricing {YEAR} — real costs and fees"
    desc=f"{t['name']} pricing for {YEAR}: published tiers, the fees that inflate the real bill, who it fits, and cheaper alternatives."
    alts=[x for x in TOOLS if x["slug"]!=t["slug"] and x.get("role","").startswith("alternative")][:3]
    ar="".join(f"<tr><td>{esc(x['name'])}</td><td>{esc(price(x))}</td><td>{esc(fit_line(x))}</td></tr>" for x in alts)
    body=f'''<h1>{esc(title)}</h1><p class="sub">{esc(desc)}</p>{DISC}
<div class="card"><strong>Starting price:</strong> {esc(price(t))}<br><strong>Real-world cost:</strong> {esc(t.get("real_spend_note","varies by size and add-ons"))}<br><strong>Best for:</strong> {esc(fit_line(t))}</div>
<h2>What you'll actually pay</h2><p>{esc(cost_para(t))}</p>
<h2>What owners complain about</h2><p class="complaint">{esc(complaint_para(t))}</p>
<h2>Cheaper alternatives to {esc(t['name'])}</h2><table><tr><th>Alternative</th><th>Price</th><th>Best for</th></tr>{ar}</table>
{cta(t)}{related_for(t)}{METHOD}'''
    qas=[(f"How much does {t['name']} cost?",f"{t['name']} starts at {price(t)}. {t.get('real_spend_note','')}".strip()),
         (f"Does {t['name']} have hidden fees?","Common extras in this category include payment-processing markups, setup/onboarding fees and paid add-ons — always ask for an all-in quote."),
         (f"What are the best {t['name']} alternatives?",f"Worth comparing: {', '.join(x['name'] for x in alts)}.")]
    add(title,desc,body,faq_ld(qas))

for a,b,sn in [("mindbody","pushpress","CrossFit boxes"),("mindbody","zen-planner",None),("pushpress","wodify","CrossFit boxes"),
               ("zen-planner","gymdesk","martial arts gyms"),("mindbody","glofox","boutique studios"),("glofox","mariana-tek","boutique studios"),
               ("mindbody","clubready","multi-location gyms"),("zen-planner","kicksite","martial arts gyms"),("wodify","wodguru","CrossFit boxes"),("teamup","gymcatch","small class studios")]:
    if a in BY and b in BY: vs(a,b,sn)
for sn in SUB: best_for(sn)
for t in TOOLS: pricing(t)

# index + privacy + disclosure pages
links="".join(f'<li><a href="{slug(tt)}.html">{esc(tt)}</a></li>' for tt,_ in pages)
add(f"{BRAND} — Independent gym software comparisons","Compare gym and studio management software on real pricing and owner feedback.",
    f"<h1>{BRAND}</h1><p class='sub'>Independent gym &amp; studio software comparisons — real pricing, real owner feedback, no vendor spin.</p><p>We help gym and studio owners cut through opaque pricing and marketing claims. Every guide is built from published pricing and aggregated owner reviews.</p><h2>All guides ({len(pages)})</h2><ul>{links}</ul><p class='muted'><a href='about.html'>About</a> · <a href='affiliate-disclosure.html'>Affiliate disclosure</a> · <a href='privacy-policy.html'>Privacy policy</a></p>")
add("Affiliate disclosure","How GymSoftwareHQ makes money and how that affects our rankings.",
    f"<h1>Affiliate disclosure</h1><p>{BRAND} is reader-supported. Some outbound links to software vendors are affiliate or referral links, meaning we may earn a commission or bounty if you sign up through them — at no additional cost to you.</p><p>This never changes our rankings. We rank tools on features, real pricing and aggregated owner feedback, not on how much a vendor pays. Where a tool has no affiliate program, we still include it if it's the right fit. In line with FTC guidance, affiliate links are marked and this disclosure appears on every guide.</p>")
add("Privacy policy",f"{BRAND} privacy policy.",
    f"<h1>Privacy policy</h1><p>{BRAND} does not collect personal information beyond standard, anonymised web analytics used to understand which guides are useful. We do not sell data. Outbound affiliate links may set cookies governed by the destination vendor's own privacy policy. Questions: contact us via the site.</p>")

about_body=("<h1>About GymSoftwareHQ</h1>"
"<p class='sub'>Independent gym &amp; studio software comparisons — real pricing, no vendor spin.</p>"
"<p>GymSoftwareHQ is an independent resource that helps gym, studio and boutique-fitness owners choose management software without the marketing fog. Pricing in this category is notoriously opaque — quoted rates balloon once payment processing, marketplace commissions and paid add-ons stack up. We exist to surface the real numbers.</p>"
"<h2>How we research</h2>"
"<p>Every guide is built from published vendor pricing, feature sets, and recurring themes in public owner reviews and community discussions (Reddit, G2, Capterra). We note when figures were last checked and always tell you to confirm on the vendor site before buying, because prices change often.</p>"
"<h2>How we stay independent</h2>"
"<p>Some outbound links are affiliate or referral links, meaning we may earn a commission or bounty if you sign up through them — at no extra cost to you. This never changes our rankings: we rank tools on features, real pricing and aggregated owner feedback, never on payout size. Tools with no affiliate program are still included when they fit. See our <a href='affiliate-disclosure.html'>affiliate disclosure</a>.</p>"
"<h2>Contact</h2>"
"<p>Questions, corrections, or a pricing update we missed? Email <a href='mailto:liwjjangs@gmail.com'>liwjjangs@gmail.com</a>.</p>")
add("About","About GymSoftwareHQ — who we are, how we research gym software, and how we stay independent.",about_body)

for title,h in pages:
    fn="index.html" if title.startswith(BRAND) else slug(title)+".html"
    open(os.path.join(OUT,fn),"w",encoding="utf-8").write(h)
print(f"Generated {len(pages)} pages")


# --- interactive software finder ---
def _fprice(t):
    lo=t.get("price_min_month"); hi=t.get("price_max_month")
    if lo is not None and hi:
        return ("free" if lo==0 else "$%d"%lo)+"-$%d/mo"%hi
    return t.get("price_note","Quote-based")
_fdata=[]
for t in TOOLS:
    link = t.get("affiliate_link") or (slug(t["name"]+" pricing "+str(YEAR)+" - real costs and fees")+".html")
    _fdata.append({"name":t["name"],"price":_fprice(t),"pmin":(t.get("price_min_month") if t.get("price_min_month") is not None else 200),
        "best_for":[b.lower() for b in t.get("best_for",[])],"seg":(t.get("target_segment") or "").lower(),
        "complaints":[c.lower() for c in t.get("common_complaints",[])],"note":t.get("real_spend_note",""),
        "aff":bool(t.get("affiliate_link")),"link":link})
_fjson=json.dumps(_fdata)
_ftitle="Gym software finder - find the right tool for your studio (%d)"%YEAR
_fdesc="Answer 3 questions and get matched to the best gym or studio software for your business type, size, and priorities. Free interactive tool."
_fbody=('<h1>Gym software finder</h1>'
 '<p class="sub">Answer 3 quick questions - we\'ll match you to the best-fit tools from our '+str(len(TOOLS))+'-platform database, with real pricing.</p>'+DISC+
 '<div class="card">'
 '<h3>1. What type of business?</h3><select id="q_type">'
 '<option value="crossfit">CrossFit box</option><option value="yoga">Yoga studio</option>'
 '<option value="pilates">Pilates studio</option><option value="martial">Martial arts / BJJ</option>'
 '<option value="boutique">Boutique fitness studio</option><option value="personal">Personal trainer / online coaching</option>'
 '<option value="multi-location">Multi-location / franchise</option><option value="class-based">General class-based studio</option></select>'
 '<h3>2. How big are you?</h3><select id="q_size">'
 '<option value="solo">Solo / just starting</option><option value="small">Small (under 100 members)</option>'
 '<option value="mid">Mid-size</option><option value="large">Large / multi-site</option></select>'
 '<h3>3. Top priority?</h3><select id="q_pri">'
 '<option value="budget">Lowest cost</option><option value="transparency">Transparent, predictable pricing</option>'
 '<option value="features">Most features / premium experience</option></select>'
 '<a class="cta" href="#" onclick="runFinder();return false;">Show my matches →</a></div>'
 '<div id="fresult"></div>'
 '<script>const TOOLS='+_fjson+';'
 'function runFinder(){'
 'var ty=document.getElementById("q_type").value,sz=document.getElementById("q_size").value,pr=document.getElementById("q_pri").value;'
 'var kw={crossfit:["crossfit"],yoga:["yoga"],pilates:["pilates"],martial:["martial","dojo","bjj","karate"],boutique:["boutique"],personal:["personal","online coaching","trainer"],"multi-location":["multi-location","franchise","chain","health club"],"class-based":["class-based","class ","bootcamp"]}[ty]||[ty];'
 'var scored=TOOLS.map(function(t){var s=0;var hay=t.best_for.join(" ")+" "+t.seg;'
 'kw.forEach(function(k){if(hay.indexOf(k)>-1)s+=5;});'
 'if(sz=="solo"||sz=="small"){if(t.pmin<=110)s+=2;if(t.pmin>=250)s-=2;}'
 'if(sz=="large"){if(hay.indexOf("multi-location")>-1||hay.indexOf("chain")>-1||hay.indexOf("franchise")>-1)s+=3;if(t.pmin>=150)s+=1;}'
 'var badprice=t.complaints.join(" ");'
 'if(pr=="budget"){s+= t.pmin<=90?3:(t.pmin<=150?1:-1);}'
 'if(pr=="transparency"){if(badprice.indexOf("transparent")>-1||badprice.indexOf("hidden")>-1||badprice.indexOf("escalation")>-1||badprice.indexOf("increase")>-1||t.price.indexOf("Quote")>-1)s-=3;else s+=2;}'
 'if(pr=="features"){if(t.pmin>=150)s+=2;}'
 'return {t:t,s:s};}).sort(function(a,b){return b.s-a.s;});'
 'var top=scored.filter(function(x){return x.s>0;}).slice(0,4);if(top.length==0)top=scored.slice(0,3);'
 'var h="<h2>Your top matches</h2>";top.forEach(function(x,i){var t=x.t;'
 'h+="<div class=card><h3>"+(i+1)+". "+t.name+"</h3><p class=muted>"+t.price+(t.note?" - "+t.note:"")+"</p>";'
 'h+="<a class=cta href=\""+t.link+"\""+(t.aff?" rel=\"sponsored nofollow\"":"")+">See "+t.name+" details →</a></div>";});'
 'h+="<p class=method>Matches are generated from published pricing and best-fit tags. Always confirm current pricing on the vendor site. Some links are affiliate links.</p>";'
 'document.getElementById("fresult").innerHTML=h;document.getElementById("fresult").scrollIntoView({behavior:"smooth"});}'
 '</script>')
_fqas=[("How do I choose gym software?","Match the tool to your business type (CrossFit, yoga, martial arts, etc.), your size, and your top priority - cost, pricing transparency, or features. Our finder does this automatically from real pricing data."),
 ("What is the cheapest gym software?","Budget options start free-to-low for very small operations (e.g. per-member pricing), while full class-based platforms run $100-400+/mo. Use the finder with 'lowest cost' selected."),
 ("Which gym software has transparent pricing?","Some vendors publish clear per-tier pricing while others are quote-only with add-ons; the finder down-ranks tools known for hidden fees or mid-contract increases when you pick 'transparent pricing'.")]
open(os.path.join(OUT,"finder.html"),"w",encoding="utf-8").write(shell(_ftitle,_fdesc,_fbody,faq_ld(_fqas)))
print("finder.html written")


# --- sitemap.xml + robots.txt ---
_files = sorted(f for f in os.listdir(OUT) if f.endswith(".html"))
_urls = []
for _f in _files:
    _loc = f"https://{DOMAIN}/" + ("" if _f == "index.html" else _f)
    _pr = "1.0" if _f == "index.html" else ("0.5" if _f in ("privacy-policy.html", "affiliate-disclosure.html") else "0.8")
    _urls.append(f'  <url><loc>{_loc}</loc><lastmod>{D["_meta"]["last_verified"]}</lastmod><priority>{_pr}</priority></url>')
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(_urls) + "\n</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(
    f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
print("sitemap.xml + robots.txt written")
