---
url: https://youtu.be/Dli5slNaJu0
title: "Pi: A Minimal Extensible Coding Agent — Mario Zechner"
author: Mario Zechner (@badlogic)
date: 2026 (apresentação em conferência)
captured_at: 2026-04-08
source: youtube-transcript skill
---

# Transcrição: Pi Coding Agent (Mario Zechner)

> Fonte imutável. Não editar após captura.

[0:00] Hi, my name is Mario. I hail from the
[0:00] land of Arnold Schwarzenegger. [...]
[0:00] the reason I'm here is actually another
[0:00] person which is here in cognto today
[0:00] let's call him uh Pineberger [laughter]
[0:00] um back in 2025 I think somewhere around
[0:00] April he told me and Armen Rona which
[0:00] you might also know Flask fame and Sentry
[0:00] fame. Dude, those coding agents, they
[0:00] actually work now. And I was like, oh,
[0:00] shut the [..] up. [...] and a month later,
[0:00] we teamed up at this flat for 24 hours
[0:00] overnight and just let ourselves uh get
[0:00] um immersed by the clankers, by the wipe
[0:00] coat, and by the wipe slop. And since
[0:00] then, none of us have really were
[0:00] sleeping anymore, basically. So we're
[0:00] building stuff, lots of stuff, most of
[0:00] which we actually never used because
[0:00] that's the new thing in 2025/26.
[0:00] We build a lot of stuff, but we don't
[0:00] build a lot of stuff we actually use.
[0:00] Uh and eventually that culminated in me
[0:00] thinking, I hate all the existing coding
[0:00] agents or harnesses. How hard can it be
[0:00] to write one myself?
[0:00] [...] pi in the beginning there was cloud
[0:00] code actually there was copy and pasting
[0:00] from chatgpt right we all did that in
[0:00] the beginning 2023 [...]
[0:00] And then there was cloud code. Um I think
[0:00] they released it in November actually as
[0:00] a beta in 2024 but it really only became
[0:00] used uh more early February/March 2025.
[0:00] And I was like I love it. It's awesome.
[0:00] [...] and they basically created the entire
[0:00] genre. [...] they just said we
[0:00] reinforcement trained our models to just
[0:00] use file tools, bash tools to explore
[0:00] your codebase ad hoc and find the places
[0:00] that it needs to find to understand the
[0:00] code and then modify the code. And this
[0:00] worked so well that yeah we stopped
[0:00] sleeping because we all of a sudden
[0:00] could produce so much more code than we
[0:00] could before by hand.
[0:00] [...] then they fell into the trap and to
[0:00] which most of us us probably fall. The
[0:00] clankers can write so much code why not
[0:00] just let it write all the features you
[0:00] could ever imagine, right? [...] and
[0:00] eventually you end up with [...] a
[0:00] spaceship and cloud code is now a
[0:00] spaceship. It does so many things that
[0:00] you actually probably ever used like 5%
[0:00] of what it offers. You only know about
[0:00] 10% in total. And the rest, the 90%
[0:00] that's left over, that's kind of like
[0:00] the dark matter of AI and agents. Nobody
[0:00] knows what it's actually doing.
[0:00] [...] I eventually found that cloud code
[0:00] was not a good tool when it comes to
[0:00] observability and actually managing your
[0:00] context.
[0:00] [...] I believe as a consequence of the UI
[0:00] design, um, they need to reduce the
[0:00] amount of visibility you have. [...]
[0:00] there is zero model choice obviously
[0:00] because it's a anthropic native tool [...]
[0:00] there's almost zero extensibility [...]
[0:00] if you compare it to what PI allows you
[0:00] to do, it's it's not as deeply integrated.
[0:00] [...] So then I was looking around for
[0:00] options [...] AMP [...] open code [...]
[0:00] the problem with open code is that it's
[0:00] also not very good at managing your
[0:00] context. Uh for example, on each turn
[0:00] it's calling session compaction. Prune
[0:00] which does the following. It prunes all
[0:00] two results um before the last 40,000
[0:00] tokens. Now, who here knows what prompt
[0:00] caching is, right? What does this do to
[0:00] your prompt cache?
[0:00] [...] every message becomes its own JSON
[0:00] file on disk. That indicates to me that
[0:00] there wasn't a lot of thought put into
[0:00] the architecture of the whole thing.
[0:00] [...] open code comes with LSP language
[0:00] server protocol support out of the box.
[0:00] Coming back to context engineering. [...]
[0:00] if you then turn around and say, "Hey,
[0:00] dear LSP server, I just edited one line
[0:00] in this file. Is it broken?" Then the
[0:00] LSP ser yes yes it's really broken [...]
[0:00] and what this feature does it it then
[0:00] injects this error directly after the
[0:00] tool call as a kind of feedback to the
[0:00] model [...] and the model is like what
[0:00] the [..] dude I'm I'm not done editing
[0:00] things why are you telling me this [...]
[0:00] if you do this often enough the model
[0:00] will just give up and that leads to very
[0:00] bad outcomes um so I'm not a fan of LSP
[0:00] [...] There's natural synchronization
[0:00] points where you want to have linting
[0:00] and type checking and all of that and
[0:00] that is when the agent thinks it's done
[0:00] only then.
[0:00] [...] So, so this was my observations
[0:00] with regards to existing coding harnesses.
[0:00] [...] Two thesises based on all of these
[0:00] findings. We are in the messing around
[0:00] and finding out stage and nobody has any
[0:00] idea what the perfect coding agent
[0:00] should look like or what the perfect
[0:00] coding harness should look like. [...]
[0:00] And the second thing is we need better
[0:00] ways to mess around uh with coding
[0:00] agents. That is we need them to be able
[0:00] to self-modify themselves and become
[0:00] malleable. So we can quickly experiment
[0:00] with ideas [...]
[0:00] So the basic idea was and it's very
[0:00] simple and not rocket science. Strip
[0:00] away everything and build a minimal
[0:00] extensible core [...] with some creature
[0:00] of comforts. It's not a blank slate.
[0:00] So that's pi. Um and the general motto
[0:00] is uh adapt your coding agent to your
[0:00] needs instead of the other way around.
[0:00] It comes with four packages. An AI
[0:00] package which is basically just a simple
[0:00] abstraction over multiple providers [...]
[0:00] Um the agent core which is just a
[0:00] generalized agent loop with tooling
[0:00] locations verification and so on and so
[0:00] forth. Then streaming um uh a terminal
[0:00] user interface that's like 600 lines of
[0:00] code [laughter] and works really well
[0:00] surprisingly [...]
[0:00] This is the entire system prompt.
[0:00] There's nothing more there compared to
[0:00] other coding harnesses system prompts
[0:00] that's in tokens. Yeah, it turns out
[0:00] frontier models are heavily RL trained
[0:00] to know what the coding agent is. So
[0:00] why do you keep telling them that
[0:00] they're a coding agent and how they
[0:00] should do coding tasks, right?
[0:00] [...] it only has four tools read a file
[0:00] write a file edit a file and bash bash
[0:00] is all you need what's not in there no
[0:00] MCP no sub agents no plan mode no
[0:00] background bash no built-in to-dos
[0:00] here's what you can do instead for MCP
[0:00] use CLI tools plus skills or build an
[0:00] extension which we will see in a day.
[0:00] Uh, no sub agents. Why? Because they're
[0:00] not observable. Instead, use T-Max and
[0:00] spawn the agent. Again, you have full
[0:00] control over the agents outputs and
[0:00] inputs and can uh see everything that's
[0:00] happening in the sub agent. [...]
[0:00] No plan mode. Write a plan MD file. you
[0:00] have a a persistent artifact instead of
[0:00] some janky UI that doesn't really fit
[0:00] into your terminal viewport. Uh, and you
[0:00] can reuse it across multiple sessions.
[0:00] Um, no background bash, don't need it.
[0:00] We have T-Max. It's the same thing. And
[0:00] no built-in to-dos, write a to-do MD,
[0:00] same thing.
[0:00] [...] you can extend tools, custom, you
[0:00] can give the LLM tools that you define.
[0:00] I think no other coding agent harness
[0:00] currently offers that unless you fork
[0:00] open code. You don't need to here. You
[0:00] just write a simple TypeScript file and
[0:00] it gets loaded uh automatically.
[0:00] [...] And everything hot reloads. So I
[0:00] develop my own extensions that are
[0:00] project or task specific. um in pi
[0:00] inside the project and uh as the uh
[0:00] agent modifies the extension I just
[0:00] reload and it immediately updates uh all
[0:00] of the running code which is very nice
[0:00] and in practice that means you can do
[0:00] custom compaction I think that's one of
[0:00] the things that people should experiment
[0:00] more because all of the compaction
[0:00] implementations currently are not good
[0:00] [...] Does it actually work? Well,
[0:00] terminal bench. [...] Here's Pi right
[0:00] behind Terminus 2 uh using Cloud Opus
[0:00] 4.5. That was back in October where Pi
[0:00] didn't even have compaction, right?
[0:00] [...] I invented OSSification. So I just
[0:00] close issues and PRs for a couple of
[0:00] weeks and work on things on my own.
[0:00] Anything that's important will be
[0:00] reported later on anyways or in the
[0:00] discord. And then I also uh implemented
[0:00] a custom access kind of scheme where I
[0:00] have a markdown file in the repository.
[0:00] If somebody opens an PR without being in
[0:00] without their account name being in that
[0:00] markdown file, the PR gets auto closed.
[0:00] [...] First introduce yourself in a human
[0:00] voice via an issue.
