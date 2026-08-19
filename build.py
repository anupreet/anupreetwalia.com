# -*- coding: utf-8 -*-
"""Static site generator for anupreetwalia.com"""
import os, time, json, markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
VER = int(time.time())   # cache-busting stamp appended to asset URLs each build
BASE = "https://anupreetwalia.com"   # canonical origin for SEO

PERSON_LD = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Anupreet Walia","url":"https://anupreetwalia.com","jobTitle":"CTO & Co-Founder","worksFor":{"@type":"Organization","name":"Brevian AI"},"description":"Engineering executive and technical co-founder. CTO & Co-Founder of Brevian AI. 19+ years building AI products and scaling teams across AI/ML systems, knowledge graphs, RAG, and agentic AI.","sameAs":["https://www.linkedin.com/in/anupreetwalia/","https://github.com/anusual","https://scholar.google.com/citations?user=_PfGUfcAAAAJ"],"address":{"@type":"PostalAddress","addressLocality":"San Mateo","addressRegion":"CA","addressCountry":"US"}}
</script>
'''

RESEARCH_LD = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ScholarlyArticle","headline":"BatchDAG: LLM-Planned Execution Graphs for Scalable Ad-Hoc Analysis Over Enterprise Data","author":{"@type":"Person","name":"Anupreet Walia"},"datePublished":"2026","publisher":{"@type":"Organization","name":"Brevian"},"url":"https://anupreetwalia.com/research.html","sameAs":"https://arxiv.org/abs/2607.18241"}
</script>
'''

def nav(active, depth=0):
    p = "../" * depth
    def cls(name): return ' class="active"' if name == active else ""
    return f'''<nav class="site"><div class="wrap">
  <a class="brand" href="{p}index.html">anupreet walia<span class="dot">.</span></a>
  <div class="links">
    <a href="{p}index.html#work"{cls('work')}>work</a>
    <a href="{p}writing/index.html"{cls('writing')}>writing</a>
    <a href="{p}research.html"{cls('research')}>research</a>
    <a href="{p}patents.html"{cls('patents')}>patents</a>
    <a href="{p}resume.html"{cls('resume')}>r&eacute;sum&eacute;</a>
  </div>
</div></nav>'''

def footer(depth=0):
    return f'''<footer><div class="wrap">
  <span>© 2026 Anupreet Walia</span>
  <span><a href="https://www.linkedin.com/in/anupreetwalia/">LinkedIn</a> · <a href="https://github.com/anusual">GitHub</a> · <a href="https://scholar.google.com/citations?user=_PfGUfcAAAAJ&hl=en">Scholar</a></span>
</div></footer>'''

def page(title, body, active, depth=0, desc="", cpath="", og_type="website", head_extra="", og_image=None):
    p = "../" * depth
    canonical = BASE + "/" + cpath
    og_image = og_image or (BASE + "/assets/og-image.png")
    # strip HTML entities that read awkwardly in social cards
    clean_title = title.replace("&amp;", "&")
    clean_desc = desc.replace("&amp;", "&")
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Anupreet Walia">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Anupreet Walia">
<meta property="og:title" content="{clean_title}">
<meta property="og:description" content="{clean_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{clean_title}">
<meta name="twitter:description" content="{clean_desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{p}assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<meta name="theme-color" content="#0d9488">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{p}assets/styles.css?v={VER}">
{head_extra}</head>
<body>
{nav(active, depth)}
{body}
{footer(depth)}
</body>
</html>'''

def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)

# ---------------------------------------------------------------- HOME
roles = [
    ("12/2024 to now", "CTO &amp; Co-Founder", "Brevian AI",
     "AI sales intelligence built on a structured knowledge graph and a multi-agent LLM system. Set product vision, designed the architecture, and built the engineering org. Shipped Meeting Prep, Live Assist, Sales Coaching, and CRM Updates."),
    ("2024", "VP of Engineering", "Baseten",
     "ML infrastructure for deploying and serving AI models at scale. Led developer experience and model observability on TRT-LLM and vLLM, drove SOC2, and launched the self-hosted enterprise offering."),
    ("2021–2024", "VP of Engineering", "Preset",
     "Cloud analytics on Apache Superset (backed by a16z, Redpoint). Launched SaaS, Hybrid Cloud, and Embedded products; scaled engineering from 20 to 60+ across frontend, platform, data, and infra."),
    ("2018–2021", "Director of Engineering / Interim VPE", "Snapdocs",
     "Digital mortgage closing platform (Sequoia, Y Combinator). Grew engineering from 11 to 100, building frontend, platform, data engineering, data science, and infrastructure teams from scratch."),
    ("2016–2018", "Engineering Manager", "Helix",
     "Personal genomics platform (KPCB, DFJ). Started the mobile team and shipped Helix&#39;s first native iOS app; built the platform iOS SDK, marketplace APIs, and OAuth2 framework for partners."),
    ("2015–2016", "Tech Lead", "Microsoft",
     "Built Office prototypes with ML and an iOS app using MS Band biometrics for stress detection with Microsoft Research. Selected for the High Potential (HiPo) program."),
    ("2009–2015", "Computer Scientist", "Adobe",
     "Full-stack apps, APIs, and data pipelines for Typekit; optimized Flash Player and AIR runtime on Android for battery, memory, and rendering performance."),
]
role_html = "\n".join(
    f'''<div class="role"><div class="when">{w}</div><div class="what">
    <h3>{t} · <span class="org">{o}</span></h3><p>{d}</p></div></div>''' for w,t,o,d in roles)

cards = [
    ("Paper", "BatchDAG", "LLM-planned execution graphs for scalable ad-hoc analysis over enterprise data. Deployed in production at Brevian.", "research.html"),
    ("Writing", "Brevian Engineering", "Essays on context engineering, multi-agent harnesses, and the MCP intelligence layer.", "writing/index.html"),
    ("Patents", "Genomic Data UI", "Six granted patents / applications from Helix on cross-network genomic data interfaces.", "patents.html"),
    ("Profile", "Google Scholar", "Publications and citations.", "https://scholar.google.com/citations?user=_PfGUfcAAAAJ&hl=en"),
]
card_html = "\n".join(
    f'''<a class="card" href="{u}"><span class="tag">{tag}</span><h3>{h}</h3><p>{p}</p><span class="go">→</span></a>'''
    for tag,h,p,u in cards)

links_external = [
    ("Baseten: Introducing Baseten Self-hosted", "https://www.baseten.co/blog/baseten-self-hosted/"),
    ("Preset: Build and Deploy in SaaS-COSS", "https://preset.io/blog/build-and-deploy-in-saas-coss/"),
    ("Snapdocs: Women Leaders Who&#39;ve Scaled Startups", "https://www.builtincolorado.com/articles/women-leaders-scaled-startups"),
    ("Helix: Personal genomics platform", "https://www.helix.com/"),
]
ext_html = "\n".join(
    f'''<div class="role"><div class="when"></div><div class="what"><h3><a href="{u}">{t} ↗</a></h3></div></div>'''
    for t,u in links_external)

home_body = f'''<header class="hero"><div class="wrap">
  <p class="eyebrow">Engineering Executive · Technical Co-Founder</p>
  <h1>Anupreet Walia</h1>
  <p class="lede">I build AI products from scratch and scale the teams and platforms behind them.</p>
  <p class="sub">19+ years across AI/ML systems, knowledge graphs, RAG, and agentic AI, from founding teams to orgs of 100+ engineers at venture-backed startups (Sequoia, a16z, Y Combinator). This is where my technical work, writing, research, and patents live in one place.</p>
  <div class="btn-row">
    <a class="btn primary" href="research.html">Read BatchDAG →</a>
    <a class="btn" href="writing/index.html">Writing</a>
    <a class="btn" href="resume.html">Résumé</a>
  </div>
  <div class="meta-row">
    <span>San Mateo, CA</span>
    <a href="https://www.linkedin.com/in/anupreetwalia/">linkedin.com/in/anupreetwalia</a>
    <a href="https://github.com/anusual">github.com/anusual</a>
  </div>
</div></header>

<section id="highlights"><div class="wrap">
  <p class="eyebrow">In one place</p>
  <h2>Technical work</h2>
  <div class="cards">{card_html}</div>
</div></section>

<section id="work"><div class="wrap">
  <p class="eyebrow">Experience</p>
  <h2>Where I&#39;ve built</h2>
  {role_html}
</div></section>

<section id="elsewhere"><div class="wrap">
  <p class="eyebrow">Selected external work</p>
  <h2>Published elsewhere</h2>
  <p style="color:var(--muted);max-width:640px;margin:0 0 8px">Company posts and features tied to my work at each org.</p>
  {ext_html}
</div></section>

<section id="projects"><div class="wrap">
  <p class="eyebrow">Side projects</p>
  <h2>On the side</h2>
  <div class="cards">
    <a class="card" href="https://kaixn.com"><span class="tag">Side project</span><h3>Kaixn</h3><p>An independent project I build and run on the side.</p><span class="go">kaixn.com →</span></a>
  </div>
</div></section>

<section id="code"><div class="wrap">
  <p class="eyebrow">Code</p>
  <h2>GitHub</h2>
  <p style="color:var(--muted);max-width:640px;margin:0 0 8px">Most of my recent building lives under <a href="https://github.com/anusual">@anusual</a> (earlier work under <a href="https://github.com/anupreet">@anupreet</a>). From 50 contributions in 2024 to 1,266 in 2025 and 1,563 in the last year, much of it relearning the craft hands-on.</p>
  <a class="gh-years" href="https://github.com/anusual">
    <img loading="lazy" alt="GitHub contributions in the last year (1,563)" src="assets/gh-lastyear.png">
    <img loading="lazy" alt="GitHub contributions in 2025 (1,266)" src="assets/gh-2025.png">
    <img loading="lazy" alt="GitHub contributions in 2024 (50)" src="assets/gh-2024.png">
    <span class="gh-handle">github.com/anusual ↗</span>
  </a>
</div></section>'''

write("index.html", page("Anupreet Walia · Engineering Executive · Technical Co-Founder",
      home_body, "home", 0,
      "Anupreet Walia, engineering executive and technical co-founder. Technical product, writing, research (BatchDAG), and patents in one place.",
      cpath="", head_extra=PERSON_LD))

# ---------------------------------------------------------------- POSTS
posts = [
    {
      "slug": "observing-a-healthy-engineering-system",
      "title": "[WIP] Observing a Healthy Engineering System",
      "date": "Aug 19, 2026",
      "iso": "2026-08-19",
      "read": "6 min",
      "host": True,
      "first_here": True,
      "image": "observing-engineering-system-header.png",
      "image_alt": "Three properties of a healthy engineering system: Efficiency (capacity allocation, bet predictability, delivery, deploy to evidence), Accuracy (works as built, works as expected by the customer, bet outcome vs expected) and Growth (team, usage and revenue grow without disproportionate engineering work).",
      "deck": "The engineering system as People, Architecture and Systems/Processes executing roadmap bets, and three properties to observe it by: Efficiency, Accuracy and Growth.",
      "md": """As engineering leaders, we track a lot of metrics. Deployment frequency, lead time, defects, uptime, MTTR, roadmap delivery, customer bugs, team health, etc.

Most of these are easy to collect. On their own, they don't tell us whether the engineering system is healthy.

I use a simple model for the engineering system.

Company strategy informs Product strategy. Product strategy gets expressed as a roadmap, which is a set of bets about where we should invest. Engineering executes those bets through three things: **People, Architecture and Systems/Processes**.

Each of these has its own health signals.

For People, I care about things like cognitive load, communication overhead, ownership and knowledge sharing.

For Architecture, I care about defect rates, MTTR, deployment frequency and lead time.

For Systems/Processes, I care about satisfaction, performance and how well teams collaborate.

![The engineering system: company strategy informs product strategy, expressed as a roadmap of bets, which engineering executes through People, Architecture and Systems/Processes, each with its own health signals.](../assets/engineering-system-model.png)

These tell me whether different parts of the system are operating well. They don't tell me whether the system as a whole is producing what we need from it.

For that, I look for three properties: **Efficiency, Accuracy and Growth**.

### Efficiency

An efficient engineering system spends its capacity where we intended, executes its bets predictably and gets to evidence quickly.

The first thing I want to know is where the capacity went.

If the company strategy requires us to invest in Growth and Moat, but most of the engineering capacity is going into Floor and Gate work, the engineering organization may be executing well while still not executing the strategy.

This can be as simple as looking at planned vs actual allocation across the roadmap bets.

The second is predictability of the bets.

Roadmap commit vs delivered has historically been a useful measure here, but delivery is no longer the complete boundary. In [From Delivery to Learning](https://anupreetwalia.com/writing/from-delivery-to-learning.html), I expanded the dev loop from:

**hypothesis → specification → build → test → deploy**

to:

**hypothesis → specification → build → test → deploy → observe → learn → iterate**

So predictability needs to account for the bet, not just the feature. Did the bets we committed to progress to a result in the window we expected?

This doesn't mean the original scope needs to ship unchanged. A bet can change or stop because we learned something and still have moved through the system successfully.

DORA continues to measure an important part of this cycle. Deployment frequency, lead time and the stability of the delivery system tell us whether we can get changes into production efficiently.

I would add another clock after deployment:

**deploy → evidence**

Once the feature is in production, how long does it take us to know what happened?

If implementation gets 10x faster but a feature sits in production for six weeks before we know whether the customer can use it, the bottleneck moved. Measuring deploy → evidence makes that part of the loop visible.

So for Efficiency I want to observe:

| Measure | What I am looking for |
| --- | --- |
| Capacity allocation | Did engineering capacity go where we intended? |
| Bet predictability | Did the bets progress to a result in the expected window? |
| Delivery | Can we get changes into production quickly and reliably? |
| Deploy → evidence | How quickly do we know what happened after deployment? |

### Accuracy

Efficiency tells us how well work moves through the system. We also need to know whether we are doing the work right.

There are two kinds of correctness here.

**It works as built.**

The software behaves the way we specified. It is available, reliable and doesn't generate an unreasonable number of defects. SLA/uptime, defect rates, MTTR and other reliability measures give us this view.

**It works as expected by the customer.**

A feature can have 99.99% uptime, no bugs and still not work for the customer.

The customer may not be able to discover it. The workflow may not make sense. They may not be able to complete the job we expected them to complete. Or they may use it correctly and still not get the value in the original hypothesis.

This is where Product NPS, customer-reported issues and the expected outcome of the bet come in.

The distinction also matters when a bet fails.

Say we made a Gate bet because five customers told us they needed a capability. We built it correctly, all five could use it as intended, and none of them ended up needing it.

The bet was wrong. The engineering system wasn't necessarily inaccurate.

Now take the same feature, but the customers want it and can't complete the workflow because the UX prevents them from doing so. The software may technically work as built, but it isn't working as expected by the customer.

Both views belong in Accuracy.

| Measure | What I am looking for |
| --- | --- |
| Reliability / SLA | Does it work as built? |
| Defects / MTTR | How often does it break and how quickly do we recover? |
| Customer-reported issues | Where does the customer's experience differ from what we built? |
| Bet outcome vs expected outcome | Did the customer get the result the hypothesis expected? |

### Growth

A healthy engineering system also needs organic, easy paths to scale.

I look at scale across three surfaces: **team, usage and revenue**.

For the team, can we add people without communication and coordination overhead growing faster than the team? Can a new engineer become productive without needing to understand the entire system? Do ownership boundaries continue to work as the organization grows?

For usage, can the system handle the growth we expect? That could be users, transactions, API calls, workloads or whatever represents scale for the product.

For revenue, can the product support the next level of commercial growth without engineering becoming the constraint? If every new revenue tier, customer segment or large customer requires bespoke engineering work, revenue can be growing while the engineering system itself isn't scaling.

I compare these against what we planned for.

If we planned for 2x transactions and achieved 2x transactions, that alone doesn't tell me the system scaled well. If getting there required three months of emergency capacity work and heroics, we reached the number but didn't have an easy path to it.

| Surface | What I am looking for |
| --- | --- |
| Team | Can we add people without disproportionate coordination and cognitive load? |
| Usage | Can users, transactions, API calls and workloads grow without disproportionate engineering work? |
| Revenue | Can revenue grow without engineering becoming the constraint? |

### Putting the views together

A system can look healthy from one view and be unhealthy from another.

We can have excellent DORA metrics and consistently deliver the wrong bets.

We can deliver the right bets quickly and have customers unable to use them.

We can have a reliable product with growing usage while every increase in scale requires an engineering project.

We can also miss a product hypothesis while having a healthy engineering system that got us to that answer quickly and accurately.

People, Architecture and Systems/Processes tell us how the machinery is operating.

Efficiency, Accuracy and Growth tell us whether that machinery can execute the strategy we are asking it to execute.

As the dev loop expands from delivery to learning, the observations need to expand with it.""",
    },
    {
      "slug": "architecture-at-agent-speed",
      "title": "[WIP] Architecture at Agent Speed",
      "date": "Aug 19, 2026",
      "iso": "2026-08-19",
      "read": "8 min",
      "host": True,
      "first_here": True,
      "image": "architecture-at-agent-speed-header.png",
      "image_alt": "How governed architectural decisions move through the loop: spec review starts from the governed decisions, build gives them to the agent as context, PR review evaluates the code diff plus the decision delta, and drift detection surfaces de facto decisions forming in the repository.",
      "deck": "Coding agents let repositories evolve faster than teams can absorb the decisions being made. Architecture becomes a set of governed decisions that move through spec review, implementation and drift detection at the same rate as the code.",
      "md": """Coding agents have drastically increased the rate at which code gets written and how quickly repositories evolve. Every code change also carries decisions about the system: a new service creates a boundary, a feature introduces a representation of a domain concept, or an implementation adds a dependency and extends an existing pattern. Most of these decisions look reasonable in the context of the change being made.

Individual decisions generated in a single spec are not the issue. The problem shows up when these decisions stack across multiple features and branches. One feature introduces a pattern, another makes a slightly different choice, and a third extends the first pattern for a new use case. Each plan can be sane independently and each PR can be correct, while the resulting architecture is one we never consciously decided to build.

This isn't a new problem. Engineering teams have always accumulated decisions as they build software, and we use tech specs, ADRs (architecture decision records), architecture reviews, code reviews and conventions to keep the team aligned. A lot of this context also lives with engineers who have worked on the system long enough to know why something is built the way it is. Coding agents change the rate at which these decisions accumulate. Repositories can now evolve faster than the engineering organization can review the decisions being made, absorb them and keep the rest of the team aligned.

There is a limit to how many decisions a team can carry while continuing to make new ones coherently. As a system grew past that limit, we would split the team, give each team a narrower scope and create clear ownership boundaries. Each team needed to carry a smaller part of the system in its head.

Coding agents change that balance. Decisions can accumulate faster than we can reorganize teams around them, and the context that used to live in each team's heads doesn't automatically transfer to the agents doing the implementation. Splitting ownership still reduces the surface a team needs to reason about, but it doesn't give the agent the accumulated decisions it needs when making the next change.

One response has been to write more of that knowledge down in files the agent can read: AGENTS.md, coding guidelines, agent skills, tech specs and ADRs that describe how the team builds software and what it is trying to build. We did the same thing: put the engineering specs in one place and made them available to the coding agent while it planned and implemented the next feature.

That helped, but a plan describes the change we are making now. Architecture also has to account for the decisions we have already made and how the next decision fits with them. A plan can introduce a new service boundary that makes complete sense for the feature being built, and a few weeks later another plan can introduce a different boundary for a similar problem that also makes sense locally. The second decision is still being made in a system where the first one already exists.

Giving the agent both plans provides more context, but it doesn't manage how those decisions stack. Some decisions are conventions, some are invariants, some apply only to one part of the system, and some should change as the system evolves. Putting all of this into a larger AGENTS.md doesn't tell us which decisions the team has committed to, where they apply, or whether the next change is proposing to evolve one.

As the rate of implementation increases, we need a way to manage decisions at the same rate. Architecture becomes a set of governed decisions: which ones the team has committed to, where each applies, and how the system is allowed to evolve.

The codebase contains the results of previous decisions, docs and ADRs contain some of the reasoning, and engineers carry more of it in their heads. Governance makes those decisions explicit without requiring every engineer or agent to carry all of them. The relevant decisions can then be available when a spec is written, when an agent plans a change, when the implementation is reviewed and when the accumulated implementation drifts from them.

### Moving review up a level

Technical specs and RFCs have traditionally been among the places where we make and review architectural decisions. A spec might contain the proposed data flow, sequence diagrams, API design, component boundaries and the reasoning behind the approach. Reviewing the spec gave the team a chance to agree on the design before someone implemented it.

Agents are already good at producing a lot of this lower-level design. Given the intent and constraints, they can work through data flows, sequence diagrams, API shapes and implementation plans, and follow established principles like REST. As more of that work moves to agents, human review can focus on the architectural decisions that constrain those designs rather than review every part of the generated technical spec with the same attention.

If a feature needs a new service, for example, the architectural decision isn't every endpoint the agent proposes. We need to decide whether a new service is warranted, which domain owns it, what boundary it creates and what dependencies we allow across that boundary. The agent can work through much of the detailed design once those decisions are made.

This also changes what we preserve from the review. A technical spec records an implementation plan for a particular piece of work, while the architectural decisions made during that review can apply to work that follows it. If we decided that a domain owns a concept, that a service boundary is intentional or that a particular dependency direction isn't allowed, the next feature needs those decisions available without anyone having to find the spec where they were originally made.

The next spec can therefore start with the governed decisions that already apply to the system. It can work within them or propose that one needs to change, and that change can be reviewed as a decision before the agent generates the detailed design and implementation.

### Reviewing the implementation

The same decisions need to be available while the agent writes the code. An agent shouldn't have to infer from nearby implementations that a domain owns a concept, that dependencies move in one direction, or that a common pattern is an intentional invariant rather than something that happens to appear frequently in the repository.

Once the implementation comes back, the PR can be evaluated against the decisions that governed it. Alongside the code diff, we can look at the decision delta: whether the implementation followed the decisions we already made, evolved one of them, introduced a new pattern, created an exception or left part of the intended architecture incomplete.

Code review has historically done a lot of this implicitly. A senior engineer sees a dependency in a PR and knows it violates a boundary, someone notices that a new abstraction is inconsistent with a pattern used elsewhere, or a reviewer remembers that the team tried an approach before and decided against it. That works when humans can carry enough of the architecture in their heads and have enough time to find these decisions while inspecting the implementation.

As the volume of generated code increases faster than our ability to review it, finding architectural decisions line by line becomes a poor use of the human judgment available. Surfacing the decision delta lets the review focus on whether the team agrees with how the system is evolving, while the implementation can still be checked for correctness against those decisions.

### Observing the architecture as it evolves

Spec review tells us about the architecture we intended to build, while the repository contains the architecture we actually built. If repositories are evolving continuously, we also need to observe whether the accumulated implementation continues to match the decisions we have made.

Concept and domain drift become useful signals here because architectural change doesn't always arrive as one explicit decision in one PR. A concept can start acquiring multiple representations across the repository, two parts of the product can develop slightly different meanings for the same thing, ownership can gradually move across boundaries, or a dependency that started as an exception can become a pattern after several more changes use it.

Each of those changes can be locally correct while their accumulation moves the system in a direction the team hasn't explicitly chosen. Drift gives us a way to see that a de facto decision may be forming in the repository before it is represented in the governed decisions.

That doesn't make all drift a violation. If the existing architectural decision still fits the system, the drift can be corrected before more changes build on it. If the same drift keeps appearing because the existing decision no longer fits what we are building, the team can review the emerging pattern, ratify the new decision and make it available to the next spec and implementation.

As coding agents increase the rate at which repositories evolve, the decisions need to move through the work at the same rate. They are available when a spec is reviewed, become context while the agent builds, are checked against the implementation during review, and are updated when drift shows that the architecture itself is changing.""",
    },
    {
      "slug": "from-delivery-to-learning",
      "title": "[WIP] From Delivery to Learning",
      "date": "Aug 18, 2026",
      "iso": "2026-08-18",
      "read": "5 min",
      "host": True,
      "first_here": True,
      "image": "from-delivery-to-learning-header.png",
      "image_alt": "The dev loop extended from delivery to learning: hypothesis, specification, build, test, deploy, then observe, learn and iterate. The old boundary was deploy; executing the bet now includes activation, instrumentation and the first feedback loop.",
      "deck": "If engineering can implement a feature 3x faster but it takes the same time to learn whether customers want it, we haven't captured the gain. Why the dev loop needs to extend from delivery to learning.",
      "md": """If engineering can implement a feature 3x faster, but it still takes us the same amount of time to learn whether customers want it, have we captured the productivity gain we expected from AI?

As engineering leaders, we spend a lot of time optimizing the dev loop - how quickly we can build, test and deploy. This loop is largely optimized around getting a feature into production. There is a lot of iteration inside that process, but "deployed successfully" is still a reasonable boundary for where engineering work on a feature ends.

AI is making parts of that loop faster, particularly planning and implementation. Based on the old metrics, engineering output or throughput should be multiples of what it was - 3x today, with 10x as the promise. But the outcomes don't seem to have moved the same way.

When this loop became faster, the bottleneck moved to choosing what gets built, and we call it "taste" or judgement.

If we look back, when we were shipping CDs and the cost of bugs was high, we used to have a separate QA stage. As we moved to CI/CD, the cost of shipping and fixing bugs became lower and we shifted QA left. The same argument can be made now for product taste or judgement. If we want to benefit from AI, we need to move this left, i.e. make it part of the dev loop.

That means extending the development loop from **delivery to learning**.

### Roadmaps are bets

In order to move part of product validation to the dev loop, we need to get crisp about why and how we choose what to build, which is historically represented as the roadmap. A product roadmap is a list of bets, and each bet carries one class that says why it is on the list. The class is not a description of the work but the reason we are doing the work now.

To glance at the roadmap and know what we are investing in, some form of classification is needed. For this exercise, let's use these: Floor (keep the lights on), Moat (get harder to copy), Gate (open a closed door), Growth (turn arrivals into users), Monetize (turn usage into revenue), and Enabler (unlock what we ship next).

| Class | What the bet is for |
| --- | --- |
| Floor | Keep the lights on. Oncall, dependency upgrades, capacity, forced migrations, the bug backlog. |
| Moat | Make us harder to copy over time. Includes community and ecosystem work, since what other people build on top of us is the part that compounds. |
| Gate | Open a specific door that is closed today. A named customer, market, partner, or compliance requirement. |
| Growth | Move people from arriving to actually using the surface that will eventually be paid for. |
| Monetize | Convert usage that already exists into revenue. |
| Enabler | Unlock an internal capability we do not have yet, where the value is in what it lets us ship next. |

The class gives us the why. The bet still needs a hypothesis that says why now and what a good outcome looks like. Product owns choosing what bets we make (this rigor ain't changing) and why now. EPD (Engineering, Product, and Design) owns executing the bet until the bet plays out.

As a running example, take a Gate bet: a capability that five named customers need before they can adopt the product.

### Expanding the dev loop

The dev loop today looks roughly like:

**Hypothesis → specification → build → test → deploy**

There is already iteration inside this loop. Requirements change, designs change, engineers find constraints, and EPD makes decisions together.

The boundary is still deployment.

For that Gate bet, deployment tells us the capability exists and works. It doesn't tell us whether the customers activated it, whether they could use it, or whether something in the product prevented them from getting the value we expected.

Those questions are often handled after the feature ships. We look at usage, collect customer feedback, decide what needs to change, prioritize the follow-up and bring another piece of work into the dev loop.

AI makes the build part of that cycle cheaper. Leaving the rest of the cycle unchanged limits the gain to producing the first version faster.

The larger loop is:

**Hypothesis → specification → build → test → deploy → observe → learn → iterate**

Activation, instrumentation, product acceptance and the first feedback loop become part of executing the bet.

The engineering specification now contains the expected outcome alongside the feature requirements. For the Gate bet built for five customers, we know before implementation how those customers will get access, what we need to observe and what evidence tells us whether the gate actually opened.

This is the same shift-left pattern we have used before. When QA was a separate stage, the engineering loop ended before quality was established. CI/CD made iteration cheaper and testing moved into the dev loop. AI makes implementation cheaper, and product acceptance and learning can move into the loop as well. AI helps on this side too - instrumenting the feature, synthesizing feedback, and analyzing usage are getting cheaper alongside implementation.

Product still owns what bets we make and why now. Moving product acceptance left doesn't move product strategy to Engineering. It expands what EPD owns when executing the bet.

### A delivered feature is not a resolved bet

Take the same Gate bet. We build the capability, ship it in two months and it works correctly. If none of the five customers use it, the bet failed but the feature was delivered.

That result can still represent a healthy loop if we get the answer quickly enough to act on it. The loop ends when the bet has played out far enough to know what to do next. Success can mean adoption. It can also mean learning quickly that the hypothesis was wrong and stopping the investment.

If implementation gets 10x faster but the time from making a bet to getting enough evidence to make the next decision stays the same, only one part of the loop got faster.

The cycle to optimize is **bet → evidence → next decision**.""",
    },
    {
      "slug": "revising-the-engineering-interview-loop",
      "title": "Revising the Engineering Interview Loop",
      "date": "Aug 17, 2026",
      "iso": "2026-08-17",
      "read": "11 min",
      "host": True,
      "first_here": True,
      "orig": "https://www.linkedin.com/posts/anupreetwalia_this-is-a-work-in-progress-i-have-been-ugcPost-7495263711993987072-557Z/",
      "image": "interview-loop-header.png",
      "image_alt": "What the coding interview stops measuring, and what it starts measuring instead: skills added (planning with an agent, context management, iteration, judging generated code, efficiency, rollout design, validation), skills that are no longer signal, and skills unchanged.",
      "deck": "Skill-based interviewing gives us a way to change hiring as engineering itself changes. How I am updating the loop (coding with agents, feature design through rollout) now that coding agents are part of the job.",
      "md": """I have always preferred skill-based interviews. The basic premise is that hiring should evaluate whether someone has the skills required to do the job, and the interview process should be designed specifically to collect that evidence.

Structured interviewing has existed for a long time, and Google helped make the approach common in technology companies. One of the reasons for introducing more structure into interviewing was to reduce the effect of unconscious bias. If interviewers decide independently what they care about after meeting a candidate, decisions can easily become influenced by familiarity, background, communication style, or simply what an individual interviewer happens to value. Defining the skills, questions and evaluation criteria in advance creates a more consistent basis for making the decision.

There are a few parts to making this work in practice.

### Start with the skills the team needs

For a startup, I start the hiring process by looking at the existing engineering team and identifying the skills we are missing.

This matters more at smaller companies because there is very little redundancy in the team. If you have eight engineers and nobody has experience operating a particular kind of distributed system, that is a meaningful gap. Before ~30 people, individual hires can materially change what the engineering organization is capable of doing.

So, you start with skills, and the job description follows from this exercise. Some of those skills will be common across engineering roles and others will exist because of the particular gap/specialization we are trying to fill. The interview loop can then be constructed around them. Every important skill in the job description should have somewhere in the loop where we evaluate it. Similarly, every interview in the loop should correspond to something we have decided is important for the role.

This also makes it possible to notice when an interview loop has accumulated sessions that no longer serve a purpose. Engineering organizations often inherit interview formats from previous companies or continue running a particular interview because it has always been part of the process. Starting from the skills gives us a way to periodically reconsider whether each session is still useful.

### Define the evaluation before interviewing candidates

For each session in the loop, we need to decide what skills are being tested, how we will test them and how the interviewer should score what they observe.

The scoring rubric should be created at the same time as the interview loop mostly to avoid updating the evaluation for a skill that was not part of the criterion while interviewing someone we like. When that happens, the candidates we saw earlier were evaluated against a different standard, and we no longer have a consistent basis for comparing them. We can decide that we got the role definition wrong and change it for subsequent candidates, but the evaluation for a particular loop should remain consistent.

The interviews themselves should also be administered as similarly as possible. Candidates should get equivalent problems, comparable information and roughly the same amount of help from the interviewer. Interviewers need to understand what they are evaluating and what different scores mean.

There will always be judgment involved in interviewing. The purpose of structure is to make that judgment operate against criteria we agreed on before knowing who the candidate was.

### The engineering skills I have traditionally evaluated

For engineering roles, I have generally organized the loop around four areas: coding, system design, feature design, and values and principles. Fifth loop gets added if we are looking for specialization like Data Science or FE etc.

The coding interview looks at programming ability and the engineering practices someone applies while writing software. I care about whether they can understand a problem, structure an implementation, reason through edge cases, debug it and leave behind code that another engineer could work with.

System design looks at depth in distributed systems and the ability to reason about scale. The specifics depend on the role, but this is where we can explore data models, service boundaries, consistency, reliability, latency, failure modes, capacity and operational concerns. The goal is to understand how well someone can reason about systems once the problem is larger than a single program.

Feature design is closer to the normal interaction between engineering and product. A PM can provide a product requirement and the engineer works through what would be required to implement it. This gives us a view into how they deal with ambiguity, identify the core technical work, make product and engineering tradeoffs, define interfaces and data models, and decide what should be included in the initial implementation.

The values and principles interview covers how someone approaches their work and makes decisions. I use it to understand what they value in an engineering organization, how they think about ownership, quality, speed, disagreement and collaboration, and whether there are important areas of disconnect with the way the company operates.

These categories have been fairly stable for me until coding agents! This is the new version I have, and I am actively looking at how others are doing it.

| Interview | Skills tested before | Skills tested now | Rubric |
| --- | --- | --- | --- |
| **Coding → Coding with agents** | Problem decomposition, programming fundamentals, code structure, correctness, debugging, testing and engineering practices | All of the previous skills, plus planning with an agent, context management, task decomposition, iteration, evaluation of generated code and efficient use of the agent | **Problem understanding:** develops a coherent model of the problem before making significant changes. **Plan:** creates a reasonable implementation approach and decomposes work into verifiable steps. **Context:** gives the agent relevant context without repeatedly expanding context unnecessarily. **Iteration:** recognizes incorrect or unproductive directions and adjusts effectively. **Code judgment:** reads and evaluates generated code rather than assuming it is correct. **Correctness:** produces a working, tested implementation and can explain it. **Efficiency:** makes reasonable use of time, interactions and tokens to reach the result. |
| **System design** | Distributed systems, data modeling, service boundaries, scalability, reliability, consistency, latency, capacity and failure modes | Largely unchanged | **Decomposition:** identifies the important components and responsibilities. **Tradeoffs:** understands and explains architectural choices rather than relying on standard patterns. **Scale:** identifies where the design changes as load and data grow. **Reliability:** reasons about failures, recovery and degraded operation. **Data:** chooses appropriate storage and consistency models. **Operations:** considers observability, capacity and production behavior. |
| **Feature design → Feature design + rollout** | Translating product requirements into technical design, managing ambiguity, APIs, data models, edge cases, implementation scope and product/engineering tradeoffs | All of the previous skills, plus rollout design, feature gating, experimentation, observability, validation and iteration | **Requirements:** turns the product requirement into a clear technical problem. **Scope:** identifies a reasonable first implementation and avoids unnecessary work. **Design:** produces coherent APIs, data models and system changes. **Rollout:** defines how the feature can be exposed incrementally and disabled safely. **Observability:** identifies the operational and product signals required during rollout. **Validation:** defines what would indicate that the feature is working and what would cause the team to stop or change course. **Iteration:** designs the implementation so that the team can learn and modify the feature without excessive cost. |
| **Values and principles** | Ownership, quality, speed, collaboration, disagreement, decision-making and alignment with how the company operates | Largely unchanged | **Decision-making:** can explain how they make decisions when there are competing priorities. **Ownership:** demonstrates an appropriate level of responsibility for outcomes. **Tradeoffs:** has a considered approach to quality, speed and scope. **Collaboration:** can work through disagreement and incorporate information from others. **Self-awareness:** can describe decisions that did not work and how their thinking changed. **Alignment:** no significant disconnect between the candidate's working principles and the environment we are hiring them into. |
| **Specialization, when required** | Role-specific depth such as frontend, data science, ML, security or infrastructure | Changes based on the skill gap identified for the role | Defined when the role is created. The rubric should describe the specific depth required for this hire rather than using a generic specialization interview. |

### Coding with agents

Engineers on our teams are increasingly going to write software with coding agents. I want the coding interview to reflect that environment.

The candidate should have access to an agent and be given an engineering task. The interview can then evaluate how they use the agent as part of the implementation process.

There are several skills involved here that weren't visible in a traditional coding interview. One is context management. The candidate has to determine what information the agent needs, how much of the codebase or problem to expose, and how to keep the agent working with the relevant context as the task progresses.

Planning is another part of it. For a sufficiently complicated task, I would expect the engineer to understand the problem and develop an approach before asking an agent to make broad changes. That plan may itself be developed with the agent. What is critical here is whether the engineer has a coherent model of what they are trying to build and can break the work into pieces that can be executed and verified.

Iteration is also observable. Agents will produce implementations that are incomplete, unnecessarily complicated or simply wrong. The engineer needs to recognize this, determine what caused the problem and decide whether to correct the current approach or change direction. They also need to know when to inspect the code directly rather than continuing to prompt.

Efficiency is the third axis of evaluation. An engineer can get to a working solution through a large number of agent interactions and a very large context, or they can provide better context and direction and get there with considerably less work. Tokens, elapsed time and number of interactions aren't useful as isolated metrics, but they provide additional information about how effectively someone is using the tool.

The resulting interview still tests programming. The candidate has to understand the generated code, evaluate its correctness, make technical decisions and take responsibility for the final implementation. We are also evaluating a new set of skills around directing the agent that produced some of that implementation.

### System design

I don't see a significant reason to change the system design interview yet.

The implementation tools available to engineers have changed, but the systems we operate still have the same underlying properties. Engineers need to understand distributed systems, data, reliability, capacity, latency and failure modes. They need to be able to make architectural decisions and understand how those decisions behave as usage grows.

Agents can make implementing a proposed architecture considerably faster, which may eventually change some of the emphasis in system design interviews. For now, the underlying skill being measured is still one I want to evaluate directly.

### Feature design and rollout

Feature design needs a broader scope.

As implementation becomes faster, teams can build more features and more variations of a feature in the same amount of time. That increases the importance of being able to test those features cheaply and safely. If experimentation and rollout remain expensive, the organization moves the bottleneck from implementation to validation.

I would therefore extend the feature design interview through the rollout of the feature.

After working through the implementation, the candidate should describe how they would introduce it into production. This includes feature gating, the initial population that receives the feature, the ability to disable it, the telemetry required to understand its behavior, and the tests that need to exist before and during rollout.

The candidate should also define how they would validate the feature. Depending on the product, this could involve operational metrics, product metrics, qualitative feedback or an experiment. I want to understand what information they would collect, how they would decide whether to expand the rollout, and what they would do if the results were unclear.

This is also useful for understanding how an engineer thinks about iteration. The first implementation does not need to answer every product question. A feature can be designed so that the team can expose it to a small population, learn something specific and make the next implementation decision with more information.

Feature gating and observability become part of the technical design in this model. They need to be considered while designing the feature because they affect its architecture and determine how easily the team can operate and modify it after release.

This could be a separate interview for roles where experimentation and rollout are particularly important. For most product engineering roles, I would start by extending the existing feature design session rather than adding another interview.

### Values and principles

I would keep the values and principles interview largely unchanged.

The tools engineers use will continue to change, and teams will develop new working practices around them. The values interview is intended to understand the more persistent aspects of how someone works: how they make decisions, what they expect from other engineers, how they handle disagreement, what they consider good engineering work and what kind of environment allows them to do their best work.

There will naturally be some discussion of AI and agents here because they are now part of engineering work, but I don't think they require a separate values framework.

### Updating the loop

With these changes, the engineering loop I would use today consists of coding with agents, system design, feature design and rollout, and values and principles.

That particular set of interviews isn't intended to be permanent. It reflects the engineering skills I currently want to evaluate. As the way we build software changes, I expect the skills to change again.

The process for changing the interview loop should remain the same. Look at the engineering organization and the work it needs to do. Identify the skills that are missing or particularly important. Put those skills into the definition of the role. Design interviews that allow candidates to demonstrate them. Define the scoring criteria before interviewing candidates, and administer the resulting loop consistently.

That is the useful part of a skill-based interview system. It gives us a way to change hiring as engineering itself changes without having to reinvent how we think about hiring each time.""",
    },
    {
      "slug": "context-driven-design",
      "title": "Context-Driven Design: A Design Pattern",
      "date": "Jul 28, 2025",
      "read": "5 min",
      "deck": "Context-Driven Design treats context assembly as a first-class architectural concern: assembling the right working set of information at the moment of inference to build reliable LLM applications.",
      "orig": "https://www.brevian.ai/resources/context-driven-design",
      "md": """## From Prompts to Context Engineering: Why LLM Applications Need a New Design Paradigm

### Background

Large language models (LLMs) are transforming the way we build software, but their output quality is directly tied to the context they are given at inference time. Unlike traditional systems that operate solely on explicit parameters or static code, LLM-based applications rely on a dynamic, composite input — what we call context — to reason effectively. As these systems move from experimental prototypes to production-grade deployments, a gap has emerged as to how context should be assembled and delivered.

### Introducing Context-Driven Design

I see Context-Driven Design as a new, emerging design pattern specifically for LLM-powered systems as we go deeper into context engineering as a field of study. Existing design paradigms like Object-Oriented Design and Domain-Driven Design focus on how to structure code and manage domain models, but they do not address the unique runtime requirements of an LLM. In these systems, the model's reasoning quality depends on a transient working set of information — retrieved knowledge, rules, and interaction history — streamed into the model at inference time. Without a deliberate method to curate and structure this input, applications suffer from degraded accuracy, higher latency, and unpredictable outputs.

Context-Driven Design fills this gap by treating context assembly as a first-class architectural concern, one which focuses on assembling the right working set of information at the moment of inference to build reliable LLM applications.

### What Context Includes

Context is far more than the prompt a user types. It is a structured working set that includes retrieved knowledge chunks from a retrieval-augmented generation (RAG) pipeline, domain-specific facts, operational rules and guardrails, prior interaction history, and the immediate instructions provided in the prompt itself. Each of these components contributes signals that the model draws on to produce its response. Done well, this enables the model to generate accurate and grounded outputs. Done poorly, it leads to irrelevant answers, degraded accuracy, and unpredictable behavior.

### How LLMs Process Context

To design this context effectively, it helps to understand how an LLM internally processes information. Modern transformer-based models maintain a key–value (KV) cache during inference. Every processed token is stored as a pair of key and value vectors, allowing the model to attend to prior tokens without recomputing them at every step.

Conceptually, this cache is the model's short-term working memory. By feeding the model the right sequence of tokens, we are essentially deciding what gets written into that cache.

### Why Context Must Be Balanced

The need for context arises because the LLM itself has no persistent knowledge beyond its pretrained parameters. It only "knows" what is in the current KV cache. To reason about a domain, we must populate the cache with relevant facts, prior conversation turns, and retrieval results.

However, this is a balancing act. Supplying too much data can overwhelm the model, increase latency, and dilute attention across low-value tokens. Supplying less relevant or contradictory data leads to what can be described as context poisoning: misleading entries in the cache that the model might rely on, resulting in incoherent or incorrect outputs. Supplying too little data, on the other hand, forces the model to guess, which also reduces accuracy and increases hallucinations.

### Intention-Driven Design

The practical implication is that context must be constructed deliberately. Every token included should have a clear purpose. Retrieval pipelines must rank and filter chunks to ensure only high-value content is surfaced. Domain rules and compliance constraints should be encoded in a way that is concise and unambiguous. Prior conversation history should be trimmed to include only the parts that truly influence the current request. Context is not an arbitrary concatenation of text but a curated and testable artifact that directly determines what resides in the KV cache at inference time.

### Comparing to Established Design Methodologies

Traditional software engineering disciplines already offer patterns for structuring logic and data. Object-Oriented Design (OOD) decomposes systems into objects that encapsulate state and behavior. OOD excels at modeling stable domain concepts and relationships, guiding developers to create modular, reusable components.

Context-Driven Design differs in focus and granularity. While OOD shapes how code is structured, Context-Driven Design shapes what information is surfaced to a reasoning engine at runtime. In an OOD system, the central question is: which class or method should handle this responsibility? In a Context-Driven system, the question becomes: which pieces of information should populate the model's working memory right now to achieve accurate reasoning? Context-Driven Design complements existing paradigms by layering a dynamic knowledge assembly process on top of proven software structures.

### Dynamic Application of Context

Other methodologies like Domain-Driven Design (DDD) emphasize creating ubiquitous language and bounded contexts to align code with business domains. Context-Driven Design borrows from that idea but applies it dynamically: instead of building static models that live in source code, we build and update a transient context payload that informs an LLM on demand.

Rather than replacing established methodologies, Context-Driven Design complements them. You still benefit from solid OOD principles in the backend systems that manage storage, retrieval, and orchestration. Those systems supply the components — knowledge chunks, rules, histories — that feed into the context. But the last mile, the assembly of that information into a carefully managed KV cache, is where Context-Driven Design defines a new layer of architectural responsibility.

### Looking Ahead

As systems evolve, this approach could become the backbone of modern LLM architectures. Our early implementations treated prompts as static blocks of text, but production systems now dynamically assemble context at runtime. They monitor output quality, refine retrieval logic through feedback loops, and adjust the composition of context over time. Guardrails are encoded as part of the context itself, rather than being bolted on as post-processing. The result is an application that not only uses the model's capabilities but also respects its operational constraints.

### Conclusion

Treating context as a first-class data structure leads to predictable behavior, lower latency, and reduced hallucination. By thinking in terms of how each piece of information populates the KV cache, architects can ensure that the model's limited working memory is filled with only the most relevant tokens. In doing so, they build systems that are not just powered by LLMs but are designed to make the most of them — systems that are aligned, efficient, and ready for real-world use.""",
    },
    {
      "slug": "from-prompt-loops-to-multi-agent-systems",
      "title": "From Prompt Loops to Multi-Agent Systems: Why the Harness Matters",
      "date": "Jun 3, 2026",
      "read": "6 min",
      "deck": "Where the line between a prompt loop and a multi-agent system actually sits, and what that implies for the harness you have to build underneath.",
      "orig": "https://www.brevian.ai/resources/from-prompt-loops-to-multi-agent-systems",
      "md": """*Based on learnings from building Brevian.*

This post works through where the line between a prompt loop and a multi-agent system actually sits, and what that implies for what you have to build to move from one to the other.

### Defining the two

A prompt loop is one LLM context, iterating. The model thinks, calls a tool, reads the result, thinks again. One conversation, one growing context, until it terminates.

A multi-agent system has multiple LLM contexts that coordinate. Each has its own history, role, and state, and they exchange information somehow: messages, handoffs, or shared artifacts.

The follow-up question is what counts as an "agent." If a prompt loop can call tools, and one of those tools happens to wrap an LLM call internally, is that a multi-agent system?

### Tools vs. agents

A tool is a deterministic function with a fixed code path and a predictable result. An agent is an LLM loop with its own reasoning and, usually, its own tools.

From the caller's perspective, the two are interchangeable. You invoke `research_topic(query)` and you get structured output back. Whether `research_topic` is a Python function calling an API or a full LLM loop with its own scratchpad doesn't matter to the orchestrator.

That symmetry lets you build an orchestrator that sees a flat list of tools, where some of those tools happen to do LLM reasoning internally. The orchestrator's code stays simple. The subagent's context, intermediate tool calls, and scratch work never enter the orchestrator. Only the final result comes back.

Which raises the next question. If the orchestrator can't tell the difference, is this a multi-agent system or a prompt loop?

### Where the actual line is

The cleaner distinction isn't tools vs. agents. It's how many LLM contexts are involved, and whether they persist.

One LLM loop calling deterministic tools is a prompt loop. One LLM loop calling tools that wrap one-shot LLM calls is also a prompt loop. The subagent's context is ephemeral; it exists for one call and disappears. The orchestrator is the only persistent mind.

It becomes multi-agent when there are multiple LLM loops with their own ongoing state, coordinating across turns. A critic that remembers prior critiques. Agents that hand off control with their own state. Parallel agents whose intermediate states need to merge.

The orchestrator-worker pattern sits right on this line. It gets called "multi-agent" because subagents do reasoning, but architecturally it behaves like a prompt loop with rich tools.

### Which side to build on

If the steps are known and deterministic, write a tool. If the steps require judgment, exploration, or chaining multiple actions, write an agent. If you'd write it as a function in normal code, it's a tool. If you'd write it as a prompt, it's an agent.

Default to tools. Every agent boundary adds latency, cost, and a new failure mode. Reach for a subagent only when the work needs reasoning the orchestrator shouldn't be doing itself: context isolation, a specialized prompt, parallel exploration.

A consequence of this is that work that gets called "multi-agent" can often be built as a prompt loop with subagent-backed tools. That keeps the orchestrator simple while still isolating context and specializing prompts per subtask.

### Orchestration patterns

When you do need multiple agents coordinating, a few patterns recur.

- **Orchestrator-worker.** A lead agent decomposes the task, dispatches to stateless workers, and synthesizes results. This is the orchestrator-with-subagent-tools pattern above.
- **Pipeline.** Agents run in sequence, each transforming the previous output. Simple and predictable, with no backtracking. If step three reveals step one was wrong, there is no way back.
- **Parallel fan-out.** Independent subtasks run concurrently, then merge. Good for embarrassingly parallel work. The cost is duplicated effort and merge conflicts.
- **Debate or critic loops.** A proposer and a critic iterate until convergence, or several solvers compete and a judge picks. Improves quality on reasoning-heavy work at significant token cost.
- **Blackboard.** Agents read and write a shared artifact instead of messaging each other. Useful when many contributors update one output. Needs conflict resolution.
- **Event-driven handoff.** Agents trigger each other based on conditions. Closer to a workflow engine than a conversation.

### Why the harness is what you're really building

The moment you introduce a second persistent context, or even subagent-backed tools doing real work, the harness has to do things the simple loop didn't need.

- **Context construction per agent.** Each subagent should get the minimum context to do its job. Passing the orchestrator's full transcript into every worker burns the token budget. The harness needs a way to distill state and build per-agent briefs from a shared store, rather than threading history through call stacks.
- **Structured I/O between agents.** Free-form text between agents drifts and gets misinterpreted. Typed inputs and outputs, schema validation, and retry-on-malformed-output belong in the harness, not in the prompt.
- **Termination.** Loops without stop conditions run forever. Every subagent needs max iterations, token budgets, timeouts, and explicit "done" signals, enforced from outside.
- **Error handling.** Workers fail. The orchestrator needs retry, fallback, and escalation logic. None of this comes from the model.
- **Observability.** A single prompt loop produces one readable trace. A multi-agent system produces a tree of interleaved calls. Per-agent traces with parent-child relationships intact are what make it debuggable.
- **Concurrency.** Parallel fan-out is only useful if the harness can actually run agents in parallel, collect results, and merge them without races in shared state.
- **Budget enforcement.** One runaway subagent can burn a quota quickly. Per-call, per-agent, and per-task limits belong in the harness.

### The takeaway

Choosing between a prompt loop, an orchestrator with subagent-tools, and a fully multi-agent system is a design decision. Whether any of those patterns actually runs well depends on the harness underneath: context construction, structured communication, termination, observability, budget enforcement. Investing in those primitives is what makes the move from a prompt loop to a multi-agent system tractable.""",
    },
    {
      "slug": "why-rag-is-not-enough",
      "title": "Why RAG Is Not Enough",
      "date": "Aug 14, 2026",
      "iso": "2026-08-14",
      "read": "7 min",
      "host": True,
      "modified": True,
      "deck": "RAG answers retrieval questions. Enterprise-wide intelligence needs reasoning over relationships, state, lens and access control, and that requires a knowledge graph.",
      "orig": "https://www.brevian.ai/resources/why-rag-is-not-enough-revenue-intelligence",
      "md": """Retrieval-Augmented Generation was a genuine architectural step forward. By grounding language model outputs in external document corpora rather than parametric memory alone, RAG addressed hallucination and knowledge staleness in a practical, deployable way. The original [Lewis et al. (2020) paper](https://arxiv.org/abs/2005.11401) that coined the term demonstrated strong gains on knowledge-intensive tasks, and the pattern spread quickly across enterprise software.

RAG works, but it was designed for retrieval questions, and a growing class of enterprise applications requires answering reasoning questions.

The retrieval question is: given a query, find the most relevant content. RAG solves this well. The reasoning question is harder: given everything the system knows about an entity, whether that is a deal, a customer, a project or an incident, what does it mean and what should happen next? Answering it requires understanding the relationships between entities, tracking how context evolves across time, and connecting what happened three weeks ago to what should happen before Thursday. RAG was not designed to do that.

### What RAG is doing

A standard RAG pipeline has three stages: documents are chunked and embedded into a vector index, a query retrieves the chunks with the highest semantic similarity, and a language model generates a response conditioned on those chunks. The [ACM survey on GraphRAG methodologies (2024)](https://dl.acm.org/doi/10.1145/3777378) identifies three structural failures in this approach for complex reasoning tasks: it neglects relationships between entities, it loses global context because only a subset of documents is retrieved at a time, and it produces what the authors call the "lost in the middle" problem where relevant information buried in retrieved context gets ignored during generation.

These problems are manageable for a static knowledge base, but they are fundamental for a system trying to reason over a live operational domain.

### The relationship problem

Most of the data these systems reason over is not documents. A CRM record, an incident timeline, a customer's engagement pattern across six meetings, and the connection between a problem surfaced in week two and an objection raised in week four are entities and relationships, and answering questions across them is not a semantic similarity problem. It is a graph traversal problem: find the relationship between these entities and reason across it.

Research on [KG-RAG models (Scientific Reports, 2025)](https://www.nature.com/articles/s41598-025-21222-z) confirms that traditional RAG methods, which rely primarily on unstructured text corpora, are limited in their ability to handle complex relationships and perform multi-hop reasoning. In operational domains, multi-hop reasoning is the baseline requirement: a useful briefing, audit or risk assessment connects what happened to what it means, which requires an architecture that understands relationships, not just text similarity.

This is why [Microsoft's GraphRAG (2024)](https://microsoft.github.io/graphrag/) shifted the conversation. Rather than treating documents as flat text, GraphRAG builds entity-relationship graphs that enable theme-level queries with full traceability. The research example, querying supplier quality issues across relationships and time, has the same structure as querying deal health across stakeholders and conversation history, or service health across incidents and dependencies.

### The statefulness problem

RAG retrieves at query time and stops. Each retrieval is stateless: it has no memory of prior retrievals and no ability to track how context has evolved across interactions. [Research on hybrid retrieval (Preprints.org, 2025)](https://www.preprints.org/manuscript/202512.0359) confirms that dense vectors are complemented by knowledge graphs precisely for structured contexts, because graph structures persist relationships across time in a way that vector indexes do not.

A live process is a sequence of interactions where each one changes the meaning of the ones before it. In sales, a champion who attended every call in weeks one through four and then missed weeks five and six is not surfaced by a similarity search. Detecting the deviation requires a persistent structure that tracks the pattern over time. The same applies to qualification drift, evolving objections, a dependency that keeps appearing in incident timelines, or a customer whose support tickets change tone across a quarter. These are state management problems, not retrieval problems.

### The lens problem

Even when RAG retrieves correctly, it retrieves without context about why. A user asking "what should I cover in this meeting" receives chunks most semantically similar to that query, not chunks most relevant to the current state of the entity the question is about.

At Brevian we address this with a lens constraint: the intelligence layer does not retrieve knowledge generically, it queries everything from the lens of the conversation and the system of record. The same piece of knowledge is more or less relevant depending on what has already been confirmed, what risks have been flagged and where the process stands. A flat retrieval system has no way to apply that constraint, and a structured knowledge graph does.

### The access control problem

One operational dimension that rarely surfaces in technical RAG discussions is content classification. [Research on naive RAG systems (MDPI, 2025)](https://www.mdpi.com/2079-9292/14/11/2102) identifies retrieval inefficiencies, semantic mismatches, and context fragmentation as persistent production problems. In an enterprise corpus there is a harder issue: not all content should be retrieved in all contexts. A pricing document, an internal battlecard, a legal memo and a customer-safe case study can live in the same corpus, but surfacing the wrong one in the wrong context has real consequences.

RAG retrieves by semantic relevance and does not natively understand the difference between internal knowledge and external-safe assets. That distinction needs to be a first-class property of the architecture, with content classified not just by what it says but by what it is and who should see it. A knowledge graph that treats classification as a node property can enforce this at query time, and a flat vector index cannot.

### What changes when the architecture changes

The difference between RAG and a knowledge graph is less about accuracy or recall than about what kinds of questions the system can answer. RAG answers: what content is most relevant to this query? A knowledge graph answers: given everything we know about this entity and this domain, what is the most important thing that needs to happen next? The first is a retrieval problem and the second is a reasoning problem, and in operational domains the second is the one that determines outcomes.

When the architecture is built around relationships rather than retrieval, the outputs change category. What surfaces before a meeting is not the documents most similar to the meeting topic, but a structured assessment of where things stand, what has been confirmed, what gaps remain and what would advance them. What surfaces on Monday morning is not a list of records sorted by date, but a scored assessment of each entity's state with a specific action for the ones that need attention.

Retrieval stays in that architecture as a component. The relationships, the persistent state and the classification around it are what make the reasoning possible.""",
    },
    {
      "slug": "zero-error-tolerance",
      "title": "What Zero-Error Tolerance Actually Means for AI",
      "date": "Mar 4, 2026",
      "iso": "2026-03-04",
      "read": "5 min",
      "host": True,
      "deck": "When your AI handles 25% of U.S. mortgage closings, the error rate in the critical path has to be zero. Why that constraint is architectural, not a tuning problem.",
      "orig": "https://www.linkedin.com/pulse/what-zero-error-tolerance-actually-means-ai-anupreet-walia-hjb4f/",
      "md": """When your AI is handling 25% of U.S. mortgage closings, you're not working on a transaction. You're working on a transaction that, if it leads to an error, could cause delays and losses on someone's home purchase. We're talking about million-dollar transactions where chances of fraud are high, and you're introducing a probabilistic AI solution into the mix.

Error rates in the critical path need to be zero. Not "low." Not "acceptable." Zero.

That's a strange constraint to put on a technology that is, by its nature, probabilistic. Machine learning models don't guarantee outcomes. They produce predictions with confidence scores. So when the business requirement is zero errors in the critical path, you have to design the entire system around that tension rather than pretend it doesn't exist.

We had three AI models: TASHA, Doug, and Ann. They started as a single SageMaker model and evolved into specialized systems that reached 98% accuracy. Which sounds impressive until you remember what the other 2% means at scale. When you're processing tens of thousands of closings, 2% is hundreds of transactions where the AI got it wrong. Transactions tied to real people buying real homes, with real money on the line.

So that 2% didn't get a pass. It got re-verified by humans. Every time. Not as an afterthought, not as a "nice to have" quality check. It was built into the pipeline as a core architectural decision. The system knew what it didn't know, flagged it, and routed it to a human. That boundary between what the AI handles and what gets escalated wasn't a tuning parameter we optimized later. It was the first thing we designed.

That's what people miss about deploying AI in high-stakes environments. The hard part isn't getting to 98% accuracy. The hard part is building the system around the other 2%. The traceability, the fallbacks, the confidence thresholds, the human-in-the-loop routing, all designed so that the 2% never reaches the customer as an unverified output.

Most enterprise AI today doesn't work this way. The system produces an output, the output goes to the user, and the user has no way to know whether this particular answer is in the 98% or the 2%. There's no confidence signal. No trace. No fallback. Just a well-written response that may or may not be right.

I think about this every time I see AI deployed in sales, customer success, operations. Environments where the outputs feed directly into customer-facing conversations and business decisions. The tolerance for error might be higher than mortgage closings, but it's not infinite. A rep who walks into a meeting with wrong account intelligence loses credibility. A manager who commits a forecast based on AI-surfaced pipeline data that missed a key risk loses trust with the board. The errors compound, and because there's no traceability, nobody can diagnose where things went wrong.

The fix is architectural. Not better models, better systems around the models. Traceability built in from the start, not bolted on. Confidence-aware routing so the system knows when to surface an answer and when to say "I don't have enough to be sure." Data provenance so every output connects back to the specific inputs that produced it.

It's harder to build this way. It's slower. But it's the difference between AI that works in a demo and AI that works when the stakes are real.

That's the problem I spend most of my time on.""",
    },
    {
      "slug": "finding-the-craft-again",
      "title": "Finding the Craft Again",
      "date": "Feb 2026",
      "iso": "2026-02-01",
      "read": "6 min",
      "host": True,
      "deck": "Staying close to the craft is not the same as doing it. What it took to close that gap as a founding CTO.",
      "orig": "https://www.linkedin.com/pulse/finding-craft-again-anupreet-walia-ra26c/",
      "md": """At Snapdocs, I was deeply technical but hands-off on code. I did architecture reviews. I participated in technical design. I could hold my own in any systems conversation. But I wasn't writing code. I wasn't in the implementation. I hired strong architects and engineers who'd been building systems and infrastructure for years. My job was to shape direction, not build the thing myself.

At Preset I was running architecture reviews, still in the room for technical decisions. But I'd also moved further into strategic product thinking, the layer above the systems, where you're shaping what gets built, not how. The altitude increased. The distance from the code grew.

I got good at that altitude. Zoom out. Prioritize. Delegate. Trust. Step in at design reviews, not pull requests. It worked. Both companies scaled. I scaled with them. So when I started building something new as a founding CTO, I brought the playbook that had made me successful. And for a while, I struggled with why it wasn't working.

Early-stage startups have a specific kind of silence. Not the silence of things running smoothly, but the silence of things not existing yet. There's no "how we do things here." No inherited architecture. No institutional memory. Every decision you make, or don't make, is foundational, whether you treat it that way or not.

I didn't treat it that way. I treated it like Snapdocs. Like Preset. I'd say things like: "Let's not over-engineer this early." Or: "We can clean this up later." Or: "I trust you to figure out the right approach."

These sound reasonable. They are reasonable in a context where "the right approach" has a default, where someone has pattern-matched this problem before, where there's enough structure for ambiguity to resolve itself. We didn't have that. We had three people and a very hard problem and no one to inherit clarity from.

The thing no one tells you about being hands-off is that it feels like wisdom. You're not in the weeds. You're not micromanaging. You're "letting the team own it." You get to stay at the level of strategy and architecture and vision while others handle implementation. It feels like leverage. It feels like maturity. Which is why it was so disorienting when I started to realize I was the problem.

I don't remember a single moment. It was more like a series of small frictions that didn't add up. Why does this system work this way? "It just evolved that way." Why did we make this tradeoff? "We had to ship." What happens when this breaks? Silence. I kept asking questions that no one had good answers to, and not because the team was weak, but because the questions had never been asked. The decisions had been made in the cracks. There was an abstract void, and nobody could step up to fill it.

I had delegated clarity that didn't exist yet.

Here's the thing that was hard to admit: I used to do this.

Years ago, before the titles and the scaling playbooks and the "operating at altitude," I wrote code. I built systems. I made architectural decisions with my hands, not just my opinions in a review. But I'd been away from it for a long time. And the distance had grown in ways I hadn't fully reckoned with.

The industry had moved. The tools had changed. The patterns I half-remembered were outdated. I wasn't just stepping back into building, I was starting over. Relearning things I once knew, except now I was slower, rustier, and surrounded by people who'd never stopped.

There's a specific kind of humility in that. Not the humility of doing work that feels beneath your title, but the humility of realizing how far you've drifted from the craft. That you stayed close enough to speak the language, but not close enough to do the work. And now you have to earn that back.

I remember sitting with a system design problem and feeling the gap between what I knew I used to be able to do and what I could actually do now. It's a quiet kind of vertigo.

So I went back to the beginning.

Not performatively. Actually. I relearned the fundamentals and how the new patterns worked, how the infrastructure had evolved, what "good" looked like now instead of five years ago. I built things badly and then rebuilt them. I asked questions I was embarrassed to ask. And slowly, I started to find it again. Not the old version, because that was gone. But a new version. Slower in some ways, more deliberate in others. Less clever, more careful. I stopped asking "what's the best practice?" and started asking "what breaks?" I stopped optimizing for speed and started optimizing for traceability. For systems that could explain themselves. For decisions that future-me would be able to reason about.

There's a small irony I think about sometimes. Starting with 0 commits and reaching 1,266 contributions in 2025. The graph gets denser as the year goes on: sparse in the early months, then building through summer, then dark green clusters in Q4 as the new patterns finally start to stick, and 151 commits in the first few weeks of 2026. The hardest work of the last two years hasn't been the kind that shows up cleanly. It's been internal: unlearning patterns, rebuilding intuition, sitting with the discomfort of being a beginner again at something I used to be adjacent to but never fully owned. The green squares are proof it happened. But even without them, I'd know.

I don't think "operator vs. builder" is the right frame. It's more like: different stages need different versions of you. And sometimes the version you need is one you left behind, except when you go looking for it, it's not there anymore. You have to rebuild it.

At Snapdocs, at Preset, staying hands-off on code was leverage. At an early-stage startup, it was abdication dressed up as wisdom.

The role didn't change because I wanted it to. It changed because the company needed something I wasn't giving it. And the hardest part wasn't the work itself, but accepting that staying close to the craft isn't the same as doing it, and that I'd have to close that gap myself.

I'm still in that process. There are days it feels like I'm back. Days it still feels like I'm catching up. But I don't think you get to build something new from altitude alone.

You have to go closer. Even when it costs you the story you had about yourself.""",
    },
]

post_index_items = ""
for po in posts:
    if po.get("host"):
        href, arrow = f"{po['slug']}.html", ""          # hosted on this site
    else:
        href, arrow = po['orig'], " ↗"                  # link out (Brevian / LinkedIn)
    post_index_items += f'''<div class="post-item">
      <span class="date">{po["date"]}</span>
      <h3><a href="{href}">{po["title"]}{arrow}</a></h3>
      <p>{po["deck"]}</p></div>\n'''

writing_index = f'''<section style="border:none"><div class="wrap">
  <p class="eyebrow">Writing</p>
  <h1>Essays</h1>
  <p style="color:var(--muted);max-width:620px">Pieces on AI architecture, context engineering, building production multi-agent systems, and the craft of engineering.</p>
  <div class="post-list">{post_index_items}</div>
</div></section>'''
write("writing/index.html", page("Writing · Anupreet Walia", writing_index, "writing", 1,
      "Essays on AI architecture, context engineering, and multi-agent systems by Anupreet Walia.",
      cpath="writing/index.html"))

# Render hosted essays as full pages; link-out posts get a redirect stub.
for po in posts:
    if po.get("host") and po.get("md"):
        body_html = markdown.markdown(po["md"], extensions=["extra"])
        orig = po.get("orig")
        venue = ("LinkedIn" if "linkedin.com" in orig else "Brevian") if orig else ""
        if po.get("modified"):
            pub_verb = "Modified from the original published"
        elif po.get("first_here"):
            pub_verb = "Also published"
        else:
            pub_verb = "Originally published"
        origin_line = f' {pub_verb} on <a href="{orig}">{venue}</a>.' if orig else ""
        meta_venue = "" if po.get("modified") else venue
        meta_bits = " · ".join(x for x in [po["date"], (po.get("read","") + " read" if po.get("read") else ""), meta_venue] if x)
        hero = f'<img class="post-hero" src="../assets/{po["image"]}" alt="{po.get("image_alt","")}">' if po.get("image") else ""
        art = f'''<article><div class="wrap">
  <a class="back" href="index.html">← all writing</a>
  <div class="post-meta">{meta_bits}</div>
  <h1>{po["title"]}</h1>
  <p class="deck">{po["deck"]}</p>
  {hero}
  {body_html}
  <div class="author-box">
    <strong>Anupreet Walia</strong> is CTO &amp; Co-Founder of Brevian.{origin_line}
  </div>
</div></article>'''
        article_ld = ('<script type="application/ld+json">\n{"@context":"https://schema.org",'
            '"@type":"Article","headline":' + json.dumps(po["title"]) +
            ',"author":{"@type":"Person","name":"Anupreet Walia"},'
            '"datePublished":"' + po.get("iso", "2026") + '",'
            '"url":"' + BASE + "/writing/" + po["slug"] + '.html",'
            '"publisher":{"@type":"Organization","name":"Anupreet Walia"}}\n</script>\n')
        write(f"writing/{po['slug']}.html",
              page(po["title"] + " · Anupreet Walia", art, "writing", 1, po["deck"][:150],
                   cpath=f"writing/{po['slug']}.html", og_type="article", head_extra=article_ld,
                   og_image=(BASE + "/assets/" + po["image"]) if po.get("image") else None))
    else:
        write(f"writing/{po['slug']}.html",
              f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={po['orig']}">
<link rel="canonical" href="{po['orig']}">
<title>Redirecting…</title></head>
<body style="font-family:sans-serif;padding:40px">Redirecting to <a href="{po['orig']}">{po['title']}</a>…</body></html>''')

# ---------------------------------------------------------------- RESEARCH / BATCHDAG
research_body = '''<section style="border:none"><div class="wrap">
  <a class="back" href="index.html">← home</a>
  <p class="eyebrow">Research · Preprint</p>
  <h1>BatchDAG: LLM-Planned Execution Graphs for Scalable Ad-Hoc Analysis Over Enterprise Data</h1>
  <p style="color:var(--muted);font-family:var(--mono);font-size:14px">Anupreet Walia · Brevian.ai · 2026 · <a href="https://arxiv.org/abs/2607.18241">arXiv:2607.18241</a></p>

  <div class="btn-row">
    <a class="btn primary" href="https://arxiv.org/abs/2607.18241">Read the paper on arXiv →</a>
    <a class="btn" href="assets/BatchDAG_Walia.pdf">PDF</a>
  </div>

  <div class="abstract">
  <strong>Abstract.</strong> Large language models excel at analyzing individual documents but break down when users ask exhaustive, cross-entity analytical questions over enterprise-scale datasets. For example, &ldquo;Did our account executives open every meeting with effective discovery questions?&rdquo; across 50,000 recorded meetings. The single-agent tool-calling paradigm fails at this scale for three compounding reasons: context window overflow, loss of per-entity attribution in global top-N retrieval, and linear wall-clock time growth from sequential tool calls. We present <strong>BatchDAG</strong>, a system in which an LLM generates a typed directed acyclic graph (DAG) of operations (SQL queries, semantic searches, in-memory transforms, parallel fan-outs, and single-shot analyses) that a deterministic execution engine then evaluates with topological-wave parallelism. Structured JSON rows flow between steps (never prose summaries), enabling proper joins, filters, and grouping. A key optimization, <em>entity-aware batching</em>, groups input rows by their logical entity before fan-out, reducing LLM calls by up to 47&times; while preserving per-entity attribution. BatchDAG has been deployed in production at Brevian.ai, processing analytical queries over corpora of 50,000+ meetings and 3,000+ sales opportunities in under 60 seconds.
  </div>

  <div class="stat-grid">
    <div class="stat"><div class="num">47×</div><div class="lbl">fewer LLM calls via entity-aware batching</div></div>
    <div class="stat"><div class="num">&lt;60s</div><div class="lbl">per query over 50K+ meetings</div></div>
    <div class="stat"><div class="num">98.8%</div><div class="lbl">valid-DAG planning rate (300 calls)</div></div>
    <div class="stat"><div class="num">77%</div><div class="lbl">transcript evidence rate (vs 46–60% baselines)</div></div>
  </div>

  <h2>The problem</h2>
  <p>Tool-augmented LLM agents (ReAct, Toolformer, LangChain, LlamaIndex) perform well on queries targeting individual entities or small document sets. But enterprise users increasingly ask exhaustive, cross-entity analytical queries that require processing hundreds to thousands of entities, each needing its own retrieval, contextual analysis, and per-entity attribution: &ldquo;analyze every deal to see if security insurance was covered,&rdquo; or &ldquo;for each meeting, check if the key stakeholder negotiated on price.&rdquo; These expose three limits of the single-agent loop: context window overflow, loss of per-entity attribution under global top-N search, and linear wall-clock growth.</p>

  <h2>The approach</h2>
  <p>BatchDAG decomposes the problem into two phases: an LLM <strong>planner</strong> that generates a typed DAG of operations from a natural-language query, and a deterministic <strong>execution engine</strong> that evaluates the DAG with topological-wave parallelism, structured data flow, and entity-aware batching. Each step is one of six typed operations (<code>sql</code>, <code>search</code>, <code>transform</code>, <code>fan_out</code>, <code>analyze</code>, <code>compare</code>), four of which require zero LLM calls during execution. Only <code>fan_out</code> and <code>analyze</code> invoke the model, and entity-aware batching minimizes that cost by grouping rows by their logical entity (meeting, deal, account) before fan-out.</p>

  <h2>Key contributions</h2>
  <ul>
    <li>A typed DAG formalism for decomposing ad-hoc analytical queries into composable operations with structured inter-step data flow.</li>
    <li>An entity-aware batching algorithm achieving up to 47&times; reduction in LLM calls versus row-level batching.</li>
    <li>A goal-based planning prompt architecture that outperforms both exhaustive-rules and few-shot example approaches.</li>
    <li>A production deployment report on cost, latency, and correctness over enterprise-scale data (50K+ meetings, 3K+ opportunities).</li>
    <li>A controlled evaluation showing automatically generated DAG pipelines match expert-designed baselines, with superior provenance and 27% fewer hallucinations via structured intermediates.</li>
  </ul>

  <h2>Why structured intermediates matter</h2>
  <p>Steps pass structured JSON rows between them, never prose summaries. This is the single most important architectural decision in BatchDAG. When intermediate results were summarized in natural language, downstream steps hallucinated data and lost attribution. Structured rows are less expressive but fully composable: they support real database-style joins, filters, and grouping, and they preserve the provenance chain from source data to final answer.</p>

  <div class="btn-row">
    <a class="btn primary" href="https://arxiv.org/abs/2607.18241">Read the paper on arXiv →</a>
    <a class="btn" href="assets/BatchDAG_Walia.pdf">PDF</a>
    <a class="btn" href="https://scholar.google.com/citations?user=_PfGUfcAAAAJ&hl=en">Google Scholar</a>
  </div>
  <p style="color:var(--faint);font-size:13px;margin-top:18px;font-family:var(--mono)">Preprint · <a href="https://arxiv.org/abs/2607.18241">arXiv:2607.18241</a></p>
</div></section>'''
write("research.html", page("BatchDAG · Anupreet Walia", research_body, "research", 0,
      "BatchDAG: LLM-planned execution graphs for scalable ad-hoc analysis over enterprise data. Preprint (arXiv:2607.18241) by Anupreet Walia, Brevian.ai.",
      cpath="research.html", og_type="article", head_extra=RESEARCH_LD))

# ---------------------------------------------------------------- PATENTS
pat_nums = [
    ("US-11183268-B2", "https://patents.google.com/patent/US11183268B2/en"),
    ("US-10861587-B2", "https://patents.google.com/patent/US10861587B2/en"),
    ("US-20210174895-A1", "https://patents.google.com/patent/US20210174895A1/en"),
    ("US-20200134136-A1", "https://patents.google.com/patent/US20200134136A1/en"),
    ("US-20200104463-A1", "https://patents.google.com/patent/US20200104463A1/en"),
    ("US-20200105365-A1", "https://patents.google.com/patent/US20200105365A1/en"),
]
nums_html = " &nbsp;·&nbsp; ".join(f'<a href="{u}">{n}</a>' for n,u in pat_nums)
patents_body = f'''<section style="border:none"><div class="wrap">
  <a class="back" href="index.html">← home</a>
  <p class="eyebrow">Patents</p>
  <h1>Patents</h1>
  <p style="color:var(--muted);max-width:620px">Granted patents and published applications from my work at Helix on cross-network genomic data interfaces.</p>

  <div class="patent">
    <h3>Genomic Network Service / Cross-Network Genomic Data User Interface</h3>
    <p class="meta">A genomic update system that generates a user interface from network pages based on variant data matching a user&#39;s genetic variant data, presenting content from trusted, linked pages with visualizations for interaction on a device. Assignee: Helix.</p>
    <p class="meta" style="margin-top:14px;color:var(--ink)"><strong>Patent &amp; application numbers</strong></p>
    <p class="nums">{nums_html}</p>
  </div>

  <p style="color:var(--faint);font-size:13px;margin-top:18px;font-family:var(--mono)">Links resolve to Google Patents.</p>
</div></section>'''
write("patents.html", page("Patents · Anupreet Walia", patents_body, "patents", 0,
      "Patents by Anupreet Walia: cross-network genomic data user interface (Helix).",
      cpath="patents.html"))

# ---------------------------------------------------------------- RESUME
resume_roles = [
    ("CTO &amp; Co-Founder", "Brevian AI (Felicis)", "San Mateo, CA", "12/02/2024 – Present",
     "AI sales intelligence built on structured knowledge and multi-agent LLM systems.",
     ["Set product and technical strategy around structured sales intelligence, using a shared knowledge model to connect customer, product, meeting, and CRM data.",
      "Took the strategy from concept to product, shipping Meeting Prep, Live Assist, Sales Coaching, and CRM Updates and using customer feedback to drive the roadmap.",
      "Designed and built the Knowledge Engine, a structured graph connecting products, features, pain points, stakeholders, objections, and deal context, providing a common data and reasoning layer across products.",
      "Designed the multi-agent architecture with three agent types, 10+ orchestrated tools, recursive tool calling, and context management across OpenSearch, PostgreSQL, and GPT-4o/5.1.",
      "Built the engineering operating model, including hiring, engineering principles, and an L3–L8 leveling ladder."]),
    ("VP of Engineering", "Baseten (Conviction)", "San Francisco, CA", "03/19/2024 – 11/30/2024",
     "ML infrastructure for deploying and serving AI models at scale.",
     ["Led engineering for developer experience and model observability as Baseten expanded its inference platform.",
      "Shipped model-serving capabilities on TRT-LLM and vLLM with a Python/Kubernetes platform and launched the company&#39;s self-hosted enterprise offering.",
      "Drove SOC2 certification to support enterprise adoption."]),
    ("VP of Engineering", "Preset (a16z, Redpoint)", "San Mateo, CA", "02/22/2021 – 03/11/2024",
     "Cloud analytics platform built on Apache Superset.",
     ["Led product and engineering through Preset&#39;s transition from an open-source project into a commercial cloud platform, launching SaaS, Hybrid Cloud, and Embedded products.",
      "Scaled engineering from 20 to 60+, building frontend, platform, data engineering, and infrastructure teams to support the company&#39;s growth.",
      "Built the infrastructure and operating practices required for multi-tenant SaaS, enterprise security and compliance, and multiple deployment models."]),
    ("Director of Engineering / Interim VPE", "Snapdocs (Sequoia, Y Combinator)", "San Francisco, CA", "09/24/2018 – 02/19/2021",
     "Digital mortgage closing platform.",
     ["Led engineering through ~8&times; revenue growth, scaling the organization from 11 to 100 engineers and building frontend, platform, data engineering, data science, and infrastructure teams, supported by standardized hiring frameworks, interview processes, and evaluation rubrics.",
      "Built the platform and engineering practices required to support the increase in customers and transaction volume, with investments in reliability, infrastructure, and developer productivity.",
      "Led QA, DevOps, Data Science, Engineering, and Core Platform during this period."]),
    ("Engineering Manager", "Helix (KPCB, DFJ)", "San Carlos, CA", "11/14/2016 – 09/21/2018",
     "Personal genomics platform.",
     ["Built the mobile engineering function as Helix expanded its genomics platform into a consumer product and partner marketplace.",
      "Shipped Helix&#39;s first native iOS application and built the platform iOS SDK, marketplace APIs, and OAuth2 framework used by partners across the Helix ecosystem."]),
    ("Tech Lead", "Microsoft", "San Francisco, CA", "02/23/2015 – 11/11/2016",
     "",
     ["Built Office prototypes using machine learning and an iOS application using Microsoft Band biometrics for stress detection with Microsoft Research.",
      "Selected for Microsoft&#39;s High Potential (HiPo) program."]),
    ("Computer Scientist", "Adobe", "San Francisco, CA", "02/09/2009 – 02/20/2015",
     "",
     ["Built full-stack applications, APIs, and data pipelines for Typekit.",
      "Optimized Flash Player and AIR runtime on Android for battery, memory, and rendering performance."]),
]
resume_exp = ""
for title, org, loc, when, blurb, bullets in resume_roles:
    blurb_html = f'<p class="org-blurb">{blurb}</p>' if blurb else ""
    bl = "\n".join(f"<li>{b}</li>" for b in bullets)
    resume_exp += f'''<div class="cv-role">
  <div class="cv-head"><h3>{title} · <span class="org">{org}</span></h3><span class="cv-when">{when}</span></div>
  <div class="cv-loc">{loc}</div>
  {blurb_html}
  <ul>{bl}</ul>
</div>'''

resume_body = f'''<section style="border:none"><div class="wrap">
  <a class="back" href="index.html">← home</a>
  <p class="eyebrow">Résumé</p>
  <h1>Anupreet Walia</h1>
  <p style="color:var(--muted);font-weight:600;margin-top:2px">Engineering Executive · Technical Co-Founder</p>
  <p style="color:var(--muted);font-family:var(--mono);font-size:13.5px">San Mateo, CA · <a href="https://www.linkedin.com/in/anupreetwalia/">LinkedIn</a> · <a href="https://github.com/anusual">GitHub</a></p>
  <div class="btn-row"><a class="btn" href="assets/Anupreet_Walia_Resume_2026.pdf" download>Download PDF</a></div>

  <h2>Summary</h2>
  <p>Engineering executive and technical founder with 19+ years building products and engineering organizations from 0→1 through scale. I lead product and engineering strategy, design the technical and organizational systems required to execute it, and remain hands-on when the work requires it. Experience across AI systems, developer platforms, distributed systems, and engineering organizations scaling to 100+ people.</p>

  <h2>Experience</h2>
  {resume_exp}

  <h2>Education</h2>
  <p><strong>M.S., Computer Science</strong>, Georgia Institute of Technology. IRA Hardin Fellowship Recipient.</p>

  <h2>Technical depth</h2>
  <p><strong>AI Systems:</strong> Multi-agent architectures, LLM orchestration, knowledge graphs, RAG/GraphRAG, retrieval and context engineering.</p>
  <p><strong>Distributed Systems:</strong> Multi-tenant SaaS, data platforms, ML inference infrastructure, reliability and observability.</p>
  <p><strong>Platforms:</strong> Developer platforms, APIs and SDKs, enterprise integrations, cloud infrastructure.</p>
  <p><strong>Engineering Organizations:</strong> 0→1 teams, organization scaling, hiring systems, leveling, and engineering operating practices.</p>

  <h2>Selected technical work</h2>
  <p><strong><a href="research.html">BatchDAG</a></strong>: LLM-planned execution graphs for scalable ad-hoc analysis over enterprise data. Deployed in production at Brevian. Preprint: <a href="https://arxiv.org/abs/2607.18241">arXiv:2607.18241</a>.</p>
  <p><strong><a href="writing/index.html">Brevian Engineering</a></strong>: Writing on context engineering, multi-agent harnesses, knowledge graphs, and the MCP intelligence layer.</p>
  <p><strong><a href="patents.html">Patents</a></strong>: Six granted patents / applications from Helix on cross-network genomic data interfaces.</p>
  <p><strong><a href="https://github.com/anusual">GitHub</a></strong>: Recent hands-on engineering work under @anusual, with earlier work under <a href="https://github.com/anupreet">@anupreet</a>.</p>
</div></section>'''
write("resume.html", page("Résumé · Anupreet Walia", resume_body, "resume", 0,
      "Résumé of Anupreet Walia, engineering executive and technical co-founder.",
      cpath="resume.html"))

# ---------------------------------------------------------------- robots + sitemap
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")

today = time.strftime("%Y-%m-%d")
urls = ["", "research.html", "writing/index.html", "patents.html", "resume.html"]
urls += [f"writing/{po['slug']}.html" for po in posts if po.get("host")]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    loc = BASE + "/" + u
    pr = "1.0" if u == "" else "0.8"
    sm.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
sm.append("</urlset>")
write("sitemap.xml", "\n".join(sm))

print("DONE")
