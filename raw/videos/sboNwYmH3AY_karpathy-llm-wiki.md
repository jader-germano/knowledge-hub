---
url: https://youtu.be/sboNwYmH3AY
title: "LLM Wiki — Andrej Karpathy"
author: "@NathanLatka (apresentador) / Andrej Karpathy (ideia original)"
date: 2026-04 (aproximado)
captured_at: 2026-04-08
source: youtube-transcript skill
---

# Transcrição: LLM Wiki (Karpathy)

> Fonte imutável. Não editar após captura.

[0:00] What you're looking at right here is 36
[0:00] of my most recent YouTube videos
[0:00] organized into an actual knowledge
[0:00] system that makes sense. And in today's
[0:00] video, I'm going to show you how you can
[0:00] set this up in 5 minutes. It's super
[0:00] super easy. You can see here how we have
[0:00] these different nodes and different
[0:00] patterns emerging. And as we zoom in, we
[0:00] can see what each of these little dots
[0:00] represents. So, for example, this is one
[0:00] of my videos, $10,000 aentic workflows.
[0:00] We can see it's got some tags. It's got
[0:00] the video link. It's got the raw file.
[0:00] And it gives an explanation of what this
[0:00] video is about and what the takeaways
[0:00] are. And the coolest part is I can
[0:00] follow the back links to get where I
[0:00] want. There's a backlink for the WAT
[0:00] framework. There's a backlink for Claude
[0:00] Code. There's a backlink for all these
[0:00] different tools I mentioned like
[0:00] Perplexity, Visual Studio Code, Nano
[0:00] Banana, Naden N. It also has techniques
[0:00] like the WT framework or bypass
[0:00] permissions mode or human review
[0:00] checkpoint. So, as this continues to
[0:00] fill up, we can start to see patterns
[0:00] and relationships between every tool or
[0:00] every skill or every MCP server that I
[0:00] might have talked about in a YouTube
[0:00] video. And I can just query it in a
[0:00] really efficient way now that we have
[0:00] this actual system set up. And the crazy
[0:00] part is I said, "Hey, Cloud Code, go
[0:00] grab the transcripts from my recent
[0:00] videos and organize everything. I
[0:00] literally didn't have to do any manual
[0:00] relationship building here. It just
[0:00] figured it all out on its own." And then
[0:00] right here, I have a much smaller one,
[0:00] but this is more of my personal brain.
[0:00] So this is stuff going on in my personal
[0:00] life. This is stuff going on with, you
[0:00] know, UpAI or my YouTube channel or my
[0:00] different businesses and my employees
[0:00] and our quarter 2 initiatives and things
[0:00] like that. This is more of my own second
[0:00] brain. So I've got one second brain here
[0:00] and then I've got one basically YouTube
[0:00] knowledge system and I could combine
[0:00] these or I could keep them separate and
[0:00] I can just keep building more knowledge
[0:00] systems and plug them all into other AI
[0:00] agents that I need to have this context.
[0:00] It's just super cool. So Andre Carpathy
[0:00] just released this little post about LLM
[0:00] knowledge bases and explaining what he's
[0:00] been doing with them. And in just a
[0:00] matter of few days, it got a ton of
[0:00] traction on X. So let's do a quick
[0:00] breakdown and then I'm going to show you
[0:00] guys how you can get this set up in
[0:00] basically 5 minutes. It's way more
[0:00] simple than you may think. Something
[0:00] I've been finding very useful recently
[0:00] is using LLM to build personal knowledge
[0:00] bases for various topics of research
[0:00] interest. So there's different stages.
[0:00] The first part is data ingest. He puts
[0:00] in basically source documents. So he
[0:00] basically takes a PDF and puts it into
[0:00] Cloud Code and then Cloud Code does the
[0:00] rest. He uses Obsidian as the IDE. So
[0:00] this is nothing really too
[0:00] game-changing. Obsidian just lets you
[0:00] visually see your markdown files. But
[0:00] for example, this Obsidian project right
[0:00] here with all this YouTube transcript
[0:00] stuff that actually lives right here.
[0:00] This is the exact same thing. Here are
[0:00] the raw YouTube transcripts. And here's
[0:00] that wiki that I showed you guys with
[0:00] the different um folders for what Cloud
[0:00] Code did with my YouTube transcripts.
[0:00] And then there's a Q&A phase where you
[0:00] basically can ask questions about
[0:00] YouTube or about the research and it can
[0:00] look through the entire wiki in a much
[0:00] more efficient way and it can give you
[0:00] answers that are super intelligent. He
[0:00] said here, "I thought that I had to
[0:00] reach for fancy rag, but the LLM has
[0:00] been pretty good about automaintaining
[0:00] index files and brief summaries of all
[0:00] documents and it reads all the important
[0:00] related data fairly easily at this small
[0:00] scale." So right now he's doing about
[0:00] 100 articles and about half a million
[0:00] words. So there's a few other things
[0:00] that we'll cover later, but the TLDDR is
[0:00] you give raw data to cloud code. It
[0:00] compares it, it organizes it, and then
[0:00] it puts it into the right spots with
[0:00] relationships, and then you can query it
[0:00] about anything. And it can help you
[0:00] identify where there's gaps in that node
[0:00] or in that, you know, relationship, and
[0:00] it can go do research and fill in the
[0:00] gaps. All right. So why is this a big
[0:00] deal? Because normal AI chats are
[0:00] ephemeral, meaning the knowledge
[0:00] disappears after the conversation. But
[0:00] this method, using Karpathy's LLM wiki,
[0:00] makes knowledge compound like interest
[0:00] in a bank. People on X are calling it a
[0:00] game changanger because it finally makes
[0:00] AI feel like a tireless colleague who
[0:00] actually remembers everything and it
[0:00] stays organized. It's also super simple.
[0:00] It will take you five minutes to set up.
[0:00] I'll show you guys. You don't need a
[0:00] fancy vector database embeddings or
[0:00] complex infrastructure. It's literally
[0:00] just a folder with markdown files.
[0:00] That's it. You literally just have a
[0:00] vault up top. So in this example, it's
[0:00] called my wiki. You've got a raw folder
[0:00] where you put all of the stuff. And then
[0:00] you've got a wiki folder, which is what
[0:00] the LLM takes from your raw and puts it
[0:00] into the wiki. So in here you have all
[0:00] the wiki pages which it will create but
[0:00] then you also have an index and you have
[0:00] a log. So for example in my YouTube
[0:00] transcripts vault here is the index. You
[0:00] can see that I have all these different
[0:00] tools which I could obviously click on
[0:00] and it would take me right to that page
[0:00] or after that I have all the different
[0:00] techniques agent teams sub agents
[0:00] permission modes the WAT framework and
[0:00] then we've got different concepts MCP
[0:00] servers rag vibe coding we've got all
[0:00] these different sources which are you
[0:00] know the YouTube videos and then when I
[0:00] have people or when I have comparisons
[0:00] they will be put in here in the index
[0:00] and then we also have a log which is the
[0:00] operation history so in this case in the
[0:00] YouTube project the log isn't huge cuz I
[0:00] only ran one huge batch of the initial
[0:00] 36 YouTube videos, but now every time I
[0:00] have one, I say, "Hey, can you go ahead
[0:00] and ingest the new YouTube video into
[0:00] the wiki and then we'll see every single
[0:00] time we update this." And then, of
[0:00] course, you need your claw. MD to
[0:00] explain how the project works and how to
[0:00] search through things and how to, you
[0:00] know, update things. It's also a big
[0:00] deal from a cost perspective, token
[0:00] efficiency, and long-term value. One X
[0:00] user turned 383 scattered files and over
[0:00] a 100 meeting transcripts into a compact
[0:00] wiki and dropped token usage by 95% when
[0:00] querying with Claude. And obviously
[0:00] token management and efficiency is a
[0:00] huge conversation right now and will
[0:00] always be. The other thing that's really
[0:00] cool about this is there's not really
[0:00] like a GitHub repo you go copy or
[0:00] there's not a complicated setup. You
[0:00] literally just say hey cloud code read
[0:00] this idea from Andre Karpathy and
[0:00] implement it. And people on X are now
[0:00] talking about like this is how 2026 AI
[0:00] agentic software and products will be
[0:00] made. You just give it a highle idea and
[0:00] it goes and builds it out. And Karpathy
[0:00] even said, "Hey, you know, I left this
[0:00] prompt vague so that you guys can
[0:00] customize it." [...] So Andre Carpathy
[0:00] just released this little post about LLM
[0:00] knowledge bases [...] Something I've been
[0:00] finding very useful recently is using LLM
[0:00] to build personal knowledge bases for
[0:00] various topics of research interest. [...]
[0:00] He said here, "I thought that I had to
[0:00] reach for fancy rag, but the LLM has
[0:00] been pretty good about automaintaining
[0:00] index files and brief summaries of all
[0:00] documents and it reads all the important
[0:00] related data fairly easily at this small
[0:00] scale." So right now he's doing about
[0:00] 100 articles and about half a million words.
[0:00] [...] the TLDDR is you give raw data to
[0:00] cloud code. It compares it, it organizes
[0:00] it, and then it puts it into the right
[0:00] spots with relationships, and then you
[0:00] can query it about anything. [...]
[0:00] Karpathy also said, "Sometimes I like to
[0:00] keep it really simple and really flat,
[0:00] which means like no subfolders and not a
[0:00] bunch of over organizing."
[0:00] [...] One X user turned 383 scattered
[0:00] files and over a 100 meeting transcripts
[0:00] into a compact wiki and dropped token
[0:00] usage by 95% when querying with Claude.
[0:00] [...] Karpathi says that he runs some LLM
[0:00] health checks over the wiki to find
[0:00] inconsistent data, impute missing data
[0:00] with web searches, find interesting
[0:00] connections for new article candidates [...]
[0:00] So now the final question about this
[0:00] that I wanted to cover is like does this
[0:00] kill semantic search rag? And the answer
[0:00] is no, but kind of yes. [...] if you have
[0:00] hundreds of pages with good indexes,
[0:00] you're fine with wiki graph. But if you
[0:00] were getting up to the millions of
[0:00] documents, then you're going to want to
[0:00] actually do more of a traditional rag
[0:00] pipeline, at least for now with how the
[0:00] current models are and everything we
[0:00] know right now in April 2026.
