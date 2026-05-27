# 30-Day LinkedIn Campaign — Shravan N

**Goal:** Maximize recruiter search visibility before December 2026 graduation. Post one of these per day, attach the matching GIF from `gifs/day_XX.gif`.

**Content calendar:**
- Days 1–7: Announcement + project showcases (broad recruiter visibility)
- Days 8–14: Skill deep-dives (one stack per day, deep keyword saturation)
- Days 15–21: Building in public (engagement + niche keywords)
- Days 22–30: Career + recruiter pitch (close the loop, drive DMs)

**Posting tips:**
- Post 8–10am ET on weekdays, 10am–noon on weekends.
- Pin Day 1 (announcement) to your profile permanently.
- Reply to every comment within 2 hours for the first 24h (LinkedIn boosts posts with early engagement).
- Repost your own best-performers from Week 1 in Weeks 3–4.

---

## Day 1 — Open to Work announcement

**Open to Work | Software Engineer | New Grad 2026**

I'm Shravan N, a final-year CS student and Software Engineer working across **Python, React.js, AI, Large Language Models (LLMs), and AWS Cloud**. Interviewing for full-time roles starting December 2026: **Software Engineer, Full Stack Developer, AI/ML Engineer, LLM Engineer, Backend Engineer, Cloud Engineer**.

**Technical skills:**

**Languages:** Python, JavaScript, TypeScript, Java, SQL, HTML5, CSS3
**Backend:** FastAPI, Flask, Django, Node.js, Express.js, REST APIs, GraphQL, Microservices, JWT, OAuth 2.0
**Frontend:** React.js, Next.js, Redux, React Hooks, React Router, Tailwind CSS, Material UI, SPA
**AI / ML:** scikit-learn, TensorFlow, PyTorch, Pandas, NumPy, NLP, feature engineering
**LLMs / GenAI:** OpenAI GPT-4, Anthropic Claude, LangChain, LlamaIndex, Hugging Face, RAG, vector databases (Pinecone, FAISS, ChromaDB), embeddings, prompt engineering, fine-tuning
**AWS Cloud:** EC2, S3, Lambda, API Gateway, DynamoDB, RDS, CloudWatch, IAM, ECS, Serverless
**DevOps:** Git, GitHub Actions, Docker, Kubernetes, CI/CD, Linux, Bash
**Databases:** PostgreSQL, MySQL, MongoDB, Redis, DynamoDB
**Practices:** OOP, DSA, System Design, SDLC, Agile, Scrum, TDD, Unit Testing

In the last 6 months I've shipped end-to-end web apps with a React.js front end, Python REST APIs, a PostgreSQL data layer, and AWS deployment, including a RAG-based LLM application using LangChain and a vector database for semantic search.

**Available:** December 2026. Ready for technical interviews now.
**Open to:** Remote, hybrid, or on-site. Relocation anywhere within the United States.

If your team is hiring, a referral, connection, or repost would mean a lot. DMs are open.

\#OpenToWork #Hiring #SoftwareEngineer #NewGrad #NewGrad2026 #Python #React #JavaScript #TypeScript #FullStack #FastAPI #AI #MachineLearning #LLM #LangChain #RAG #AWS #CloudEngineer #Docker #Kubernetes #DevOps #PostgreSQL #SystemDesign #Hiring2026

---

## Day 2 — Why I chose software engineering

Two years ago I couldn't write a for-loop without Googling it.

I started Computer Science because I liked breaking things and figuring out why they broke. I picked Python because the syntax didn't look like math. My first project was a coin-flip simulator. It took me four hours. It worked on the second try.

Then I built a calculator. Then a todo app. Then a Flask app that scraped weather data and texted me when it was going to rain. Then a React front end on top of it.

Somewhere in there, building stopped feeling like assignments and started feeling like the most fun thing I do all week.

Six months of serious development later, I've shipped end-to-end web applications. I've deployed Python APIs to AWS Lambda. I've built a RAG application using LangChain and a vector database. I've written code in JavaScript, TypeScript, Java, and SQL.

I'm still learning. I will be learning for the next 40 years.

But if you're a hiring manager looking for a new grad who actually enjoys the work — not just the title — let's talk.

I'm Shravan N. Graduating December 2026. Open to full-time Software Engineer roles across the United States.

What got you hooked on engineering? I'd love to hear in the comments.

\#OpenToWork #SoftwareEngineer #NewGrad #NewGrad2026 #Python #JavaScript #ComputerScience #Hiring2026

---

## Day 3 — What's on my laptop right now

If you opened my laptop right now, here's what's actually running.

**Editor:** VS Code with Python, Pylance, ESLint, Prettier, GitHub Copilot, Docker, and the Claude extension. Zen mode on, font at 14pt.

**Terminals:** iTerm split four ways. One running a FastAPI dev server with `uvicorn --reload`. One running `npm run dev` for a React + Vite front end. One on Postgres via `psql`. One on `git status` and `gh pr` commands.

**Browser:** localhost:3000 for the React app, localhost:8000/docs for the FastAPI Swagger UI, the AWS console on Lambda, and a tab open on the OpenAI playground.

**Background processes:** Docker Desktop with a Postgres container, Redis container, and a local LangChain vector store.

**What I'm actually building today:** a small RAG app that ingests PDF lecture notes, embeds them with OpenAI embeddings, stores them in Chroma, and answers questions over them using GPT-4o.

This is what 6 months of self-directed learning looks like. Modern stack, modern tools, real projects.

If your team needs a New Grad Software Engineer who already lives in this stack — Python, React.js, AWS, LLMs — I'm interviewing now for December 2026.

\#SoftwareEngineer #Python #FastAPI #React #ReactJS #LangChain #OpenAI #AWS #Docker #PostgreSQL #LLM #RAG #NewGrad #OpenToWork

---

## Day 4 — Project showcase: full-stack web app

The first project I'd put in front of a hiring manager: a full-stack web app with a React front end, a Python API, a PostgreSQL database, and AWS deployment.

**The stack:**
- Frontend: React.js with TypeScript, Tailwind CSS, React Router, React Query for data fetching, Vite for build.
- Backend: FastAPI with Pydantic models, async SQLAlchemy, JWT authentication, OAuth 2.0 social login.
- Database: PostgreSQL with proper indexes and a migration system using Alembic.
- Infrastructure: Dockerized backend deployed to AWS ECS Fargate behind an Application Load Balancer. Frontend on S3 + CloudFront. CI/CD via GitHub Actions.

**What I learned:**
- API design first. I wrote the OpenAPI spec before I wrote a line of UI code.
- Database indexes matter at 100 rows, not 100,000. A missing index turned a 20ms query into 800ms.
- Authentication is a system, not a feature. JWT rotation, refresh tokens, CORS, and CSRF each took a day.
- AWS billing has sharp edges. I left a NAT Gateway running over a weekend once. Lesson learned.

This project is on my GitHub. The deployed URL is in my portfolio. Both are linked in my profile.

Hiring a New Grad Full Stack Developer for December 2026? I'd love a conversation.

\#FullStack #FullStackDeveloper #React #FastAPI #Python #PostgreSQL #AWS #Docker #CICD #RESTAPI #JWT #NewGrad #OpenToWork #Hiring2026

---

## Day 5 — Project showcase: RAG LLM application

Last month I built a chatbot that actually knows my university's course catalog.

It's a RAG (Retrieval-Augmented Generation) application. Here's how it works under the hood.

**Ingestion:**
- Scrape the course catalog PDFs and HTML pages.
- Chunk text into 500-token windows with 50-token overlap.
- Embed each chunk with OpenAI's text-embedding-3-small.
- Store vectors and metadata in ChromaDB.

**Retrieval and generation:**
- User asks: "What prereqs do I need for CS 480?"
- Embed the query, do a top-k=5 similarity search in Chroma.
- Pass the retrieved chunks plus the query into GPT-4o with a system prompt that constrains it to the provided context.
- Stream the answer back to a React front end via Server-Sent Events.

**The hard parts:**
- Chunking strategy. Naive splits broke sentences. I switched to semantic chunking using LangChain's RecursiveCharacterTextSplitter.
- Hallucination control. The model wanted to invent course codes. I added a strict "if not in context, say you don't know" rule.
- Latency. Cold-start embedding lookups were 1.2s. I added a local cache for the top 100 queries.

This is what I mean when I say I work with LLMs: not just calling an API, but designing the retrieval layer that makes the API useful.

Hiring an AI Engineer or LLM Engineer? I'm available December 2026.

\#LLM #LargeLanguageModels #RAG #LangChain #OpenAI #ChromaDB #VectorDatabase #PromptEngineering #AIEngineer #MachineLearning #Python #FastAPI #NewGrad #OpenToWork

---

## Day 6 — What 6 months of building taught me

Six months ago I'd never deployed anything. Five lessons since.

**1. Ship the ugly version first.**
My first React app had inline styles, no error handling, and a 400-line App.js. It also worked. The refactor came after. Don't optimize for code you haven't shipped.

**2. Read the docs before the Stack Overflow answer.**
The FastAPI docs taught me more about Python type hints than any blog post. The React docs taught me hooks better than any YouTube tutorial.

**3. Logs > debugger, most of the time.**
For a distributed system with a React front end, FastAPI backend, and Postgres, a well-placed `print` is faster than attaching a debugger to three processes.

**4. Cloud is just somebody else's Linux box.**
The fear of "AWS" disappeared the day I realized Lambda is just a function, S3 is just a folder, and IAM is just permissions. Then I could focus on the system, not the buzzwords.

**5. Reviewing other people's code teaches you more than writing your own.**
I read every PR in my class team. I picked up Git workflows, test patterns, and naming conventions that no class taught me.

Six months isn't a lot. But it's enough to know what good engineering looks like and want to do more of it.

Hiring a New Grad Software Engineer who can ship code on day one? Let's talk. December 2026 start.

\#SoftwareEngineer #NewGrad #Python #React #AWS #Engineering #OpenToWork #Hiring2026

---

## Day 7 — Week 1 recap + ask

One week into posting daily. Here's where I am.

I'm Shravan N, a CS student graduating December 2026, building in **Python, React.js, AI/LLMs, and AWS**. I've spent the last 6 months shipping end-to-end web applications, including a full-stack React + FastAPI + PostgreSQL app deployed on AWS, and a RAG-based LLM chatbot built with LangChain and ChromaDB.

I'm interviewing now for full-time roles: **Software Engineer, Full Stack Developer, AI/ML Engineer, LLM Engineer, Backend Engineer, Cloud Engineer**. Open to remote, hybrid, or on-site. Open to relocation anywhere within the United States.

**The ask:**
If your team is hiring a new grad, please send me a DM. If you know a hiring manager, a referral or repost would help enormously. If you've been reading these posts and have feedback, I'd love to hear it in the comments.

The next three weeks will go deeper: stack-by-stack technical deep-dives next week, building-in-public the week after, and a final week focused on what I bring to a first job.

Thanks for being here.

\#OpenToWork #NewGrad #NewGrad2026 #SoftwareEngineer #Python #React #AWS #LLM #Hiring2026

---

## Day 8 — Python deep-dive

People say Python is "easy to learn." That's true for the first week. Then you discover decorators, async, type hints, the GIL, and metaclasses, and you realize you've barely started.

Here's how I actually use Python every day.

**Web APIs with FastAPI.** Pydantic models for request/response validation. Async endpoints with `async def`. Dependency injection via `Depends()`. OpenAPI docs generated for free at `/docs`.

**Async everywhere.** `httpx.AsyncClient` for outbound HTTP. `asyncpg` for Postgres. `asyncio.gather` to fan out parallel work. Async is not optional in 2026 for any backend that touches the network.

**Type hints.** Every function gets type annotations. `mypy` in CI. The investment pays back the first time a refactor would have silently broken something.

**Data work.** Pandas for tabular data, NumPy for numerics. The `polars` library when Pandas isn't fast enough.

**Testing.** PyTest with fixtures, parameterized tests, and `pytest-asyncio` for async code. Coverage above 80% on every project that's gone past prototype.

**The libraries I reach for first:** requests, httpx, FastAPI, SQLAlchemy, Pydantic, LangChain, OpenAI SDK, boto3, Pandas, NumPy, scikit-learn, PyTorch.

Python isn't just a "scripting language" to me. It's the language I use to ship production systems.

Hiring a Python Developer or Backend Engineer for December 2026?

\#Python #PythonDeveloper #FastAPI #AsyncIO #BackendDeveloper #RESTAPI #SoftwareEngineer #NewGrad #OpenToWork

---

## Day 9 — React.js deep-dive

I rewrote a 400-line class component into hooks last week. It came out at 160 lines. It also runs faster.

Here's how I actually use React.

**Hooks I reach for daily:** useState, useEffect, useMemo, useCallback, useRef, useContext, useReducer for complex state, useLayoutEffect when DOM measurement matters.

**State management.** Context + useReducer for app-level state up to medium complexity. Redux Toolkit when state crosses 50+ actions. React Query for server state — never store API responses in Redux.

**Performance.** React DevTools profiler before any optimization. `React.memo` on leaf components in long lists. `useMemo` for expensive derived state. Code splitting with `React.lazy` and `Suspense` to keep the initial bundle under 200KB.

**TypeScript.** Every project. Strict mode on. Generic components for tables, forms, lists. Discriminated unions for state machines.

**Styling.** Tailwind CSS for speed. CSS Modules when a component needs isolation. Headless UI or Radix for accessible primitives.

**Tooling.** Vite for dev server and build. ESLint and Prettier in pre-commit. Vitest for unit tests, Playwright for end-to-end.

React isn't a framework I list on a resume. It's the way I think about UI: declarative, composable, predictable.

Hiring a React Developer or Frontend Engineer for December 2026?

\#React #ReactJS #ReactDeveloper #TypeScript #JavaScript #FrontendDeveloper #FullStack #TailwindCSS #NewGrad #OpenToWork

---

## Day 10 — AWS in production

My first AWS bill was 4 cents. Here's what I deployed for it.

**The stack:**
- A FastAPI backend running on a single t4g.small EC2 in a private subnet.
- An RDS PostgreSQL t4g.micro on the free tier.
- An S3 bucket for static React assets, fronted by CloudFront for HTTPS and caching.
- API Gateway in front of a Lambda function for one async cron job.
- Route 53 for DNS, ACM for free SSL certificates.
- CloudWatch for logs and one alarm on 5xx error rate.

**Lessons:**

NAT Gateways cost money. Always. I run things in public subnets with security groups when possible.

S3 + CloudFront is the cheapest static hosting on the planet. A React app costs me literal pennies a month at low traffic.

Lambda is incredible for cron jobs and webhooks. Cold starts hurt for user-facing APIs. I use Lambda for "fire and forget," EC2 or ECS for "must respond fast."

IAM is the hardest part. Least-privilege roles are tedious to write but worth it. I write them with `aws-policy-cli` or Terraform.

The AWS Free Tier is real. You can build and host a small production app for a year on $0–$5/month if you're careful.

Hiring a Cloud Engineer or Backend Engineer for December 2026?

\#AWS #AWSCloud #CloudEngineer #Serverless #Lambda #EC2 #S3 #DevOps #CloudComputing #NewGrad #OpenToWork

---

## Day 11 — How RAG actually works

RAG is "just" three steps. Most people stop at one.

**Step 1: Embed.**
Take your documents. Split them into chunks (I use 500 tokens with 50-token overlap). Run each chunk through an embedding model like OpenAI's text-embedding-3-small. You get a 1536-dimensional vector per chunk. Store it in a vector database — Pinecone, FAISS, ChromaDB, Weaviate, pgvector.

**Step 2: Retrieve.**
A user asks a question. You embed the question the same way. You do a cosine similarity search in the vector database and grab the top-k most similar chunks (k=5 is a fine default).

**Step 3: Generate.**
You pass the retrieved chunks plus the original question into an LLM (GPT-4o, Claude, Llama) inside a system prompt that says "answer using only this context." The LLM stitches an answer.

**Where most RAG demos fail:**
- Bad chunking. Splitting mid-sentence destroys meaning. Use semantic or recursive splitters.
- No re-ranking. Top-k by cosine similarity is fine for 80% of cases. For the other 20%, add a re-ranker like Cohere Rerank or a cross-encoder.
- Forgotten edge cases. The user asks something not in the corpus. Add a "I don't know" path or you'll get hallucinations.
- No eval. You can't improve what you don't measure. RAGAS, TruLens, or a homemade eval set with answer accuracy.

That's RAG. The "RA" is the hard part. The "G" is a single API call.

Hiring an LLM Engineer or AI Engineer for December 2026?

\#LLM #RAG #LangChain #OpenAI #VectorDatabase #Pinecone #ChromaDB #PromptEngineering #AIEngineer #MachineLearning #NewGrad #OpenToWork

---

## Day 12 — System design study notes

I'm working through Grokking System Design and "Designing Data-Intensive Applications." Here are five concepts that finally clicked.

**1. Load balancing isn't just round-robin.**
Layer 4 vs Layer 7. Sticky sessions for stateful apps. Health checks that actually check health, not just "is the port open." Consistent hashing for cache shards.

**2. Caching is a tradeoff with three sides.**
Cache hit ratio, staleness tolerance, and invalidation complexity. Pick two. The third one will hurt.

**3. Queues turn a hard problem into an easier problem.**
"How do I send 10,000 emails when the user clicks Submit?" becomes "How do I enqueue 10,000 messages and consume them at a steady rate?" SQS, RabbitMQ, Kafka — same idea, different tradeoffs.

**4. Databases scale by giving things up.**
ACID transactions, joins, strong consistency — each one limits scale. Postgres can take you very far. Sharding, read replicas, and eventual consistency are the next steps when it can't.

**5. The CAP theorem is a lens, not a rule.**
Almost no real system is purely AP or CP. You design for the failure mode that hurts your users the least.

I'm still learning. System design interviews are the part of prep I'm putting the most hours into right now.

Hiring an engineer who's serious about distributed systems? I'm graduating December 2026.

\#SystemDesign #DistributedSystems #BackendDeveloper #SoftwareEngineer #NewGrad #ScalableSystems #OpenToWork

---

## Day 13 — DSA grind

200 LeetCode problems this semester. Here's what actually moved the needle.

**Stop solving random problems. Solve by pattern.**
Two pointers. Sliding window. Fast/slow pointers. Binary search on the answer. Merge intervals. Top-K with a heap. Backtracking. DP on subsequences. Graph BFS/DFS. Union-Find. Tries.

If you can name the pattern from the problem statement, you can usually solve it. Most LeetCode mediums are a known pattern in disguise.

**Time-box.**
30 minutes per problem. If I haven't found the approach, I read the editorial, understand it, and re-solve it from scratch the next day.

**Re-solve, don't re-read.**
The third time I solve a problem from memory is when it actually sticks. Anki cards with problem statements, no solutions.

**Write the brute force first.**
Always. Even if I "know" the optimal. The brute force is the baseline I optimize against, and it's what the interviewer wants to see first.

**Test with edge cases before submitting.**
Empty input, single element, duplicates, max constraints, integer overflow. I built a habit of writing the test cases on paper before the code.

DSA isn't the whole job. But it's the gate. And it's a gate I'm putting in the hours to walk through.

Hiring a New Grad Software Engineer ready for technical interviews?

\#DataStructures #Algorithms #LeetCode #InterviewPrep #SoftwareEngineer #NewGrad #OpenToWork

---

## Day 14 — SQL vs NoSQL: how I actually decide

"Should I use Postgres or Mongo?" gets asked in every project chat. Here's my actual decision tree.

**Use PostgreSQL when:**
- Your data has clear relationships (users have orders, orders have items).
- You need ACID transactions (anything touching money, inventory, bookings).
- You'll be writing JOINs, GROUP BYs, and analytical queries.
- You want strict schema enforcement.
- You need full-text search (Postgres has it built in).
- You want JSONB columns for the occasional flexible field. (Best of both worlds.)

**Use MongoDB when:**
- Your data is genuinely document-shaped and varies per record (CMS content, event logs, IoT readings).
- You're prototyping fast and the schema will change a lot.
- You need to scale writes horizontally past what a single Postgres can handle.

**Use Redis when:**
- You need a cache (TTL, eviction).
- You need a rate limiter, a queue, a session store, or pub/sub.
- Sub-millisecond latency matters.

**Use DynamoDB when:**
- You're already on AWS and want a managed key-value store with predictable single-digit-millisecond reads.
- You can model your access patterns up front (DynamoDB punishes flexibility).

Most projects I've built start on Postgres and stay on Postgres. The "you must use NoSQL to scale" advice from 2015 hasn't aged well.

Hiring a Backend Engineer who picks the right database for the job?

\#PostgreSQL #SQL #MongoDB #DynamoDB #Redis #Database #BackendDeveloper #SoftwareEngineer #NewGrad #OpenToWork

---

## Day 15 — Building in public: this week's project

This week I'm building a paper summarizer with Anthropic Claude.

**The problem:** I read 3–5 research papers a week for my LLM coursework. Skimming abstracts loses context. Reading every paper takes too long.

**The build:**
- A Python CLI that accepts a PDF or arXiv URL.
- Extracts text using `pypdf`.
- Sends the full paper to Claude 4.7 with a structured prompt asking for: 1-sentence TL;DR, 3 key contributions, methodology, limitations, and 5 follow-up questions.
- Renders the output as a clean Markdown file with frontmatter for Obsidian.

**What I shipped today:**
- PDF extraction working end-to-end on a 30-page paper.
- Claude API integration with streaming.
- Structured output validated against a Pydantic schema.

**What's left:**
- Batch mode for ingesting a whole folder.
- A small SQLite database to track papers I've already summarized.
- A Streamlit UI so my classmates can use it.

This is the part of being a new grad I actually love: I have an itch, I have the skills, I scratch it in three evenings.

Will share the repo once I clean up the prompts.

Hiring an engineer who builds for themselves first? I'm graduating December 2026.

\#BuildingInPublic #Anthropic #Claude #LLM #Python #PromptEngineering #SoftwareEngineer #NewGrad #OpenToWork

---

## Day 16 — A bug I'll never forget

Spent four hours debugging this week. Turned out to be one missing `await`.

The setup: FastAPI endpoint, async route, calling an async helper that wraps an OpenAI API call. Endpoint returned a coroutine object, not the data. The serializer choked. The error said "object of type coroutine is not JSON serializable."

What I tried first: assuming the OpenAI SDK was broken. It wasn't. Spent an hour reading their changelog. Nothing.

What I tried second: assuming Pydantic was misconfigured. It wasn't. Spent an hour redesigning my response model. Nothing.

What finally worked: reading my own code, line by line, slowly. The helper was `async def`, I called it without `await`. Python happily returned the coroutine. FastAPI tried to serialize the coroutine. Boom.

**Lessons:**
- The bug is almost always in your code, not the library's.
- A 4-hour bug is usually a 30-second fix once you find it. Slow down when you're stuck. Re-read the actual code.
- Type checkers catch this. `mypy --strict` would have flagged the coroutine-not-awaited warning. I now run mypy in pre-commit.
- Writing about a bug is the best way to remember the lesson.

If you're hiring a new grad who's learned to debug under pressure — graduating December 2026.

\#Python #AsyncIO #Debugging #FastAPI #SoftwareEngineer #NewGrad #OpenToWork

---

## Day 17 — LangChain Expression Language (LCEL)

LCEL changed how I compose LLM chains. If you're still writing chains the old way, you're writing more code than you need to.

**The old way:**
```
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)
output_parser = StrOutputParser()
result = chain.run(input)
parsed = output_parser.parse(result)
```

**The LCEL way:**
```
chain = prompt | llm | StrOutputParser()
result = chain.invoke(input)
```

The `|` operator composes Runnables. Anything in LangChain that implements the Runnable interface — prompts, LLMs, parsers, retrievers, custom functions — chains together with a pipe.

**Why I switched:**
- Streaming for free. Every Runnable supports `.stream()`.
- Batching for free. `.batch([inputs])` runs them in parallel.
- Async for free. `.ainvoke()` works on every chain.
- Observable. LangSmith traces every step automatically.
- Composable. A RAG pipeline becomes `retriever | format_docs | prompt | llm | parser`.

It's the closest LangChain has come to feeling like idiomatic Python.

If you're hiring an LLM Engineer who already lives in LangChain — graduating December 2026.

\#LangChain #LCEL #LLM #LLMEngineer #Python #AIEngineer #PromptEngineering #NewGrad #OpenToWork

---

## Day 18 — My first deploy crashed in 30 seconds

True story.

I deployed my first FastAPI app to AWS Lambda. The deploy succeeded. The first request returned a 502. The second request returned a 502. Every request returned a 502.

**What I'd done wrong:**

I packaged the app with `pip install -t .` and zipped it. The zip was 280MB. Lambda's limit is 250MB. The deploy "succeeded" because the upload completed, but the function couldn't initialize.

**What I learned:**
- Lambda layers exist for a reason. Move big dependencies (Pandas, NumPy, anything with native code) into a layer.
- Lambda container images are the better default in 2026. Up to 10GB, real Dockerfile, predictable.
- Check CloudWatch logs first, not the API Gateway response. The 502 told me nothing. The CloudWatch init log told me everything.
- Read the limits page before you deploy. AWS has a hundred limits and you only learn about them by hitting them.

The fix took 15 minutes. The lesson took the rest of the week.

This is what real engineering looks like at the start of a career. You break things, you read the docs, you ship a better version.

Hiring a new grad who's already broken (and fixed) production-style systems?

\#AWS #Lambda #Serverless #DevOps #SoftwareEngineer #NewGrad #OpenToWork

---

## Day 19 — How I deployed a Python API for $0

You can run a real Python API on AWS for actual zero dollars per month if your traffic is low. Here's how.

**The architecture:**

1. **API Gateway HTTP API.** 1 million requests/month on the free tier for the first 12 months. After that, $1/million. For a portfolio app, you'll never hit the limit.

2. **AWS Lambda.** 1 million invocations and 400,000 GB-seconds per month, free forever. A 128MB function serving 50,000 monthly requests costs nothing.

3. **DynamoDB on-demand.** 25GB storage and 25 WCU/RCU free forever. A small app uses a fraction of that.

4. **S3 + CloudFront for the frontend.** Static site hosting. Pennies per month for low traffic. Free SSL via ACM.

5. **Route 53.** $0.50/month per hosted zone. Not free, but the cheapest piece.

**Total cost for a portfolio app with ~10K monthly requests: $0.50/month.**

**Total cost if you skip Route 53 and use the Lambda URL: $0/month.**

The trick is staying inside Lambda + DynamoDB + S3. The moment you add RDS, NAT, ALB, or EC2, you're paying. For most "show recruiters my work" deployments, you don't need any of those.

Hiring a Cloud Engineer who actually knows the bill?

\#AWS #Lambda #Serverless #DynamoDB #S3 #CloudComputing #DevOps #NewGrad #OpenToWork

---

## Day 20 — My first open source PR

Last week I got my first OSS PR merged. A small docs fix in a Python library. The maintainer responded in two hours. The merge took five minutes.

**Why I did it:**
- I'd been using the library for a project and found one example in the README that didn't run.
- I fixed the example, added a missing import, ran the test, wrote a one-line PR description.
- That's it. That's the whole story of my first OSS contribution.

**Why it matters more than I expected:**

A merged PR shows recruiters something a resume can't: I can read someone else's code, understand it, follow contribution guidelines, write a clean commit message, and respond to review.

A merged PR is also a forcing function. You can't half-do it. You either follow the conventions or your PR gets closed.

**Where I'm going next:**
- A larger contribution to the same project — adding a feature I personally need.
- A docs PR to a much bigger project (FastAPI, LangChain).
- Eventually, a real bug fix on a library I depend on.

The bar to start contributing is much lower than I thought. If you're a student reading this and intimidated, find a typo. Fix it. You'll be a contributor by tomorrow.

\#OpenSource #GitHub #Python #SoftwareEngineer #NewGrad #OpenToWork

---

## Day 21 — Vector DB comparison: Pinecone vs FAISS vs Chroma

If you're building RAG, you'll pick one of these. Here's what I've actually used.

**Pinecone — managed, hosted, scales effortlessly.**
- Best for: production, multi-tenant apps, anything where you don't want to operate a database.
- Pros: Zero ops, fast, metadata filtering is excellent.
- Cons: Costs money from day one. Vendor lock-in. Your data leaves your environment.
- What I'd use it for: a SaaS product with paying customers.

**FAISS — in-process, fastest at single-node, no service to run.**
- Best for: notebooks, research, single-machine apps.
- Pros: Free. Blazing fast. Runs anywhere Python runs. Index types from flat to IVF to HNSW.
- Cons: No persistence by default — you save and load the index yourself. No metadata filtering out of the box.
- What I'd use it for: a personal tool or a Jupyter-based experiment.

**ChromaDB — open-source, self-hosted, the sweet spot for small apps.**
- Best for: prototypes that need to feel like a real database without paying.
- Pros: Free. Persists to disk. Metadata filtering. Python-first API. Runs in-process or as a server.
- Cons: Scaling past a few million vectors gets tricky. Operational story is still maturing.
- What I'd use it for: my personal RAG projects (and that's what I picked for my course catalog chatbot).

**Honorable mentions:** pgvector for "I already have Postgres," Weaviate for "I need a real graph + vectors," Qdrant for "I want Rust-fast at single-node."

Hiring an LLM Engineer who's already shipped with these?

\#VectorDatabase #Pinecone #FAISS #ChromaDB #RAG #LLM #AIEngineer #NewGrad #OpenToWork

---

## Day 22 — Why hire a new grad

I get it. Senior engineers ship faster. New grads need ramp-up. The math seems obvious.

Here's the math I'd actually run if I were hiring.

**Cost:** A new grad costs roughly 40–50% of a senior. For the same budget, you can hire two new grads or one senior.

**Velocity at month 1:** Senior wins by a mile. The senior is shipping. The new grad is reading the codebase.

**Velocity at month 6:** Closer than you'd think. A motivated new grad is shipping mid-level work by month 4, especially if the codebase uses modern tools they already know.

**Velocity at year 2:** The new grad you trained is now the senior you didn't have to compete to hire. They know your codebase, your culture, your customers. The senior you hired might already be at their next job.

**Energy:** New grads bring something seniors often don't — curiosity, willingness to take the unglamorous task, and zero baggage from the way things used to work.

I'm not saying replace seniors with new grads. I'm saying the trade is rarely as one-sided as the resume screen makes it look.

If you're hiring a new grad for December 2026, I'm Shravan N. Python, React, AI/LLM, AWS. DMs open.

\#Hiring #NewGrad #SoftwareEngineer #Recruiting #OpenToWork #Hiring2026

---

## Day 23 — What I'm looking for in my first role

Three things matter to me in my first job. In order.

**1. A team that ships.**
Not a team that "ships when it's perfect." A team that puts code in production every week. I learn faster watching real deploys than reading any book.

**2. Mentorship that's structured, not accidental.**
Code reviews on every PR. A senior engineer assigned to me for the first 6 months. Pair programming at least once a week. "Just ask if you have questions" is not a mentorship plan.

**3. A modern stack — but not for the sake of modern.**
I want to work in tools that the industry is converging on: Python or Go or TypeScript on the backend, React or similar on the front, AWS or GCP for cloud, a real CI/CD pipeline. Not because new is better, but because I want the next job I take after this one to feel continuous.

**What I'm not optimizing for:**
- The biggest brand on my resume.
- The highest comp at the offer stage.
- The "coolest" technology.

**What I am optimizing for:**
- Becoming a strong mid-level engineer in 12–18 months.

If your team can do those three things, I want to talk.

\#NewGrad #SoftwareEngineer #Career #OpenToWork #Hiring2026

---

## Day 24 — Interview prep checkpoint

Where I am, three months out from interview season.

**Strong.**
- Behavioral interviews. STAR-format stories ready for: a hard bug, a conflict, a project I led, a time I changed my mind, a time I failed.
- Coding interviews on arrays, strings, hashmaps, two pointers, sliding window, BFS, DFS. ~200 LeetCode mediums solved, ~30 hards.
- Take-home assignments. I've done a Flask API take-home and a React UI take-home. Submitted clean repos with tests, READMEs, and Docker.

**Improving.**
- Coding interviews on DP and graph algorithms beyond basic BFS/DFS. Working through it.
- System design at the staff level. Comfortable at the new-grad level (URL shortener, paste service, news feed). Pushing into harder ones.

**Weak (and being honest about it).**
- Distributed consensus algorithms at depth. I understand Raft conceptually but I haven't implemented it.
- Database internals (B-trees, LSM trees) at the level a real interviewer would want.

**The plan:**
- 4 mock interviews booked over the next 6 weeks.
- One system design problem per weekend, written up like a real doc.
- DP grind continues at one problem per day.

If you're hiring a new grad who's prepared for the bar — interviewing now.

\#InterviewPrep #LeetCode #SystemDesign #SoftwareEngineer #NewGrad #OpenToWork

---

## Day 25 — Favorite project + biggest lesson

If a recruiter asked me for one project to look at, this is the one.

**The project:** A course recommendation chatbot for my university. React front end, FastAPI backend, PostgreSQL with pgvector for embeddings, OpenAI GPT-4o for generation, deployed on AWS ECS Fargate behind CloudFront. The UI lets students ask questions like "what courses should I take if I want to do AI research?" and gets context-aware answers grounded in the catalog.

**What it taught me:**

Every layer matters. The model is impressive on its own. The product is only good if the retrieval is good, the UI is fast, the database queries are indexed, and the cold-start latency is hidden.

I spent maybe 20% of my time on the "AI" part. The other 80% was schema design, API contracts, error handling, deploy automation, and a hundred small UX details.

That's the lesson I'd want a hiring manager to hear: I treat the LLM as one component of a system, not the whole system. The system is what users feel.

The repo is on my GitHub. Happy to walk a hiring team through the architecture.

If you're hiring an engineer who thinks about the whole product — graduating December 2026.

\#LLM #RAG #FullStack #FastAPI #React #PostgreSQL #pgvector #AWS #AIEngineer #NewGrad #OpenToWork

---

## Day 26 — Why AI/ML interests me

I came to AI/ML through frustration.

I was building a feature for a small Flask app — let users ask natural-language questions about their data. The traditional approach (parse intent, look up keywords, hand-craft query templates) was a nightmare. Every new question broke something.

I tried an LLM out of desperation. Wrote a 200-token system prompt. Passed the schema and the user question. The model wrote the SQL. The SQL was correct. The feature shipped in an afternoon.

That afternoon changed my career path.

**What I love about LLMs and modern AI:**
- They collapse problems that used to take months into prompts that take hours.
- They don't replace good engineering. The retrieval, the schema, the eval pipeline, the guardrails — those are still real engineering work. The model is the easy part.
- The field is moving fast enough that today's "junior" is tomorrow's "person who shipped the first one."

**What I'm building toward:**
- Deeper ML fundamentals. I can call APIs; I want to also understand what's happening inside.
- Eval-driven LLM development. Treating prompts and pipelines like code: tested, versioned, monitored.
- Multi-modal applications. Vision + text is the next jump.

If your team is hiring an AI Engineer or LLM Engineer who came in through the practical door, not the academic one — December 2026.

\#AI #ArtificialIntelligence #MachineLearning #LLM #AIEngineer #LLMEngineer #OpenAI #NewGrad #OpenToWork

---

## Day 27 — What day 90 looks like with me

If you hire me in December 2026, here's what month three could look like.

**Month 1.**
- Read the codebase. Pair with two engineers. Get my dev environment perfect.
- Pick up the smallest tickets first — typos, copy fixes, single-line bugs. Get the PR-to-merge loop working.
- Ship 5–10 small PRs by week 4.

**Month 2.**
- Own one small feature end-to-end. Spec, design, implementation, test, deploy.
- Start participating in code review. Comments first, approvals later.
- Take the on-call rotation in shadow mode.

**Month 3.**
- Own a meaningful feature with cross-team scope. Pull in design, product, QA on my own.
- Run a small post-mortem if I broke something. Write the runbook to prevent it.
- Mentor the next new grad's first PR.

By day 90, the question shouldn't be "is the new grad contributing?" It should be "what does the new grad want to own next quarter?"

That's the bar I'm setting for myself. That's what I'd want a manager to hold me to.

If your team needs a new grad with this kind of ramp, I'm graduating December 2026.

\#NewGrad #SoftwareEngineer #Hiring #Career #OpenToWork #Hiring2026

---

## Day 28 — Recruiters: this is the post for you

Saving you a scroll.

**Name:** Shravan N
**Role:** Software Engineer, New Grad
**Graduation:** December 2026
**Availability:** December 2026, ready for interviews immediately
**Location:** United States. Open to remote, hybrid, or on-site. Open to relocation anywhere within the US.

**Roles I'm open to:**
Software Engineer, Software Developer, Full Stack Developer, Full Stack Engineer, Backend Developer, Backend Engineer, Frontend Developer, AI Engineer, AI/ML Engineer, LLM Engineer, Machine Learning Engineer, Cloud Engineer, DevOps Engineer, Junior Software Engineer, Associate Software Engineer.

**Core stack (production-ready):**
Python, JavaScript, TypeScript, React.js, Next.js, FastAPI, Flask, Node.js, Express.js, REST APIs, GraphQL, PostgreSQL, MongoDB, Redis, AWS (EC2, S3, Lambda, API Gateway, DynamoDB, RDS, ECS), Docker, Kubernetes, Git, GitHub Actions, CI/CD, Linux.

**AI/LLM stack:**
OpenAI GPT-4o, Anthropic Claude, LangChain, LlamaIndex, Hugging Face Transformers, RAG, vector databases (Pinecone, FAISS, ChromaDB, pgvector), embeddings, prompt engineering, fine-tuning, scikit-learn, TensorFlow, PyTorch, Pandas, NumPy.

**Engineering fundamentals:**
OOP, Data Structures and Algorithms, System Design, SDLC, Agile, Scrum, TDD, Unit Testing, REST, Microservices, Authentication (JWT, OAuth 2.0), database design.

**What you get:** A new grad with 6 months of real shipping experience, an end-to-end full-stack project deployed to AWS, and a RAG-based LLM application in production.

DM me. Email is on my profile. Portfolio in the comments.

\#OpenToWork #Hiring #SoftwareEngineer #NewGrad #NewGrad2026 #FullStack #Python #React #AI #LLM #AWS #Recruiters

---

## Day 29 — 30 days in, what's changed

Almost a month of posting daily.

**What changed:**
- I started this campaign with 200 connections. I'm now at over [X — fill this in when you post].
- I've had [N] recruiter DMs. Some led somewhere. Most didn't. That's normal.
- I've gotten better at writing about my work. Turns out describing what you build is a separate skill from building it.
- I've built confidence I didn't have on Day 1. Posting publicly is uncomfortable for the first week. After that, it's just a habit.

**What didn't change:**
- I'm still graduating December 2026.
- I'm still open to Software Engineer, Full Stack Developer, AI/ML Engineer, LLM Engineer, Backend Engineer, and Cloud Engineer roles.
- I'm still based in the United States and open to relocation anywhere in the US.

**What I want to thank:**
- Every person who reposted, commented, or sent a referral. You know who you are.
- The recruiters who replied even when there wasn't a match.
- The engineers who took the time to give me feedback on my writing or my projects.

Posting daily is a kind of compounding interest. Every post reaches a few more people. A few of those people are recruiters. A few of those recruiters are hiring.

One more post tomorrow.

\#OpenToWork #NewGrad #SoftwareEngineer #Hiring2026 #Gratitude

---

## Day 30 — Still open to work

Last post in this campaign. Same message as Day 1, with a month of context behind it.

I'm Shravan N. I'm a final-year Computer Science student graduating December 2026. I'm a Software Engineer who works across Python, React.js, AI, Large Language Models, and AWS Cloud. I'm interviewing now for full-time roles.

**Over the last 30 days I've shared:**
- Full deep-dives on my Python, React, AWS, and LLM stacks.
- Two end-to-end project breakdowns: a full-stack React + FastAPI + PostgreSQL app on AWS, and a RAG LLM chatbot built with LangChain and ChromaDB.
- Hard-won lessons from 6 months of shipping: bugs I broke, costs I learned about, patterns that work.
- Honest takes on what I'm looking for in my first job and what a hiring team can expect from me on day 90.

**I'm still open to:**
- Software Engineer, Full Stack Developer, AI/ML Engineer, LLM Engineer, Backend Engineer, Cloud Engineer roles.
- Remote, hybrid, or on-site.
- Relocation anywhere within the United States.
- A start date in December 2026.

**The ask is the same as Day 1.**

If your team is hiring, send me a DM. If you know a hiring manager, please refer me or repost. If you've read every post in this campaign, thank you, and I'd love a connection request.

I'll keep building. I'll keep posting. The next campaign starts after the first offer.

Let's talk.

\#OpenToWork #Hiring #SoftwareEngineer #NewGrad #NewGrad2026 #Python #React #AI #LLM #AWS #Hiring2026
