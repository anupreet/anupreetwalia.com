# -*- coding: utf-8 -*-
"""Static site generator for anupreetwalia.com"""
import os, time, json, markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
VER = int(time.time())   # cache-busting stamp appended to asset URLs each build
BASE = "https://anupreetwalia.com"   # canonical origin for SEO

PERSON_LD = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Anupreet Walia","url":"https://anupreetwalia.com","jobTitle":"CTO & Co-Founder","worksFor":{"@type":"Organization","name":"Brevian AI"},"description":"Engineering executive and technical co-founder. CTO & Co-Founder of Brevian AI. 20+ years building AI products and scaling teams across AI/ML systems, knowledge graphs, RAG, and agentic AI.","sameAs":["https://www.linkedin.com/in/anupreetwalia/","https://github.com/anusual","https://scholar.google.com/citations?user=_PfGUfcAAAAJ"],"address":{"@type":"PostalAddress","addressLocality":"San Mateo","addressRegion":"CA","addressCountry":"US"}}
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
    ("10/2024 to now", "CTO &amp; Co-Founder", "Brevian AI",
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
  <p class="eyebrow">Engineering executive · Technical co-founder</p>
  <h1>Anupreet Walia</h1>
  <p class="lede">I build AI products from scratch and scale the teams and platforms behind them. Currently CTO &amp; Co-Founder of Brevian AI.</p>
  <p class="sub">20+ years across AI/ML systems, knowledge graphs, RAG, and agentic AI, from founding teams to orgs of 100+ engineers at venture-backed startups (Sequoia, a16z, Y Combinator). This is where my technical work, writing, research, and patents live in one place.</p>
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

write("index.html", page("Anupreet Walia · Engineering executive &amp; technical co-founder",
      home_body, "home", 0,
      "Anupreet Walia, CTO &amp; Co-Founder of Brevian AI. Technical product, writing, research (BatchDAG), and patents in one place.",
      cpath="", head_extra=PERSON_LD))

# ---------------------------------------------------------------- POSTS
posts = [
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
      "deck": "Skill-based interviewing gives us a way to change hiring as engineering itself changes. How I am updating the loop — coding with agents, feature design through rollout — now that coding agents are part of the job.",
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

As implementation becomes faster, teams can build more features and more variations of a feature in the same amount of time. That increases the importance of being able to test those features cheaply and safely. If experimentation and rollout remain expensive, the organization simply moves the bottleneck from implementation to validation.

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
      "slug": "brevian-mcp",
      "title": "Introducing Brevian MCP: What If You Could Ask Your Sales Data Anything?",
      "date": "May 11, 2026",
      "read": "5 min",
      "deck": "New intelligence, synthesized from every layer of your sales data, delivered as operational playbooks you can act on this week.",
      "orig": "https://www.brevian.ai/resources/brevian-mcp-what-if",
      "md": """**Not search results. Not dashboards. New intelligence, synthesized from every layer of your sales data.**

A sales leader sat down with Claude last week, connected to Brevian MCP, and typed a question:

> "Find meetings attached to lost opps where a competitor was in place and the client revealed their renewal date to us. Table with opp, owner, competitor, and competitor renewal date."

What came back was not a list of deals. It was a competitive renewal calendar. Eight opportunities, each with the specific competitor in place, the exact renewal date the prospect mentioned on a call, and the transcript-verified quote where they said it. The output included outreach timing recommendations: which deals have a re-engagement window opening now, which ones to queue for next quarter, and which ones to skip because the prospect just signed a fresh three-year contract with the incumbent.

That calendar did not exist anywhere in the CRM. Nobody had logged competitor renewal dates as a structured field. The intelligence was assembled in seconds from signals scattered across months of recorded conversations, matched to deal records, and organized into something a team could execute against immediately.

That is what Brevian MCP does. And it is live today.

### The Question That Changes Everything

Every sales leader carries a mental list of questions they would love to answer but never have time to research. The kind that require pulling CRM data, cross-referencing meeting records, reading transcripts, checking coaching reports, and assembling it all into something usable. An afternoon of work, minimum. The high-value questions that are not easily answerable but could unlock important strategies.

Brevian MCP eliminates that tradeoff. It connects your full Brevian intelligence surface to Claude, ChatGPT, and any MCP-compatible AI platform. Not as a data feed. As an intelligence layer that an AI agent can reason across, combining signals from your CRM, your transcripts, your coaching data, and your meeting history to produce insights that have never existed before.

### From Question to Playbook in Seconds

Here is what that looks like when you push it further. A sales leader asked:

> "Find non-renewal lost opps from the last year, over $20,000, where meetings focused on a core product line. Rank by most promising re-engagement using the coaching scoring system. Top 20 with opp, owner, why it is promising, and re-engagement advice."

What came back was a twenty-deal resurrection playbook. Not a sorted list. A scored, ranked analysis.

The system built a four-dimension scoring framework on the fly: buyer commitment signals, active blockers (how defined and resolvable they are), buying-process state at time of loss, and champion strength. Each deal scored 1 to 3 on every dimension, max 12. The top-ranked deal scored a perfect 12. The customer had said "this is a lock" on a recorded call, quotes had been generated, end-of-quarter credits applied, and they were asking for start dates.

Every deal in the table came with two things: a one-sentence explanation of why it is promising, grounded in specific transcript evidence, and a one-sentence re-engagement recommendation tailored to that deal's situation.

But the system did something else nobody asked for. It removed three deals that looked strong on CRM data but whose transcripts revealed disqualifying signals. One prospect had committed to a competitor on a recorded call. Another had gone dark on a board-approval meeting. A third had explicitly pushed the decision to next fiscal year due to budget cuts. The AI read the transcripts, identified the signals, and pulled those deals from the ranked list before presenting it.

And it flagged a data quality issue: twelve of the twenty candidates had no indexed transcript content, which capped their scores. The system told you exactly where its confidence was high and where it was limited by coverage gaps.

That entire output — the scoring methodology, the ranked table, the disqualifications, the data quality caveat — was generated in the time it takes to read this paragraph.

### What Just Happened

An AI agent just did the work of a senior sales analyst. It filtered your pipeline. It read your transcripts. It scored your deals using signals from coaching data. It synthesized a prioritized playbook with specific, actionable recommendations for each opportunity. It identified and removed false positives. It told you where the data was strong and where it was thin.

The playbook it produced has never existed in any system. No dashboard generates it. No report template covers it. It was created in the space between the question and the answer, because for the first time, an AI agent could reason across every layer of your sales intelligence simultaneously.

That is the shift. Not better search. Not faster dashboards. The ability to ask a question your organization has never asked before and get back operational intelligence you can act on today.

### Why MCP Makes This Possible

MCP (Model Context Protocol) is the open standard AI platforms adopted in 2025 for connecting assistants to external tools. Claude, ChatGPT, Cursor, and a growing list of platforms all speak it. One server, one authentication model, and every AI platform your team uses gets access to the same intelligence layer.

Brevian has spent years building derived intelligence on top of raw sales data. Deal reports with scored dimensions and timestamped evidence. Qualification tracking across every conversation. Semantic search that understands what a conversation is about. Stakeholder engagement signals. MCP is what opens all of that to any AI agent, so it can combine those signals in ways we never pre-designed and produce insights we never anticipated.

The queries in this post were not features we built. They were questions a sales leader asked. The intelligence was generated on the fly. That is the point.

### Five Minutes to Your First Question

Mint a Personal Access Token in Brevian's settings, add Brevian as a custom connector in Claude or ChatGPT, and paste the token when prompted. Your full intelligence surface goes live.

Security ships with the product. Every token hashed at rest. Every query audited. Access scoped to user, organization, and workspace. Token revocation cascades instantly to every derived session. Phase 1 is read-only by design.

### Your Questions, Not Ours

The competitive renewal calendar and the resurrection playbook are two examples. Your team will have hundreds of their own.

What if you could identify every deal where a champion went silent and cross-reference it with their last coaching report? What if you could find every meeting where your team's competitive positioning diverged from the trained battlecard and rank those gaps by deal value? What if you could map every objection a prospect raised across six months of calls and see which ones your team handled and which ones they never addressed?

Every one of those produces intelligence that does not exist until the question is asked. That is what Brevian MCP unlocks. And the best questions will be the ones we have not thought of yet.""",
    },
    {
      "slug": "knowledge-engine-vs-conversation-intelligence",
      "title": "What a Knowledge Engine Does That Conversation Intelligence Doesn't",
      "date": "Mar 10, 2026",
      "read": "5 min",
      "deck": "Most sales managers have more call recordings than they have time to watch. That is not an information problem. It is a structure problem.",
      "orig": "https://www.brevian.ai/resources/knowledge-engine-vs-conversation-intelligence",
      "md": "",
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
  <p style="color:var(--muted);max-width:620px">Pieces on AI architecture, context engineering, building production multi-agent systems, and the craft of engineering. Published on the Brevian blog and LinkedIn.</p>
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
        pub_verb = "Also published" if po.get("first_here") else "Originally published"
        origin_line = f' {pub_verb} on <a href="{orig}">{venue}</a>.' if orig else ""
        meta_bits = " · ".join(x for x in [po["date"], (po.get("read","") + " read" if po.get("read") else ""), venue] if x)
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
  <p>Engineering executive and technical founder with 20+ years building products and engineering organizations from 0→1 through scale. I lead product and engineering strategy, design the technical and organizational systems required to execute it, and remain hands-on when the work requires it. Experience across AI systems, developer platforms, distributed systems, and engineering organizations scaling to 100+ people.</p>

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
  <p><strong><a href="research.html">BatchDAG</a></strong> — LLM-planned execution graphs for scalable ad-hoc analysis over enterprise data. Deployed in production at Brevian. Preprint: <a href="https://arxiv.org/abs/2607.18241">arXiv:2607.18241</a>.</p>
  <p><strong><a href="writing/index.html">Brevian Engineering</a></strong> — Writing on context engineering, multi-agent harnesses, knowledge graphs, and the MCP intelligence layer.</p>
  <p><strong><a href="patents.html">Patents</a></strong> — Six granted patents / applications from Helix on cross-network genomic data interfaces.</p>
  <p><strong><a href="https://github.com/anusual">GitHub</a></strong> — Recent hands-on engineering work under @anusual, with earlier work under <a href="https://github.com/anupreet">@anupreet</a>.</p>
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
