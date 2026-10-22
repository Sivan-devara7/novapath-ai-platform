"""
Generates production-grade, authoritative role benchmark JSON files for all 16 roles
(11 new researched roles + 5 existing roles) based on roadmap.sh, O*NET, ESCO, and official docs.
Saves them into backend/data/roles/<role_slug>.json.
"""

import os
import json

ROLES_DATA = [
    {
        "role": "Frontend Developer",
        "slug": "frontend-developer",
        "aliases": ["Frontend Engineer", "UI Developer", "Client-Side Developer", "Web Front-End Engineer"],
        "model_classes": {"Web Designing": 0.70, "Python Developer": 0.15, "Java Developer": 0.15},
        "action_verbs": ["built", "designed", "rendered", "optimized", "styled", "refactored", "implemented", "integrated", "architected"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": True
        },
        "critical_skills": [
            "html5", "css3", "javascript", "typescript", "react",
            "next.js", "tailwind css", "responsive web design", "dom manipulation",
            "rest apis", "state management", "git", "web performance",
            "component lifecycle", "browser devtools", "web accessibility",
            "cross-browser compatibility", "package managers"
        ],
        "bonus_skills": [
            "vue.js", "svelte", "graphql", "websockets", "jest",
            "playwright", "cypress", "webpack", "vite", "progressive web apps",
            "three.js", "micro-frontends", "server-side rendering", "storybook",
            "css modules", "web security"
        ],
        "skill_synonyms": {
            "html5": ["html", "semantic html", "xhtml"],
            "css3": ["css", "cascading style sheets", "modern css"],
            "javascript": ["js", "es6", "es6+", "ecmascript", "vanilla js"],
            "typescript": ["ts"],
            "react": ["react.js", "reactjs"],
            "next.js": ["nextjs", "next.js 14", "next.js 13"],
            "tailwind css": ["tailwind", "tailwindcss"],
            "responsive web design": ["responsive design", "media queries", "mobile-first design", "rwd"],
            "dom manipulation": ["dom api", "virtual dom", "shadow dom"],
            "rest apis": ["rest api", "restful api", "fetch api", "axios"],
            "state management": ["redux", "redux toolkit", "zustand", "mobx", "recoil", "react context"],
            "git": ["github", "gitlab", "version control"],
            "web performance": ["core web vitals", "lighthouse", "lazy loading", "code splitting"],
            "component lifecycle": ["react hooks", "hooks", "useeffect", "usestate"],
            "browser devtools": ["chrome devtools", "developer tools", "devtools"],
            "web accessibility": ["a11y", "wcag", "aria", "screen readers"],
            "cross-browser compatibility": ["cross-browser testing", "polyfills", "autoprefixer"],
            "package managers": ["npm", "yarn", "pnpm"],
            "vue.js": ["vue", "vuejs", "vue 3", "vuex", "pinia"],
            "svelte": ["sveltekit", "svelte.js"],
            "graphql": ["apollo client", "relay"],
            "websockets": ["socket.io", "web sockets"],
            "jest": ["react testing library", "rtl", "unit testing"],
            "playwright": ["e2e testing", "end to end testing"],
            "cypress": ["cypress.io"],
            "webpack": ["bundlers", "vite", "turbopack", "rollup"],
            "vite": ["vitejs"],
            "progressive web apps": ["pwa", "service workers"],
            "three.js": ["threejs", "webgl", "canvas api"],
            "micro-frontends": ["module federation", "microfrontends"],
            "server-side rendering": ["ssr", "ssg", "isr", "static site generation"],
            "storybook": ["storybook.js", "design system documentation"],
            "css modules": ["styled-components", "styled components", "sass", "scss"],
            "web security": ["content security policy", "csp", "xss prevention", "csrf defense"]
        },
        "tools": ["VS Code", "Chrome DevTools", "Figma", "Postman", "Vite", "Webpack", "Vercel", "npm"],
        "certifications": [
            "Meta Front-End Developer Professional Certificate",
            "W3Cx Front-End Web Developer Professional Certificate",
            "AWS Certified Cloud Practitioner"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Translating Figma designs into responsive, semantic HTML/CSS/JS with basic React components and Git workflow.",
                "expected_skills": ["html5", "css3", "javascript", "responsive web design", "react", "git"],
                "projects": ["Responsive Portfolio Landing Page", "Interactive Task Tracker with LocalStorage", "Weather App consuming REST API"]
            },
            "mid": {
                "focus": "Production Next.js or React applications with TypeScript, modular state management, automated unit tests, and performance optimization.",
                "expected_skills": ["typescript", "react", "next.js", "state management", "tailwind css", "jest", "web performance"],
                "projects": ["Full-featured E-Commerce Store with Cart & Stripe", "SaaS Dashboard with Real-Time Analytics", "Design System Component Library"]
            },
            "senior": {
                "focus": "Frontend architecture, micro-frontends, Core Web Vitals optimization at scale, SSR/ISR caching strategies, and mentoring.",
                "expected_skills": ["web performance", "micro-frontends", "server-side rendering", "web accessibility", "web security", "playwright"],
                "projects": ["Enterprise Multi-Tenant Web Portal with Module Federation", "High-Throughput Streaming Dashboard", "Accessible Headless CMS Integration"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "Internet, HTML5 & Semantic Web",
                "skills": ["html5", "web accessibility"],
                "description": "Master semantic elements, document outline, forms, validation, and accessibility (WCAG/ARIA).",
                "resources": [
                    {"title": "MDN HTML Basics & Semantics", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "type": "free_doc"},
                    {"title": "web.dev Learn HTML", "url": "https://web.dev/learn/html", "type": "free_course"}
                ]
            },
            {
                "step": 2,
                "topic": "Modern CSS & Responsive Design",
                "skills": ["css3", "tailwind css", "responsive web design"],
                "description": "Flexbox, CSS Grid, media queries, mobile-first design, animations, and utility-first Tailwind CSS.",
                "resources": [
                    {"title": "web.dev Learn CSS", "url": "https://web.dev/learn/css", "type": "free_course"},
                    {"title": "Tailwind CSS Official Documentation", "url": "https://tailwindcss.com/docs", "type": "free_doc"}
                ]
            },
            {
                "step": 3,
                "topic": "JavaScript & DOM Fundamentals",
                "skills": ["javascript", "dom manipulation", "rest apis"],
                "description": "ES6+ syntax, asynchronous JS (Promises, async/await), event loop, DOM manipulation, and fetch API.",
                "resources": [
                    {"title": "The Modern JavaScript Tutorial", "url": "https://javascript.info", "type": "free_doc"},
                    {"title": "MDN Asynchronous JavaScript", "url": "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous", "type": "free_doc"}
                ]
            },
            {
                "step": 4,
                "topic": "TypeScript & Type Safety",
                "skills": ["typescript"],
                "description": "Static typing, interfaces, generics, union types, and TypeScript configuration for frontend apps.",
                "resources": [
                    {"title": "TypeScript Official Handbook", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "type": "free_doc"},
                    {"title": "Total TypeScript Free Tutorials", "url": "https://www.totaltypescript.com/tutorials", "type": "free_course"}
                ]
            },
            {
                "step": 5,
                "topic": "React & Modern Component Architecture",
                "skills": ["react", "component lifecycle", "state management"],
                "description": "Functional components, custom hooks, context, state libraries (Zustand/Redux), and component patterns.",
                "resources": [
                    {"title": "React.dev Official Documentation", "url": "https://react.dev/learn", "type": "free_doc"},
                    {"title": "Epic React Open Articles", "url": "https://kentcdodds.com/blog", "type": "free_doc"}
                ]
            },
            {
                "step": 6,
                "topic": "Production Frameworks: Next.js & Performance",
                "skills": ["next.js", "server-side rendering", "web performance"],
                "description": "App Router, Server Components, SSR/SSG/ISR, Core Web Vitals, code splitting, and asset optimization.",
                "resources": [
                    {"title": "Next.js Learn Course", "url": "https://nextjs.org/learn", "type": "free_course"},
                    {"title": "web.dev Fast Load Times", "url": "https://web.dev/fast", "type": "free_doc"}
                ]
            },
            {
                "step": 7,
                "topic": "Testing & Build Automation",
                "skills": ["jest", "playwright", "vite", "git"],
                "description": "Component testing with Vitest/Jest, E2E testing with Playwright, bundlers, and CI/CD deployment.",
                "resources": [
                    {"title": "Playwright Getting Started", "url": "https://playwright.dev/docs/intro", "type": "free_doc"},
                    {"title": "Testing Library Documentation", "url": "https://testing-library.com/docs/react-testing-library/intro", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://roadmap.sh/frontend",
            "https://developer.mozilla.org",
            "https://www.onetonline.org/link/summary/15-1254.00",
            "https://web.dev"
        ],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Backend Developer",
        "slug": "backend-developer",
        "aliases": ["Backend Engineer", "Server-Side Developer", "API Engineer", "Systems Backend Developer"],
        "model_classes": {"Python Developer": 0.45, "Java Developer": 0.35, "Database": 0.20},
        "action_verbs": ["architected", "engineered", "scaled", "optimized", "built", "implemented", "deployed", "refactored", "integrated"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": False
        },
        "critical_skills": [
            "python", "node.js", "sql", "postgresql", "restful api design",
            "docker", "redis", "orm", "authentication & authorization",
            "api security", "microservices architecture", "unit & integration testing",
            "git", "linux fundamentals", "database indexing & query optimization",
            "logging & monitoring", "asynchronous programming", "message queues"
        ],
        "bonus_skills": [
            "graphql", "kubernetes", "kafka", "rabbitmq", "elasticsearch",
            "grpc", "terraform", "ci/cd pipelines", "distributed tracing",
            "serverless architecture", "aws", "gcp", "domain-driven design",
            "websocket", "high availability", "secret management"
        ],
        "skill_synonyms": {
            "python": ["python 3", "fastapi", "django", "flask"],
            "node.js": ["nodejs", "express", "express.js", "fastify", "nest.js", "nestjs"],
            "sql": ["structured query language", "relational database", "rdbms"],
            "postgresql": ["postgres", "pgsql", "mysql"],
            "restful api design": ["rest api", "restful apis", "rest apis", "api design", "openapi", "swagger"],
            "docker": ["containerization", "containers", "docker-compose", "dockerfile"],
            "redis": ["in-memory cache", "caching", "memcached"],
            "orm": ["object-relational mapping", "prisma", "sqlalchemy", "hibernate", "typeorm"],
            "authentication & authorization": ["jwt", "oauth2", "oauth", "session management", "rbac", "auth0"],
            "api security": ["cors", "rate limiting", "sql injection prevention", "csrf defense", "owasp api"],
            "microservices architecture": ["microservices", "service-oriented architecture", "soa", "distributed systems"],
            "unit & integration testing": ["pytest", "junit", "mocha", "jest", "unit testing", "integration testing"],
            "git": ["github", "gitlab", "version control"],
            "linux fundamentals": ["linux", "bash", "shell scripting", "unix", "systemd"],
            "database indexing & query optimization": ["indexing", "query optimization", "explain analyze", "b-tree"],
            "logging & monitoring": ["structured logging", "datadog", "prometheus", "winston", "elk"],
            "asynchronous programming": ["asyncio", "concurrency", "event loop", "goroutines", "multithreading"],
            "message queues": ["message broker", "rabbitmq", "celery", "bullmq", "sqs"],
            "graphql": ["apollo server", "graphql schema"],
            "kubernetes": ["k8s", "container orchestration"],
            "kafka": ["apache kafka", "event streaming", "event-driven architecture"],
            "rabbitmq": ["amqp"],
            "elasticsearch": ["opensearch", "elk stack", "full text search"],
            "grpc": ["protocol buffers", "protobuf", "rpc"],
            "terraform": ["infrastructure as code", "iac"],
            "ci/cd pipelines": ["ci/cd", "continuous integration", "github actions", "gitlab ci"],
            "distributed tracing": ["opentelemetry", "jaeger", "apm"],
            "serverless architecture": ["aws lambda", "serverless", "cloud functions"],
            "aws": ["amazon web services", "ec2", "s3", "rds"],
            "gcp": ["google cloud platform", "google cloud"],
            "domain-driven design": ["ddd", "clean architecture", "hexagonal architecture"],
            "websocket": ["websockets", "socket.io", "server-sent events", "sse"],
            "high availability": ["load balancing", "failover", "horizontal scaling", "nginx"],
            "secret management": ["hashicorp vault", "aws secrets manager", "dotenv"]
        },
        "tools": ["Postman", "Docker", "pgAdmin", "Redis-CLI", "VS Code", "Git", "DBeaver", "Linux CLI"],
        "certifications": [
            "AWS Certified Solutions Architect - Associate",
            "Oracle Certified Professional: Java SE Developer",
            "GitHub Actions Certification"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Building robust CRUD APIs with standard validation, relational database modeling, basic authentication, and automated unit testing.",
                "expected_skills": ["python", "sql", "postgresql", "restful api design", "git", "linux fundamentals"],
                "projects": ["RESTful Blog API with JWT Auth and PostgreSQL", "Inventory Management Microservice with Docker", "URL Shortener with Redis Caching"]
            },
            "mid": {
                "focus": "Asynchronous task workers, caching layers, microservice communication, Dockerized deployment pipelines, and database query optimization.",
                "expected_skills": ["node.js", "docker", "redis", "message queues", "orm", "api security", "unit & integration testing"],
                "projects": ["Event-Driven Payment Processing Service with RabbitMQ", "High-Throughput File Ingestion API with S3 & Celery", "Federated GraphQL Service"]
            },
            "senior": {
                "focus": "Distributed systems resilience, zero-downtime database migrations, gRPC communication, high-availability architecture, and security hardening.",
                "expected_skills": ["microservices architecture", "kubernetes", "kafka", "database indexing & query optimization", "distributed tracing", "high availability"],
                "projects": ["Distributed Real-Time Streaming Pipeline with Kafka & ClickHouse", "Zero-Downtime Microservices Migration Engine", "Global Multi-Region API Gateway"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "Language Proficiency & Data Structures",
                "skills": ["python", "asynchronous programming"],
                "description": "Deep syntax, memory model, OOP/functional patterns, concurrency, and asynchronous I/O.",
                "resources": [
                    {"title": "FastAPI Official Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "free_doc"},
                    {"title": "Real Python Tutorials", "url": "https://realpython.com", "type": "free_doc"}
                ]
            },
            {
                "step": 2,
                "topic": "Relational Databases & SQL Mastery",
                "skills": ["sql", "postgresql", "database indexing & query optimization"],
                "description": "Normalization, indexing strategies (B-Tree/GIN), transactions, isolation levels, and EXPLAIN ANALYZE.",
                "resources": [
                    {"title": "PostgreSQL Official Documentation", "url": "https://www.postgresql.org/docs/", "type": "free_doc"},
                    {"title": "Use The Index, Luke (SQL Indexing Guide)", "url": "https://use-the-index-luke.com", "type": "free_doc"}
                ]
            },
            {
                "step": 3,
                "topic": "RESTful API Design & Architecture",
                "skills": ["restful api design", "orm", "api security"],
                "description": "HTTP semantics, REST standards, error handling, ORMs, JWT/OAuth2 authentication, and rate limiting.",
                "resources": [
                    {"title": "REST API Tutorial", "url": "https://restfulapi.net", "type": "free_doc"},
                    {"title": "OWASP API Security Top 10", "url": "https://owasp.org/API-Security/", "type": "free_doc"}
                ]
            },
            {
                "step": 4,
                "topic": "Caching & Background Processing",
                "skills": ["redis", "message queues"],
                "description": "In-memory caching strategies (cache-aside, write-through), eviction policies, and message queues (RabbitMQ/Celery).",
                "resources": [
                    {"title": "Redis Official University & Docs", "url": "https://redis.io/docs/", "type": "free_doc"},
                    {"title": "RabbitMQ Tutorials", "url": "https://www.rabbitmq.com/getstarted.html", "type": "free_doc"}
                ]
            },
            {
                "step": 5,
                "topic": "Containerization & Cloud Infrastructure",
                "skills": ["docker", "linux fundamentals", "ci/cd pipelines"],
                "description": "Multi-stage Dockerfiles, networking, volumes, compose environments, Linux system administration, and CI/CD.",
                "resources": [
                    {"title": "Docker Getting Started Guide", "url": "https://docs.docker.com/get-started/", "type": "free_doc"},
                    {"title": "GitHub Actions Documentation", "url": "https://docs.github.com/en/actions", "type": "free_doc"}
                ]
            },
            {
                "step": 6,
                "topic": "Distributed Systems & Event-Driven Architecture",
                "skills": ["microservices architecture", "kafka", "grpc"],
                "description": "Service decomposition, Kafka event streaming, gRPC/Protobuf RPCs, distributed transactions (Saga), and observability.",
                "resources": [
                    {"title": "Apache Kafka Quickstart", "url": "https://kafka.apache.org/quickstart", "type": "free_doc"},
                    {"title": "gRPC Documentation", "url": "https://grpc.io/docs/", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://roadmap.sh/backend",
            "https://www.onetonline.org/link/summary/15-1252.00",
            "https://12factor.net",
            "https://martinfowler.com/architecture/"
        ],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Data Analyst",
        "slug": "data-analyst",
        "aliases": ["Business Data Analyst", "BI Analyst", "Analytics Specialist", "Reporting Analyst"],
        "model_classes": {"Business Analyst": 0.50, "Database": 0.30, "Data Science": 0.20},
        "action_verbs": ["analyzed", "visualized", "synthesized", "identified", "modeled", "streamlined", "calculated", "discovered", "reported"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": False
        },
        "critical_skills": [
            "sql", "python", "microsoft excel", "power bi", "tableau",
            "data visualization", "exploratory data analysis", "descriptive statistics",
            "data cleaning & preprocessing", "business acumen & kpi tracking",
            "data modeling", "a/b testing & hypothesis testing", "reporting & executive dashboards",
            "relational database concepts", "git for analytics", "data storytelling"
        ],
        "bonus_skills": [
            "r programming", "dbt", "bigquery", "snowflake", "statistical modeling",
            "google looker", "etl / elt pipelines", "machine learning basics",
            "web analytics", "data governance & privacy", "customer segmentation",
            "jupyter notebooks", "automated scheduling", "predictive analytics",
            "power query", "power automate"
        ],
        "skill_synonyms": {
            "sql": ["advanced sql", "postgresql", "mysql", "tsql", "sql queries", "window functions"],
            "python": ["python for data analysis", "pandas", "numpy"],
            "microsoft excel": ["excel", "advanced excel", "vlookup", "xlookup", "pivot tables", "excel formulas"],
            "power bi": ["powerbi", "dax", "power query", "microsoft power bi"],
            "tableau": ["tableau desktop", "tableau server", "tableau prep"],
            "data visualization": ["data viz", "dashboard design", "charts", "matplotlib", "seaborn"],
            "exploratory data analysis": ["eda", "data exploration", "summary statistics"],
            "descriptive statistics": ["statistics", "mean", "median", "standard deviation", "variance"],
            "data cleaning & preprocessing": ["data wrangling", "data cleansing", "imputation", "data validation"],
            "business acumen & kpi tracking": ["kpi definition", "churn analysis", "retention rate", "cac", "ltv", "roi"],
            "data modeling": ["star schema", "snowflake schema", "dimensional modeling", "fact tables"],
            "a/b testing & hypothesis testing": ["hypothesis testing", "a/b testing", "p-value", "t-test", "chi-square"],
            "reporting & executive dashboards": ["automated reporting", "executive reporting", "scorecards"],
            "relational database concepts": ["rdbms", "database normalization", "foreign keys"],
            "git for analytics": ["git", "version control"],
            "data storytelling": ["insight presentation", "stakeholder communication"],
            "r programming": ["r language", "ggplot2", "tidyverse"],
            "dbt": ["data build tool", "dbt core", "dbt cloud"],
            "bigquery": ["google bigquery", "gcp bigquery"],
            "snowflake": ["snowflake data warehouse"],
            "statistical modeling": ["regression analysis", "correlation analysis"],
            "google looker": ["looker", "looker studio", "google data studio", "lookml"],
            "etl / elt pipelines": ["etl", "elt", "data pipelines", "fivetran"],
            "machine learning basics": ["scikit-learn", "clustering", "k-means"],
            "web analytics": ["google analytics", "ga4", "mixpanel", "amplitude"],
            "data governance & privacy": ["data governance", "gdpr", "data catalog"],
            "customer segmentation": ["rfm analysis", "cohort analysis", "customer lifetime value"],
            "jupyter notebooks": ["jupyter", "google colab"],
            "automated scheduling": ["cron jobs", "airflow basics"],
            "predictive analytics": ["forecasting", "time series forecasting", "prophet"]
        },
        "tools": ["Power BI", "Tableau", "Microsoft Excel", "SQL Server Management Studio", "Jupyter Notebooks", "DBeaver", "Git"],
        "certifications": [
            "Microsoft Certified: Power BI Data Analyst Associate (PL-300)",
            "Google Data Analytics Professional Certificate",
            "Tableau Certified Data Analyst"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Writing SQL queries (joins, aggregations), clean spreadsheets in Excel, and building foundational Power BI or Tableau dashboards.",
                "expected_skills": ["sql", "microsoft excel", "power bi", "data visualization", "descriptive statistics"],
                "projects": ["Retail Sales KPI Dashboard in Power BI", "Customer Churn Analysis with SQL & Excel", "Public Health Data Exploration with Python"]
            },
            "mid": {
                "focus": "Advanced SQL (CTEs, window functions), automated Python data cleaning, A/B test analysis, star-schema data modeling, and executive storytelling.",
                "expected_skills": ["sql", "python", "tableau", "a/b testing & hypothesis testing", "data modeling", "business acumen & kpi tracking"],
                "projects": ["Subscription Product Funnel & Cohort Retention Model", "Automated Financial Reconciliation Pipeline", "Marketing Campaign ROI Attribution Model"]
            },
            "senior": {
                "focus": "Enterprise data warehouse architecture, dbt modeling, statistical experimentation governance, forecasting, and cross-departmental executive influence.",
                "expected_skills": ["dbt", "snowflake", "bigquery", "statistical modeling", "reporting & executive dashboards", "data governance & privacy"],
                "projects": ["Modern Data Stack Transformation (dbt + Snowflake + Looker)", "Algorithmic Pricing Elasticity Model", "Enterprise KPI Governance Framework"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "Spreadsheets & Excel Mastery",
                "skills": ["microsoft excel", "descriptive statistics"],
                "description": "Master advanced formulas (XLOOKUP, INDEX/MATCH), pivot tables, data validation, and descriptive stats.",
                "resources": [
                    {"title": "Microsoft Excel Video Training", "url": "https://support.microsoft.com/en-us/office/excel-video-training-9bc05390-e94c-46af-a5b3-d7c22f6990bb", "type": "free_doc"},
                    {"title": "Khan Academy Statistics and Probability", "url": "https://www.khanacademy.org/math/statistics-probability", "type": "free_course"}
                ]
            },
            {
                "step": 2,
                "topic": "SQL & Relational Databases",
                "skills": ["sql", "relational database concepts"],
                "description": "Master queries: SELECT, JOIN, GROUP BY, HAVING, subqueries, CTEs, and window functions (ROW_NUMBER, LAG, LEAD).",
                "resources": [
                    {"title": "Mode Analytics SQL Tutorial for Data Analysis", "url": "https://mode.com/sql-tutorial/", "type": "free_doc"},
                    {"title": "SQLBolt Interactive Lessons", "url": "https://sqlbolt.com", "type": "free_interactive"}
                ]
            },
            {
                "step": 3,
                "topic": "BI Dashboards & Data Visualization",
                "skills": ["power bi", "tableau", "data visualization"],
                "description": "Build interactive executive dashboards, configure data connections, DAX calculated measures, and visual hierarchy.",
                "resources": [
                    {"title": "Microsoft Learn Power BI Career Path", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "type": "free_course"},
                    {"title": "Tableau Free Training Videos", "url": "https://www.tableau.com/learn/training", "type": "free_course"}
                ]
            },
            {
                "step": 4,
                "topic": "Python for Data Analysis",
                "skills": ["python", "exploratory data analysis", "data cleaning & preprocessing"],
                "description": "Pandas DataFrames, NumPy vectorization, Matplotlib/Seaborn visualizations, and automated data cleaning.",
                "resources": [
                    {"title": "Kaggle Learn: Python & Pandas", "url": "https://www.kaggle.com/learn/pandas", "type": "free_interactive"},
                    {"title": "Python Data Science Handbook (Free Online)", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/", "type": "free_doc"}
                ]
            },
            {
                "step": 5,
                "topic": "Applied Statistics & A/B Testing",
                "skills": ["a/b testing & hypothesis testing", "business acumen & kpi tracking"],
                "description": "Hypothesis testing, confidence intervals, sample size calculation, p-values, and conversion rate experimentation.",
                "resources": [
                    {"title": "Penn State STAT 500 Applied Statistics", "url": "https://online.stat.psu.edu/stat500/", "type": "free_doc"},
                    {"title": "Evan Miller A/B Testing Guide", "url": "https://www.evanmiller.org/ab-testing/", "type": "free_doc"}
                ]
            },
            {
                "step": 6,
                "topic": "Data Warehousing & Dimensional Modeling",
                "skills": ["data modeling", "snowflake", "dbt"],
                "description": "Kimball dimensional modeling, star schemas, snowflake schemas, cloud warehouses (BigQuery/Snowflake), and dbt.",
                "resources": [
                    {"title": "dbt Learn Fundamentals Course", "url": "https://courses.getdbt.com/courses/fundamentals", "type": "free_course"},
                    {"title": "Snowflake Documentation & Tutorials", "url": "https://docs.snowflake.com", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://roadmap.sh/data-analyst",
            "https://www.onetonline.org/link/summary/15-2051.01",
            "https://learn.microsoft.com/en-us/certifications/power-bi-data-analyst-associate/"
        ],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Data Scientist/ML Engineer",
        "slug": "data-scientist-ml-engineer",
        "aliases": ["Data Scientist", "Machine Learning Engineer", "ML Engineer", "Applied AI Scientist"],
        "model_classes": {"Data Science": 0.70, "Python Developer": 0.20, "Database": 0.10},
        "action_verbs": ["trained", "fine-tuned", "architected", "deployed", "optimized", "benchmarked", "evaluated", "engineered", "formulated"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": True
        },
        "critical_skills": [
            "python", "machine learning algorithms", "deep learning", "pytorch",
            "tensorflow", "scikit-learn", "statistics & probability", "feature engineering",
            "sql for data science", "model evaluation metrics", "natural language processing",
            "computer vision basics", "mlops", "model deployment", "git & version control",
            "exploratory data analysis", "data cleaning & imputation"
        ],
        "bonus_skills": [
            "large language models", "rag & vector databases", "distributed training",
            "model optimization", "cloud ml platforms", "big data processing",
            "feature stores", "kubeflow", "model monitoring & drift detection",
            "time series forecasting", "reinforcement learning", "explainable ai",
            "cuda", "ci/cd for ml", "data scraping & collection"
        ],
        "skill_synonyms": {
            "python": ["python 3", "numpy", "pandas", "scipy"],
            "machine learning algorithms": ["classical ml", "random forest", "xgboost", "lightgbm", "svm", "gradient boosting"],
            "deep learning": ["neural networks", "deep neural networks", "cnn", "rnn", "transformers", "lstm"],
            "pytorch": ["torch", "torchvision", "torchaudio"],
            "tensorflow": ["tf", "keras", "tf.keras"],
            "scikit-learn": ["sklearn", "scikit learn"],
            "statistics & probability": ["bayesian statistics", "hypothesis testing", "probability theory", "statistical inference"],
            "feature engineering": ["feature extraction", "feature selection", "pca", "one-hot encoding", "scaling"],
            "sql for data science": ["sql", "advanced sql", "data extraction"],
            "model evaluation metrics": ["roc-auc", "precision", "recall", "f1-score", "rmse", "cross-validation"],
            "natural language processing": ["nlp", "bert", "hugging face", "tokenization", "text classification", "spacy"],
            "computer vision basics": ["cv", "opencv", "image classification", "object detection", "yolo"],
            "mlops": ["mlflow", "weights & biases", "wandb", "dvc", "experiment tracking"],
            "model deployment": ["fastapi", "docker", "model serving", "triton", "torchserve", "flask api"],
            "git & version control": ["git", "github", "dvc"],
            "exploratory data analysis": ["eda", "matplotlib", "seaborn", "data visualization"],
            "data cleaning & imputation": ["data preprocessing", "smote", "handling missing data", "outlier removal"],
            "large language models": ["llms", "llama", "mistral", "fine-tuning", "lora", "peft", "prompt engineering"],
            "rag & vector databases": ["rag", "retrieval augmented generation", "faiss", "pinecone", "chromadb", "langchain", "llamaindex"],
            "distributed training": ["ddp", "distributed data parallel", "deepspeed", "ray train", "horovod"],
            "model optimization": ["tensorrt", "onnx", "quantization", "pruning", "fp16", "int8"],
            "cloud ml platforms": ["aws sagemaker", "gcp vertex ai", "azure ml"],
            "big data processing": ["apache spark", "pyspark", "databricks"],
            "feature stores": ["feast", "hopsworks"],
            "kubeflow": ["kubernetes for ml", "kserve"],
            "model monitoring & drift detection": ["data drift", "concept drift", "evidently ai", "whylabs"],
            "time series forecasting": ["arima", "prophet", "neuralprophet", "time series"],
            "reinforcement learning": ["rl", "rlhf", "q-learning", "policy gradients"],
            "explainable ai": ["xai", "shap", "lime", "model interpretability"],
            "cuda": ["gpu acceleration", "cuda c++"],
            "ci/cd for ml": ["cml", "github actions for ml"],
            "data scraping & collection": ["beautifulsoup", "scrapy", "selenium"]
        },
        "tools": ["PyTorch", "Jupyter", "Weights & Biases", "MLflow", "Docker", "FastAPI", "Hugging Face", "AWS SageMaker"],
        "certifications": [
            "AWS Certified Machine Learning - Specialty",
            "TensorFlow Developer Certificate",
            "Databricks Certified Machine Learning Associate"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Data exploration, feature engineering, training standard scikit-learn models (regression, classification), model evaluation, and baseline neural networks.",
                "expected_skills": ["python", "scikit-learn", "sql for data science", "exploratory data analysis", "model evaluation metrics", "machine learning algorithms"],
                "projects": ["Customer Churn Prediction with XGBoost & SHAP", "Housing Price Prediction with Advanced Feature Engineering", "Image Classifier using PyTorch Transfer Learning"]
            },
            "mid": {
                "focus": "Deep learning architectures (Transformers, CNNs), MLOps pipelines with MLflow, deploying models as containerized FastAPI services, and hyperparameter tuning.",
                "expected_skills": ["deep learning", "pytorch", "natural language processing", "mlops", "model deployment", "feature engineering"],
                "projects": ["Production Sentiment & Intent Classification API with BERT & FastAPI", "RAG Pipeline over Domain Documents with FAISS", "Automated Defect Detection with YOLO & OpenCV"]
            },
            "senior": {
                "focus": "Distributed multi-GPU training, LLM fine-tuning (LoRA/PEFT), inference acceleration with TensorRT/ONNX, model drift monitoring, and enterprise AI strategy.",
                "expected_skills": ["large language models", "distributed training", "model optimization", "cloud ml platforms", "model monitoring & drift detection"],
                "projects": ["Domain-Specific LLM Fine-Tuning Pipeline with LoRA & DeepSpeed", "High-Throughput Low-Latency Inference Engine on TensorRT", "Automated Retraining & Drift Detection Pipeline in Vertex AI"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "Mathematics, Probability & Linear Algebra",
                "skills": ["statistics & probability"],
                "description": "Matrix operations, eigenvalues, derivatives, gradient descent, probability distributions, and hypothesis testing.",
                "resources": [
                    {"title": "Mathematics for Machine Learning (Free Book)", "url": "https://mml-book.github.io", "type": "free_doc"},
                    {"title": "3Blue1Brown Essence of Linear Algebra", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "type": "free_course"}
                ]
            },
            {
                "step": 2,
                "topic": "Data Preprocessing & Classical ML",
                "skills": ["machine learning algorithms", "scikit-learn", "feature engineering", "model evaluation metrics"],
                "description": "Regression, classification, tree ensembles (Random Forest, XGBoost), cross-validation, and metrics (F1, ROC-AUC).",
                "resources": [
                    {"title": "Scikit-Learn Official User Guide", "url": "https://scikit-learn.org/stable/user_guide.html", "type": "free_doc"},
                    {"title": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "type": "free_course"}
                ]
            },
            {
                "step": 3,
                "topic": "Deep Learning with PyTorch",
                "skills": ["deep learning", "pytorch", "natural language processing"],
                "description": "Tensors, autograd, feedforward networks, CNNs, RNNs, and self-attention Transformer mechanisms.",
                "resources": [
                    {"title": "PyTorch Official Tutorials", "url": "https://pytorch.org/tutorials/", "type": "free_doc"},
                    {"title": "Fast.ai Practical Deep Learning for Coders", "url": "https://course.fast.ai", "type": "free_course"}
                ]
            },
            {
                "step": 4,
                "topic": "Transformers, LLMs & Generative AI",
                "skills": ["natural language processing", "large language models", "rag & vector databases"],
                "description": "Hugging Face ecosystem, BERT/GPT architectures, tokenization, LoRA fine-tuning, RAG, and vector search.",
                "resources": [
                    {"title": "Hugging Face NLP Course", "url": "https://huggingface.co/learn/nlp-course/chapter1/1", "type": "free_course"},
                    {"title": "DeepLearning.AI Short Courses", "url": "https://www.deeplearning.ai/short-courses/", "type": "free_course"}
                ]
            },
            {
                "step": 5,
                "topic": "MLOps & Model Deployment",
                "skills": ["mlops", "model deployment", "model optimization"],
                "description": "Packaging models in Docker, building inference microservices in FastAPI, tracking experiments with MLflow, and ONNX export.",
                "resources": [
                    {"title": "Made With ML (Production MLOps)", "url": "https://madewithml.com", "type": "free_course"},
                    {"title": "MLflow Documentation", "url": "https://mlflow.org/docs/latest/index.html", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://roadmap.sh/ai-data-scientist",
            "https://www.onetonline.org/link/summary/15-2051.00",
            "https://scikit-learn.org",
            "https://pytorch.org/tutorials/"
        ],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Mobile App Developer",
        "slug": "mobile-app-developer",
        "aliases": ["Mobile Developer", "iOS Developer", "Android Developer", "Mobile Engineer", "Cross-Platform Mobile Developer"],
        "model_classes": {"Java Developer": 0.40, "Web Designing": 0.35, "Python Developer": 0.25},
        "action_verbs": ["developed", "published", "designed", "architected", "integrated", "optimized", "shipped", "profiled", "refactored"],
        "role_specific_rules": {
            "portfolio_required": True,
            "min_bullet_points": 4,
            "prefer_live_links": True
        },
        "critical_skills": [
            "flutter", "react native", "native android", "native ios",
            "mobile ui/ux principles", "state management for mobile", "restful api integration",
            "local storage", "push notifications", "app permissions & hardware apis",
            "mobile lifecycle management", "git", "debugging & profiling",
            "app publishing & store guidelines", "responsive layouts & orientation",
            "mobile app architecture", "asynchronous programming", "offline-first architecture"
        ],
        "bonus_skills": [
            "mobile ci/cd", "mobile testing", "mobile security", "graphql for mobile",
            "deep linking & universal links", "in-app purchases", "mobile analytics & crash reporting",
            "bluetooth & iot integration", "websockets & real-time sync",
            "mobile performance optimization", "kotlin multiplatform", "arkit / arcore",
            "micro-apps & modularization", "payment gateway sdks", "mobile accessibility"
        ],
        "skill_synonyms": {
            "flutter": ["dart", "flutter sdk"],
            "react native": ["rn", "react-native", "expo"],
            "native android": ["android sdk", "kotlin", "jetpack compose", "java for android"],
            "native ios": ["swift", "swiftui", "uikit", "xcode", "cocoapods"],
            "mobile ui/ux principles": ["material design", "apple human interface guidelines", "hig"],
            "state management for mobile": ["bloc", "provider", "riverpod", "redux for mobile", "mobx mobile"],
            "restful api integration": ["retrofit", "dio", "alamofire", "http client", "axios"],
            "local storage": ["sqlite", "room database", "coredata", "hive", "sharedpreferences", "keychain"],
            "push notifications": ["firebase cloud messaging", "fcm", "apns", "onesignal"],
            "app permissions & hardware apis": ["camera api", "gps", "geolocation", "biometrics", "accelerometer"],
            "mobile lifecycle management": ["activity lifecycle", "fragment lifecycle", "viewcontroller lifecycle"],
            "git": ["github", "gitlab", "version control"],
            "debugging & profiling": ["android profiler", "xcode instruments", "memory leak debugging", "leakcanary"],
            "app publishing & store guidelines": ["google play console", "apple app store connect", "testflight", "app signing"],
            "responsive layouts & orientation": ["constraintlayout", "autolayout", "flexbox mobile"],
            "mobile app architecture": ["mvvm", "clean architecture", "mvi", "viper"],
            "asynchronous programming": ["coroutines", "kotlin coroutines", "async/await", "combine", "rxjava"],
            "offline-first architecture": ["offline sync", "caching", "background sync"],
            "mobile ci/cd": ["fastlane", "bitrise", "github actions for mobile"],
            "mobile testing": ["espresso", "xctest", "unit testing mobile", "widget testing", "appium"],
            "mobile security": ["keystore", "keychain", "proguard", "r8", "certificate pinning"],
            "graphql for mobile": ["apollo android", "apollo ios"],
            "deep linking & universal links": ["deep linking", "app links", "universal links"],
            "in-app purchases": ["iap", "revenuecat", "storekit", "google play billing"],
            "mobile analytics & crash reporting": ["crashlytics", "firebase crashlytics", "sentry mobile", "mixpanel mobile"],
            "bluetooth & iot integration": ["ble", "bluetooth low energy", "corebluetooth"],
            "websockets & real-time sync": ["socket.io mobile", "real-time synchronization"],
            "mobile performance optimization": ["app size reduction", "battery consumption", "rendering performance"],
            "kotlin multiplatform": ["kmp", "kmm"],
            "arkit / arcore": ["augmented reality mobile"],
            "micro-apps & modularization": ["modular architecture", "dynamic feature modules"],
            "payment gateway sdks": ["stripe sdk", "razorpay sdk"],
            "mobile accessibility": ["talkback", "voiceover", "dynamic type"]
        },
        "tools": ["Android Studio", "Xcode", "VS Code", "Postman", "Firebase Console", "Figma", "Git"],
        "certifications": [
            "Google Associate Android Developer Certification",
            "Meta React Native Specialization",
            "Apple Certified iOS Developer"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Building standalone mobile apps with Flutter or React Native, consuming REST APIs, handling UI navigation, local storage, and publishing demo APKs.",
                "expected_skills": ["flutter", "react native", "restful api integration", "local storage", "git", "responsive layouts & orientation"],
                "projects": ["Cross-Platform Recipe & Grocery App with SQLite", "Fitness Workout Tracker with Local Storage", "News Reader consuming HackerNews API"]
            },
            "mid": {
                "focus": "Production state management (Bloc/Riverpod), push notifications, biometric auth, offline-first sync, automated unit/widget testing, and Play/App Store publishing.",
                "expected_skills": ["state management for mobile", "push notifications", "offline-first architecture", "debugging & profiling", "app publishing & store guidelines"],
                "projects": ["Production E-Commerce App with Payment Gateway & Cart", "Real-Time Ride Hailing / Delivery App with Maps & WebSocket", "Offline-First Expense Tracker with Cloud Sync"]
            },
            "senior": {
                "focus": "Mobile architecture at scale (modular multi-repo), CI/CD pipelines with Fastlane, memory profiling/leak reduction, security hardening, and native platform bridging.",
                "expected_skills": ["mobile app architecture", "mobile ci/cd", "mobile performance optimization", "mobile security", "kotlin multiplatform"],
                "projects": ["Enterprise Banking App with Biometric Auth & Certificate Pinning", "High-Performance Video Editing Mobile Engine", "White-Label Multi-Tenant Mobile SDK"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "Core Platform & Language (Dart / Swift / Kotlin)",
                "skills": ["flutter", "native android", "native ios"],
                "description": "Choose Flutter (Dart), React Native (TS), or Native (Kotlin/Swift). Master language syntax, memory management, and OOP.",
                "resources": [
                    {"title": "Flutter Documentation & Codelabs", "url": "https://docs.flutter.dev/get-started/codelab", "type": "free_doc"},
                    {"title": "Android Developers Official Guide", "url": "https://developer.android.com/get-started/overview", "type": "free_doc"}
                ]
            },
            {
                "step": 2,
                "topic": "Mobile UI & State Management",
                "skills": ["mobile ui/ux principles", "state management for mobile", "responsive layouts & orientation"],
                "description": "Widget/View hierarchies, responsive layouts, declarative UI (Compose/SwiftUI/Flutter), and state management (Bloc/Provider).",
                "resources": [
                    {"title": "Bloc Library Official Documentation", "url": "https://bloclibrary.dev/#/gettingstarted", "type": "free_doc"},
                    {"title": "React Native State Management Guide", "url": "https://reactnative.dev/docs/intro-react", "type": "free_doc"}
                ]
            },
            {
                "step": 3,
                "topic": "Networking, Local Persistence & Offline Sync",
                "skills": ["restful api integration", "local storage", "offline-first architecture"],
                "description": "Connecting to REST/GraphQL backends, caching data locally (Room/Hive/CoreData), handling network loss, and background sync.",
                "resources": [
                    {"title": "Offline-First Mobile Architecture (Android)", "url": "https://developer.android.com/topic/architecture/data-layer/offline-first", "type": "free_doc"},
                    {"title": "Flutter Cookbook: Networking & Persistence", "url": "https://docs.flutter.dev/cookbook/networking/fetch-data", "type": "free_doc"}
                ]
            },
            {
                "step": 4,
                "topic": "Device APIs, Notifications & Permissions",
                "skills": ["app permissions & hardware apis", "push notifications"],
                "description": "Handling permissions runtime flows, GPS/location tracking, camera capture, biometric security, and FCM notifications.",
                "resources": [
                    {"title": "Firebase Cloud Messaging Documentation", "url": "https://firebase.google.com/docs/cloud-messaging", "type": "free_doc"},
                    {"title": "Apple Push Notification service Overview", "url": "https://developer.apple.com/documentation/usernotifications", "type": "free_doc"}
                ]
            },
            {
                "step": 5,
                "topic": "Profiling, Automated CI/CD & Store Deployment",
                "skills": ["debugging & profiling", "app publishing & store guidelines", "mobile ci/cd"],
                "description": "Profiling CPU/memory leaks, signing release APKs/IPAs, setting up Fastlane build automation, and publishing to Google Play/App Store.",
                "resources": [
                    {"title": "Fastlane Documentation", "url": "https://docs.fastlane.tools", "type": "free_doc"},
                    {"title": "Google Play Console Launch Checklist", "url": "https://developer.android.com/distribute", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://roadmap.sh/flutter",
            "https://roadmap.sh/android",
            "https://roadmap.sh/react-native",
            "https://developer.android.com",
            "https://developer.apple.com",
            "https://www.onetonline.org/link/summary/15-1252.00"
        ],
        "last_updated": "2026-10-22"
    },
    {
        "role": "QA/Test Automation Engineer",
        "slug": "qa-test-automation-engineer",
        "aliases": ["QA Engineer", "Software Development Engineer in Test", "SDET", "Test Automation Engineer", "Quality Assurance Analyst"],
        "model_classes": {"Automation Testing": 0.55, "Testing": 0.35, "Java Developer": 0.10},
        "action_verbs": ["automated", "tested", "validated", "engineered", "executed", "identified", "benchmarked", "integrated", "triaged"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": False
        },
        "critical_skills": [
            "test automation fundamentals", "selenium webdriver", "playwright", "cypress",
            "programming for testing", "api testing", "test frameworks",
            "test case design", "defect management & tracking", "git",
            "ci/cd integration for tests", "sql for data verification", "page object model",
            "cross-browser testing", "test reporting", "bdd / tdd principles",
            "web technologies basics"
        ],
        "bonus_skills": [
            "performance & load testing", "mobile automation", "security testing basics",
            "docker for test environments", "contract testing", "visual regression testing",
            "accessibility testing", "mocking & stubbing", "chaos engineering testing",
            "cloud testing", "code coverage analysis", "linux & shell scripting",
            "test data management", "graphql api testing", "agile / scrum methodologies"
        ],
        "skill_synonyms": {
            "test automation fundamentals": ["test automation", "test pyramid", "regression testing", "smoke testing", "sanity testing", "qa fundamentals"],
            "selenium webdriver": ["selenium", "selenium grid", "webdriver"],
            "playwright": ["playwright test", "playwright testing"],
            "cypress": ["cypress.io", "cypress testing"],
            "programming for testing": ["python for automation", "java for automation", "typescript for automation", "javascript"],
            "api testing": ["postman", "rest assured", "newman", "api automation"],
            "test frameworks": ["pytest", "junit", "testng", "mocha", "jasmine"],
            "test case design": ["test cases", "boundary value analysis", "equivalence partitioning", "test scenarios"],
            "defect management & tracking": ["jira", "bugzilla", "bug life cycle", "defect tracking"],
            "git": ["github", "gitlab", "version control"],
            "ci/cd integration for tests": ["jenkins", "github actions for testing", "gitlab ci", "test pipelines"],
            "sql for data verification": ["sql", "database testing", "data validation queries"],
            "page object model": ["pom", "page objects", "pom design pattern"],
            "cross-browser testing": ["browserstack", "saucelabs", "cross-browser compatibility"],
            "test reporting": ["allure report", "extentreports", "html reports"],
            "bdd / tdd principles": ["cucumber", "gherkin", "bdd", "tdd", "specflow"],
            "web technologies basics": ["html selectors", "css selectors", "xpath"],
            "performance & load testing": ["jmeter", "k6", "locust", "load testing", "performance testing"],
            "mobile automation": ["appium", "espresso", "xcuitest", "mobile testing"],
            "security testing basics": ["owasp zap", "vulnerability scanning", "dast"],
            "docker for test environments": ["docker", "containerized testing"],
            "contract testing": ["pact", "contract tests"],
            "visual regression testing": ["percy", "applitools"],
            "accessibility testing": ["axe-core", "wave", "a11y testing"],
            "mocking & stubbing": ["wiremock", "mockito"],
            "chaos engineering testing": ["chaos testing"],
            "cloud testing": ["aws device farm", "lambdatest"],
            "code coverage analysis": ["jacoco", "coverage.py", "sonar"],
            "linux & shell scripting": ["bash", "shell scripts"],
            "test data management": ["synthetic test data", "mock data generation"],
            "graphql api testing": ["graphql testing"],
            "agile / scrum methodologies": ["agile testing", "sprint testing"]
        },
        "tools": ["Playwright", "Selenium", "Postman", "Jira", "JMeter", "Git", "Jenkins", "VS Code"],
        "certifications": [
            "ISTQB Certified Tester Foundation Level (CTFL)",
            "ISTQB Test Automation Engineer (CT-TAE)",
            "Postman API Fundamentals Student Expert"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Manual test case creation, executing regression suites, bug logging in Jira, basic Selenium/Playwright scripts, and Postman API verification.",
                "expected_skills": ["test automation fundamentals", "test case design", "defect management & tracking", "api testing", "git", "web technologies basics"],
                "projects": ["Automated E-Commerce Smoke Test Suite with Playwright", "RESTful API Validation Suite with Postman & Newman", "Comprehensive Test Plan & Bug Matrix for Web App"]
            },
            "mid": {
                "focus": "Designing Page Object Model (POM) automation frameworks, CI/CD automated test gates in GitHub Actions, DB state assertions, and BDD with Cucumber.",
                "expected_skills": ["playwright", "selenium webdriver", "page object model", "test frameworks", "ci/cd integration for tests", "bdd / tdd principles"],
                "projects": ["Scalable Cross-Browser Testing Framework in PyTest/Playwright", "Automated Microservice API Testing Suite with REST Assured", "Dockerized Test Grid with Allure Reporting"]
            },
            "senior": {
                "focus": "Enterprise test architecture, shift-left testing strategy, performance testing with k6/JMeter, contract testing with Pact, and test flakiness elimination.",
                "expected_skills": ["performance & load testing", "contract testing", "mobile automation", "docker for test environments", "test reporting"],
                "projects": ["High-Concurrency Load Testing Framework with k6 & Grafana", "Enterprise Contract Testing Strategy with Pact & CI/CD", "Unified Multi-Platform Mobile & Web Testing Architecture"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "Testing Principles & Test Case Design",
                "skills": ["test automation fundamentals", "test case design", "defect management & tracking"],
                "description": "Test pyramid, functional vs non-functional testing, boundary value analysis, equivalence partitioning, and Jira bug tracking.",
                "resources": [
                    {"title": "Ministry of Testing - Foundations of Software Testing", "url": "https://www.ministryoftesting.com", "type": "free_doc"},
                    {"title": "Guru99 Software Testing Fundamentals", "url": "https://www.guru99.com/software-testing.html", "type": "free_doc"}
                ]
            },
            {
                "step": 2,
                "topic": "Programming & Web Selectors",
                "skills": ["programming for testing", "web technologies basics", "git"],
                "description": "Python or TypeScript for scripting, understanding DOM, XPath, CSS selectors, assertions, and Git workflows.",
                "resources": [
                    {"title": "W3Schools XPath Tutorial", "url": "https://www.w3schools.com/xml/xpath_intro.asp", "type": "free_doc"},
                    {"title": "Automate the Boring Stuff with Python", "url": "https://automatetheboringstuff.com", "type": "free_doc"}
                ]
            },
            {
                "step": 3,
                "topic": "Modern Web Automation with Playwright",
                "skills": ["playwright", "page object model", "test frameworks"],
                "description": "Installing Playwright, writing resilient tests with auto-waiting, implementing Page Object Model, and PyTest/Jest fixtures.",
                "resources": [
                    {"title": "Playwright Official Getting Started", "url": "https://playwright.dev/docs/intro", "type": "free_doc"},
                    {"title": "Playwright Page Object Models Guide", "url": "https://playwright.dev/docs/pom", "type": "free_doc"}
                ]
            },
            {
                "step": 4,
                "topic": "API Testing & Automation",
                "skills": ["api testing", "sql for data verification"],
                "description": "Testing HTTP verbs, status codes, JSON schema validation, automated runs with Newman/PyTest requests, and verifying database state.",
                "resources": [
                    {"title": "Postman Learning Center & Student Program", "url": "https://learning.postman.com/docs/getting-started/overview/", "type": "free_doc"},
                    {"title": "REST Assured Official Getting Started", "url": "https://rest-assured.io", "type": "free_doc"}
                ]
            },
            {
                "step": 5,
                "topic": "CI/CD Integration, Reporting & Performance Testing",
                "skills": ["ci/cd integration for tests", "test reporting", "performance & load testing"],
                "description": "Integrating test runs into GitHub Actions / Jenkins, generating rich Allure HTML reports, and load testing APIs with k6.",
                "resources": [
                    {"title": "k6 Documentation for Performance Testing", "url": "https://k6.io/docs/", "type": "free_doc"},
                    {"title": "Allure Report Documentation", "url": "https://allurereport.org/docs/", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://roadmap.sh/qa",
            "https://www.onetonline.org/link/summary/15-1253.00",
            "https://playwright.dev",
            "https://www.selenium.dev"
        ],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Software Engineer (generic)",
        "slug": "software-engineer-generic",
        "aliases": ["Software Engineer", "Software Developer", "SWE", "Application Developer", "Generalist Software Engineer"],
        "model_classes": {"Java Developer": 0.35, "Python Developer": 0.35, "DotNet Developer": 0.15, "Database": 0.15},
        "action_verbs": ["engineered", "developed", "architected", "implemented", "optimized", "refactored", "built", "debugged", "designed"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": False
        },
        "critical_skills": [
            "data structures & algorithms", "object-oriented programming", "git & version control",
            "core programming language", "sql & database basics", "restful apis",
            "clean code & design principles", "unit testing & tdd", "debugging & problem solving",
            "operating systems fundamentals", "computer networking basics",
            "software development life cycle", "basic linux & cli", "code review & documentation",
            "design patterns", "docker basics", "ci/cd fundamentals"
        ],
        "bonus_skills": [
            "microservices architecture", "cloud computing fundamentals", "nosql databases",
            "message queues", "system design", "kubernetes fundamentals",
            "web security basics", "concurrency & multithreading", "graphql basics",
            "infrastructure as code", "performance profiling & optimization",
            "build tools", "continuous monitoring", "domain-driven design",
            "open source contribution"
        ],
        "skill_synonyms": {
            "data structures & algorithms": ["dsa", "algorithms", "data structures", "time complexity", "big o", "leetcode"],
            "object-oriented programming": ["oop", "object oriented design", "encapsulation", "polymorphism", "inheritance"],
            "git & version control": ["git", "github", "gitlab", "pull requests", "version control"],
            "core programming language": ["python", "java", "c++", "c#", "golang", "go", "typescript"],
            "sql & database basics": ["sql", "rdbms", "database schema", "acid"],
            "restful apis": ["rest api", "restful api", "api integration", "http methods"],
            "clean code & design principles": ["solid principles", "dry", "kiss", "clean code", "clean architecture"],
            "unit testing & tdd": ["unit testing", "tdd", "test driven development", "junit", "pytest"],
            "debugging & problem solving": ["debugging", "troubleshooting", "stack traces", "profiling"],
            "operating systems fundamentals": ["os concepts", "threads", "processes", "memory management"],
            "computer networking basics": ["tcp/ip", "http", "https", "dns", "networking"],
            "software development life cycle": ["sdlc", "agile", "scrum", "kanban"],
            "basic linux & cli": ["linux", "bash", "command line", "ssh"],
            "code review & documentation": ["code review", "technical documentation", "markdown"],
            "design patterns": ["gang of four", "factory pattern", "singleton pattern", "observer pattern"],
            "docker basics": ["docker", "containerization", "dockerfile"],
            "ci/cd fundamentals": ["ci/cd", "continuous integration", "github actions"],
            "microservices architecture": ["microservices", "distributed systems"],
            "cloud computing fundamentals": ["aws", "gcp", "azure", "cloud basics"],
            "nosql databases": ["mongodb", "redis", "dynamodb"],
            "message queues": ["rabbitmq", "kafka"],
            "system design": ["scalability", "high availability", "load balancing", "caching"],
            "kubernetes fundamentals": ["k8s", "kubernetes"],
            "web security basics": ["owasp", "security best practices", "hashing"],
            "concurrency & multithreading": ["multithreading", "async", "concurrency"],
            "graphql basics": ["graphql"],
            "infrastructure as code": ["terraform"],
            "performance profiling & optimization": ["performance tuning", "memory leaks"],
            "build tools": ["maven", "gradle", "make", "cmake"],
            "continuous monitoring": ["prometheus", "grafana"],
            "domain-driven design": ["ddd"],
            "open source contribution": ["open source", "foss"]
        },
        "tools": ["Git", "VS Code / IntelliJ", "Docker", "Postman", "Linux Terminal", "GitHub"],
        "certifications": [
            "AWS Certified Cloud Practitioner",
            "GitHub Foundations Certification",
            "Oracle Certified Associate Java Programmer"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Strong Computer Science core (DSA, Big-O, OOP), clean syntax in Python/Java/C++, writing unit tests, and building full-stack CRUD applications.",
                "expected_skills": ["data structures & algorithms", "object-oriented programming", "git & version control", "core programming language", "sql & database basics", "clean code & design principles"],
                "projects": ["Multi-User Task Management App with Authentication", "Algorithms & Data Structures Portfolio in C++/Python", "CLI Tool for Log Parsing & File Organization"]
            },
            "mid": {
                "focus": "Software design patterns, microservice APIs, relational & NoSQL databases, Docker containerization, CI/CD automated deployment, and system architecture.",
                "expected_skills": ["design patterns", "restful apis", "docker basics", "unit testing & tdd", "system design", "operating systems fundamentals"],
                "projects": ["Microservices-Based Notification Service with Redis & Docker", "High-Performance REST API with Caching & Rate Limiting", "Distributed File Storage Client"]
            },
            "senior": {
                "focus": "Enterprise system design (high availability, partitioning, caching), technical leadership, cross-system refactoring, architectural specifications, and mentorship.",
                "expected_skills": ["system design", "microservices architecture", "cloud computing fundamentals", "concurrency & multithreading", "performance profiling & optimization"],
                "projects": ["Scalable Distributed Rate Limiter & Token Bucket Service", "High-Volume Transaction Processing Engine", "Zero-Downtime Database Sharding Engine"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "Programming Fundamentals & Clean Code",
                "skills": ["core programming language", "object-oriented programming", "clean code & design principles"],
                "description": "Master language depth (memory, typing, OOP/functional), SOLID principles, and clean code conventions.",
                "resources": [
                    {"title": "CS50 Introduction to Computer Science (Harvard)", "url": "https://cs50.harvard.edu/x/", "type": "free_course"},
                    {"title": "Clean Code Summary & Patterns", "url": "https://github.com/ryanmcdermott/clean-code-javascript", "type": "free_doc"}
                ]
            },
            {
                "step": 2,
                "topic": "Data Structures & Algorithms",
                "skills": ["data structures & algorithms", "debugging & problem solving"],
                "description": "Arrays, linked lists, trees, graphs, heaps, hash maps, sorting, binary search, and dynamic programming.",
                "resources": [
                    {"title": "NeetCode DSA Roadmap", "url": "https://neetcode.io/roadmap", "type": "free_interactive"},
                    {"title": "Visualgo Algorithm Visualizations", "url": "https://visualgo.net", "type": "free_interactive"}
                ]
            },
            {
                "step": 3,
                "topic": "Databases, Networking & APIs",
                "skills": ["sql & database basics", "restful apis", "computer networking basics"],
                "description": "RDBMS schema design, indexing, transactions, TCP/IP, HTTP semantics, and building REST APIs.",
                "resources": [
                    {"title": "MDN Overview of HTTP", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview", "type": "free_doc"},
                    {"title": "Database Systems Course (CMU 15-445 Open Notes)", "url": "https://15445.courses.cs.cmu.edu", "type": "free_doc"}
                ]
            },
            {
                "step": 4,
                "topic": "System Design & Architecture",
                "skills": ["system design", "microservices architecture", "design patterns"],
                "description": "Scalability, load balancing, caching, database partitioning, asynchronous processing, and Gang of Four design patterns.",
                "resources": [
                    {"title": "The System Design Primer (Donne Martin)", "url": "https://github.com/donnemartin/system-design-primer", "type": "free_doc"},
                    {"title": "Refactoring Guru - Design Patterns", "url": "https://refactoring.guru/design-patterns", "type": "free_doc"}
                ]
            },
            {
                "step": 5,
                "topic": "DevOps, Containers & Cloud",
                "skills": ["docker basics", "ci/cd fundamentals", "cloud computing fundamentals"],
                "description": "Containerizing applications with Docker, writing GitHub Actions CI/CD pipelines, and cloud computing basics.",
                "resources": [
                    {"title": "Docker Official Get Started", "url": "https://docs.docker.com/get-started/", "type": "free_doc"},
                    {"title": "AWS Cloud Essentials Documentation", "url": "https://aws.amazon.com/getting-started/", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://roadmap.sh/computer-science",
            "https://roadmap.sh/software-architect",
            "https://www.onetonline.org/link/summary/15-1252.00",
            "https://teachyourselfcs.com"
        ],
        "last_updated": "2026-10-22"
    },
    {
        "role": "SRE",
        "slug": "sre",
        "aliases": ["Site Reliability Engineer", "Reliability Engineer", "Infrastructure Engineer", "Cloud SRE", "Platform Reliability Engineer"],
        "model_classes": {"DevOps Engineer": 0.65, "Network Security Engineer": 0.20, "Database": 0.15},
        "action_verbs": ["automated", "orchestrated", "architected", "mitigated", "optimized", "monitored", "hardened", "scaled", "troubleshot"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": False
        },
        "critical_skills": [
            "linux systems administration", "kubernetes", "infrastructure as code", "ci/cd automation",
            "monitoring & observability", "logging systems", "sli / slo / sla management",
            "incident management & on-call", "python or go for tooling", "cloud computing",
            "networking protocols", "docker & container runtimes", "load balancing & reverse proxies",
            "distributed tracing", "shell scripting", "capacity planning & autoscaling",
            "high availability & disaster recovery"
        ],
        "bonus_skills": [
            "chaos engineering", "service mesh", "security & compliance", "configuration management",
            "gitops", "database reliability", "helm & kustomize", "ebpf",
            "secret management", "cost optimization / finops", "cdn architecture",
            "message broker operations", "sre handbook practices", "kernel tuning",
            "zero-trust architecture"
        ],
        "skill_synonyms": {
            "linux systems administration": ["linux", "kernel", "systemd", "procfs", "sysadmin", "unix"],
            "kubernetes": ["k8s", "k8s cluster", "pods", "deployments", "kubectl"],
            "infrastructure as code": ["terraform", "opentofu", "cloudformation", "iac"],
            "ci/cd automation": ["github actions", "gitlab ci", "argocd", "jenkins", "ci/cd"],
            "monitoring & observability": ["prometheus", "grafana", "observability", "metrics", "datadog"],
            "logging systems": ["elk", "elk stack", "elasticsearch", "fluentd", "loki", "logstash"],
            "sli / slo / sla management": ["slo", "sli", "sla", "error budgets", "service level objectives"],
            "incident management & on-call": ["postmortems", "rca", "root cause analysis", "pagerduty", "incident response"],
            "python or go for tooling": ["python scripting", "golang", "go for automation"],
            "cloud computing": ["aws", "gcp", "google cloud", "azure", "cloud architecture"],
            "networking protocols": ["tcp/ip", "dns", "bgp", "tls/ssl", "http/2", "vpc"],
            "docker & container runtimes": ["docker", "containerd", "cgroups", "namespaces"],
            "load balancing & reverse proxies": ["nginx", "haproxy", "envoy", "alb"],
            "distributed tracing": ["opentelemetry", "jaeger", "tempo", "tracing"],
            "shell scripting": ["bash", "shell scripts", "sh"],
            "capacity planning & autoscaling": ["hpa", "vpa", "cluster autoscaler", "autoscaling"],
            "high availability & disaster recovery": ["ha", "disaster recovery", "failover", "multi-region"],
            "chaos engineering": ["chaos mesh", "gremlin", "chaos testing"],
            "service mesh": ["istio", "linkerd"],
            "security & compliance": ["falco", "trivy", "kyverno", "cis benchmarks"],
            "configuration management": ["ansible", "puppet", "chef"],
            "gitops": ["argocd", "fluxcd", "gitops workflow"],
            "database reliability": ["postgresql replication", "patroni", "pgbouncer"],
            "helm & kustomize": ["helm", "helm charts", "kustomize"],
            "ebpf": ["cilium", "ebpf monitoring"],
            "secret management": ["vault", "hashicorp vault", "external secrets operator"],
            "cost optimization / finops": ["finops", "kubecost", "cloud cost reduction"],
            "cdn architecture": ["cloudflare", "cloudfront", "fastly"],
            "message broker operations": ["kafka cluster", "rabbitmq cluster"],
            "sre handbook practices": ["google sre", "site reliability engineering book"],
            "kernel tuning": ["sysctl", "iptables", "nftables"],
            "zero-trust architecture": ["zero trust", "mTLS"]
        },
        "tools": ["Kubernetes", "Terraform", "Prometheus", "Grafana", "Docker", "AWS / GCP", "Bash", "PagerDuty"],
        "certifications": [
            "Certified Kubernetes Administrator (CKA)",
            "AWS Certified DevOps Engineer - Professional",
            "HashiCorp Certified: Terraform Associate"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Linux administration, writing Bash/Python automation scripts, containerizing apps with Docker, and setting up Prometheus/Grafana monitors.",
                "expected_skills": ["linux systems administration", "shell scripting", "docker & container runtimes", "cloud computing", "monitoring & observability"],
                "projects": ["Automated Linux Server Provisioning & Hardening Script", "Dockerized Web App with Prometheus Metrics & Grafana Dashboard", "Automated Backup & Health Check Daemon"]
            },
            "mid": {
                "focus": "Kubernetes cluster administration, Infrastructure as Code with Terraform, defining SLOs/SLIs with error budgets, CI/CD with ArgoCD, and incident response.",
                "expected_skills": ["kubernetes", "infrastructure as code", "ci/cd automation", "sli / slo / sla management", "incident management & on-call", "networking protocols"],
                "projects": ["Production Kubernetes Cluster on AWS using Terraform & Helm", "Full Observability Stack with OpenTelemetry, Prometheus & Jaeger", "Automated Canary Deployment Pipeline with Argo Rollouts"]
            },
            "senior": {
                "focus": "Multi-region high availability, disaster recovery exercises, chaos engineering, eBPF network observability, enterprise error budget governance, and architectural resilience.",
                "expected_skills": ["chaos engineering", "high availability & disaster recovery", "service mesh", "ebpf", "cost optimization / finops"],
                "projects": ["Multi-Region Automated Failover & Disaster Recovery Mesh", "Chaos Engineering Injection Platform with Chaos Mesh", "Enterprise FinOps & Cloud Cost Optimization Architecture"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "Linux Systems & Networking Internals",
                "skills": ["linux systems administration", "networking protocols", "shell scripting"],
                "description": "Kernel parameters, process lifecycle, systemd, memory management, TCP/IP handshake, DNS resolution, and Bash scripting.",
                "resources": [
                    {"title": "Linux Journey (Free Interactive Linux Guide)", "url": "https://linuxjourney.com", "type": "free_interactive"},
                    {"title": "Beej's Guide to Network Programming", "url": "https://beej.us/guide/bgnet/", "type": "free_doc"}
                ]
            },
            {
                "step": 2,
                "topic": "Containers & Kubernetes Orchestration",
                "skills": ["docker & container runtimes", "kubernetes", "capacity planning & autoscaling"],
                "description": "Container internals (namespaces, cgroups), Kubernetes architecture (control plane, kubelet), deployments, and ingress.",
                "resources": [
                    {"title": "Kubernetes Official Tutorials", "url": "https://kubernetes.io/docs/tutorials/", "type": "free_doc"},
                    {"title": "Mumshad Mannambeth CKA Study Resources", "url": "https://github.com/kodekloudhub/certified-kubernetes-administrator-course", "type": "free_doc"}
                ]
            },
            {
                "step": 3,
                "topic": "Infrastructure as Code & Cloud",
                "skills": ["infrastructure as code", "cloud computing", "ci/cd automation"],
                "description": "Declarative cloud provisioning with Terraform, state management, AWS VPCs/IAM, and GitHub Actions / GitOps pipelines.",
                "resources": [
                    {"title": "HashiCorp Terraform Tutorials", "url": "https://developer.hashicorp.com/terraform/tutorials", "type": "free_doc"},
                    {"title": "AWS Well-Architected Framework", "url": "https://aws.amazon.com/architecture/well-architected/", "type": "free_doc"}
                ]
            },
            {
                "step": 4,
                "topic": "Observability: Metrics, Logs & Traces",
                "skills": ["monitoring & observability", "logging systems", "distributed tracing"],
                "description": "Prometheus metric types, PromQL queries, Grafana visualization, Loki/ELK log aggregation, and OpenTelemetry distributed tracing.",
                "resources": [
                    {"title": "Prometheus Official Getting Started", "url": "https://prometheus.io/docs/introduction/first_steps/", "type": "free_doc"},
                    {"title": "OpenTelemetry Documentation", "url": "https://opentelemetry.io/docs/", "type": "free_doc"}
                ]
            },
            {
                "step": 5,
                "topic": "Site Reliability Principles & Incident Management",
                "skills": ["sli / slo / sla management", "incident management & on-call", "chaos engineering"],
                "description": "Google SRE tenets, SLI/SLO calculations, error budget exhaustion policies, blameless postmortems, and chaos engineering.",
                "resources": [
                    {"title": "Google Site Reliability Engineering Books (Free Online)", "url": "https://sre.google/books/", "type": "free_doc"},
                    {"title": "Google SRE Workbook", "url": "https://sre.google/workbook/table-of-contents/", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://roadmap.sh/devops",
            "https://sre.google/sre-book/table-of-contents/",
            "https://kubernetes.io/docs/"
        ],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Product Manager",
        "slug": "product-manager",
        "aliases": ["Product Owner", "Technical Product Manager", "Associate Product Manager", "APM", "Senior Product Manager"],
        "model_classes": {"PMO": 0.40, "Operations Manager": 0.35, "Business Analyst": 0.25},
        "action_verbs": ["launched", "strategized", "prioritized", "spearheaded", "orchestrated", "accelerated", "defined", "negotiated", "aligned"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": True
        },
        "critical_skills": [
            "product strategy & vision", "user research & customer discovery", "product lifecycle management",
            "agile & scrum methodologies", "prd writing", "prioritization frameworks",
            "product analytics & kpis", "a/b testing & experimentation", "cross-functional leadership",
            "wireframing & prototyping basics", "data analysis", "competitive & market analysis",
            "go-to-market strategy", "stakeholder management & communication", "product discovery",
            "customer journey mapping"
        ],
        "bonus_skills": [
            "analytics tools", "jira / confluence administration", "technical literacy",
            "pricing & monetization strategy", "product-led growth", "financial modeling & unit economics",
            "ux / design systems understanding", "ai product management", "legal & compliance awareness",
            "customer support & feedback loops", "search engine optimization", "mobile product management",
            "okr goal setting", "negotiation & conflict resolution", "release management & feature flagging"
        ],
        "skill_synonyms": {
            "product strategy & vision": ["product vision", "product roadmap", "strategic planning", "product strategy"],
            "user research & customer discovery": ["user interviews", "customer discovery", "user surveys", "persona creation"],
            "product lifecycle management": ["plm", "product lifecycle", "feature rollout"],
            "agile & scrum methodologies": ["scrum", "agile", "sprint planning", "backlog grooming", "user stories"],
            "prd writing": ["prd", "product requirements document", "specifications", "functional specs"],
            "prioritization frameworks": ["rice framework", "moscow", "kano model", "value vs effort"],
            "product analytics & kpis": ["dau/mau", "retention rate", "churn rate", "nps", "conversion rate"],
            "a/b testing & experimentation": ["a/b testing", "split testing", "hypothesis testing"],
            "cross-functional leadership": ["stakeholder alignment", "leading without authority", "team leadership"],
            "wireframing & prototyping basics": ["figma", "balsamiq", "miro", "wireframes"],
            "data analysis": ["sql", "excel", "dashboard analysis"],
            "competitive & market analysis": ["competitive analysis", "swot", "tam sam som", "market research"],
            "go-to-market strategy": ["gtm", "product launch", "market entry"],
            "stakeholder management & communication": ["executive presentations", "stakeholder communication"],
            "product discovery": ["design sprints", "lean startup", "mvp definition"],
            "customer journey mapping": ["user journey", "customer journey", "touchpoints"],
            "analytics tools": ["mixpanel", "amplitude", "google analytics", "posthog"],
            "jira / confluence administration": ["jira", "confluence", "atlassian"],
            "technical literacy": ["api understanding", "system architecture literacy"],
            "pricing & monetization strategy": ["monetization", "saas pricing", "freemium"],
            "product-led growth": ["plg", "viral loops", "onboarding optimization"],
            "financial modeling & unit economics": ["cac", "ltv", "payback period"],
            "ux / design systems understanding": ["ux design", "design systems"],
            "ai product management": ["ai product strategy", "llm product management"],
            "legal & compliance awareness": ["gdpr", "ccpa", "compliance"],
            "customer support & feedback loops": ["zendesk", "productboard", "feedback loops"],
            "search engine optimization": ["seo basics"],
            "mobile product management": ["app store optimization", "aso"],
            "okr goal setting": ["okrs", "objectives and key results"],
            "negotiation & conflict resolution": ["negotiation"],
            "release management & feature flagging": ["feature flags", "launchdarkly"]
        },
        "tools": ["Jira", "Confluence", "Figma", "Amplitude", "Mixpanel", "Miro", "Notion"],
        "certifications": [
            "Certified Scrum Product Owner (CSPO)",
            "Pragmatic Institute Certified (PMC)",
            "Product School Certified Product Manager"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Writing crisp user stories and PRDs, running user discovery interviews, tracking feature KPIs, and facilitating sprint ceremonies with engineering.",
                "expected_skills": ["agile & scrum methodologies", "prd writing", "user research & customer discovery", "product analytics & kpis", "data analysis"],
                "projects": ["End-to-End PRD for New Mobile Onboarding Flow", "User Research Study & Customer Journey Map for E-Commerce", "Feature Prioritization Matrix using RICE"]
            },
            "mid": {
                "focus": "Owning complete product pods, roadmap strategy, A/B testing experimentation engines, GTM execution, and product-led growth (PLG) optimization.",
                "expected_skills": ["product strategy & vision", "a/b testing & experimentation", "go-to-market strategy", "prioritization frameworks", "analytics tools"],
                "projects": ["Self-Serve SaaS Checkout & Monetization Redesign", "A/B Experimentation Engine for Search Recommendation", "Zero-to-One B2B Analytics Feature Launch"]
            },
            "senior": {
                "focus": "Multi-product portfolio roadmap, P&L ownership, company-wide OKR calibration, executive stakeholder alignment, and coaching associate PMs.",
                "expected_skills": ["cross-functional leadership", "pricing & monetization strategy", "product-led growth", "financial modeling & unit economics", "okr goal setting"],
                "projects": ["Multi-Year Enterprise Platform Modernization Strategy", "Pricing Tier Restructuring Driving +24% ARR", "AI Copilot Integration Product Strategy"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "Product Foundations & Discovery",
                "skills": ["product discovery", "user research & customer discovery", "customer journey mapping"],
                "description": "Customer problem definition, user interviews, journey mapping, empathy maps, and lean MVP validation.",
                "resources": [
                    {"title": "Product School Free Resources & Books", "url": "https://productschool.com/resources", "type": "free_doc"},
                    {"title": "Mind the Product Articles", "url": "https://www.mindtheproduct.com", "type": "free_doc"}
                ]
            },
            {
                "step": 2,
                "topic": "Execution, Agile & PRD Writing",
                "skills": ["agile & scrum methodologies", "prd writing", "prioritization frameworks"],
                "description": "Writing user stories, acceptance criteria, authoring comprehensive PRDs, sprint planning, and RICE scoring.",
                "resources": [
                    {"title": "Atlassian Agile Coach & Scrum Guide", "url": "https://www.atlassian.com/agile", "type": "free_doc"},
                    {"title": "Lenny's Newsletter Free PM Templates", "url": "https://www.lennysnewsletter.com", "type": "free_doc"}
                ]
            },
            {
                "step": 3,
                "topic": "Product Analytics & Experimentation",
                "skills": ["product analytics & kpis", "a/b testing & experimentation", "data analysis"],
                "description": "Tracking retention, cohort analysis, conversion funnels, hypothesis testing, and setting up Amplitude/Mixpanel.",
                "resources": [
                    {"title": "Amplitude Product Analytics Playbook", "url": "https://amplitude.com/resources", "type": "free_doc"},
                    {"title": "Mixpanel Guide to Product Metrics", "url": "https://mixpanel.com/topics/", "type": "free_doc"}
                ]
            },
            {
                "step": 4,
                "topic": "Strategy, Monetization & GTM",
                "skills": ["product strategy & vision", "go-to-market strategy", "competitive & market analysis"],
                "description": "Competitive moats, TAM/SAM/SOM market sizing, SaaS monetization, positioning, and cross-functional launch plans.",
                "resources": [
                    {"title": "Reforge Free Insights & Strategy Essays", "url": "https://www.reforge.com/blog", "type": "free_doc"},
                    {"title": "OpenView Product-Led Growth Guide", "url": "https://openviewpartners.com/product-led-growth/", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://roadmap.sh/product-manager",
            "https://www.mindtheproduct.com"
        ],
        "last_updated": "2026-10-22"
    },
    {
        "role": "UI/UX Designer",
        "slug": "ui-ux-designer",
        "aliases": ["Product Designer", "UX Designer", "UI Designer", "User Experience Specialist", "Interaction Designer"],
        "model_classes": {"Web Designing": 0.75, "Arts": 0.25},
        "action_verbs": ["designed", "prototyped", "researched", "tested", "iterated", "standardized", "crafted", "streamlined", "conceptualized"],
        "role_specific_rules": {
            "portfolio_required": True,
            "min_bullet_points": 4,
            "prefer_live_links": True
        },
        "critical_skills": [
            "figma", "user research & usability testing", "wireframing & low-fidelity prototyping",
            "high-fidelity ui design", "design systems", "information architecture",
            "responsive design", "interaction design", "user persona & empathy mapping",
            "accessibility standards", "design thinking methodology", "heuristic evaluation",
            "customer journey mapping", "developer handoff", "visual storytelling & presentation",
            "grid systems & layout"
        ],
        "bonus_skills": [
            "adobe creative suite", "front-end basics", "motion design", "ux writing & microcopy",
            "quantitative ux metrics", "miro / figjam workshops", "design sprint facilitation",
            "3d design basics", "voice & conversational ui design", "design token management",
            "mobile platform guidelines", "a/b design testing analysis", "product strategy collaboration",
            "service design", "data visualization design"
        ],
        "skill_synonyms": {
            "figma": ["figma auto layout", "figma components", "figma prototypes"],
            "user research & usability testing": ["user research", "usability testing", "moderated testing", "user testing"],
            "wireframing & low-fidelity prototyping": ["wireframing", "wireframes", "low-fi prototyping", "lo-fi"],
            "high-fidelity ui design": ["high-fi ui", "visual design", "ui design", "mockups"],
            "design systems": ["component library", "ui kit", "style guides", "design tokens"],
            "information architecture": ["ia", "site maps", "card sorting", "navigation structure"],
            "responsive design": ["mobile responsive", "desktop adaptation", "fluid grids"],
            "interaction design": ["ixd", "micro-interactions", "transitions", "prototyping"],
            "user persona & empathy mapping": ["user personas", "personas", "empathy maps"],
            "accessibility standards": ["wcag", "wcag 2.1", "color contrast", "accessible design", "a11y design"],
            "design thinking methodology": ["design thinking", "human-centered design", "hcd"],
            "heuristic evaluation": ["nielsen norman heuristics", "usability audit"],
            "customer journey mapping": ["journey map", "experience map", "touchpoint analysis"],
            "developer handoff": ["specifications", "zeplin", "figma inspect", "asset export"],
            "visual storytelling & presentation": ["design presentation", "case study presentation"],
            "grid systems & layout": ["8pt grid", "grid system", "typography hierarchy"],
            "adobe creative suite": ["adobe illustrator", "photoshop", "adobe xd"],
            "front-end basics": ["html/css understanding", "flexbox basics"],
            "motion design": ["lottie", "after effects", "protopie", "framer"],
            "ux writing & microcopy": ["ux copy", "microcopy", "content design"],
            "quantitative ux metrics": ["sus score", "task completion rate", "ces", "time on task"],
            "miro / figjam workshops": ["figjam", "miro", "collaborative workshops"],
            "design sprint facilitation": ["design sprints", "gv design sprint"],
            "3d design basics": ["spline", "blender"],
            "voice & conversational ui design": ["voice ui", "conversational design"],
            "design token management": ["tokens studio", "design tokens"],
            "mobile platform guidelines": ["material design 3", "apple hig"],
            "a/b design testing analysis": ["multivariate design testing"],
            "product strategy collaboration": ["product discovery design"],
            "service design": ["service blueprints"],
            "data visualization design": ["dashboard ui design"]
        },
        "tools": ["Figma", "FigJam", "Adobe Creative Suite", "ProtoPie", "Maze", "Miro", "Zeplin"],
        "certifications": [
            "Google UX Design Professional Certificate",
            "Nielsen Norman Group UX Master Certified",
            "Interaction Design Foundation UX Specialist"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Conducting user interviews, building wireframes, designing clean UI mockups in Figma with auto-layout, and presenting a portfolio with 2 structured case studies.",
                "expected_skills": ["figma", "wireframing & low-fidelity prototyping", "high-fidelity ui design", "accessibility standards", "grid systems & layout"],
                "projects": ["Mobile Food Delivery App Case Study (Research to High-Fi)", "Accessible SaaS Landing Page Redesign", "Fintech Mobile Wallet Flow in Figma"]
            },
            "mid": {
                "focus": "Complex design systems with design tokens, unmoderated usability testing with Maze, interactive prototyping, micro-interactions, and developer handoff.",
                "expected_skills": ["design systems", "user research & usability testing", "interaction design", "developer handoff", "heuristic evaluation"],
                "projects": ["Cross-Platform Multi-Brand Design System in Figma", "Enterprise Cloud Management Dashboard Overhaul", "Healthcare Patient Portal Usability Study & Redesign"]
            },
            "senior": {
                "focus": "Design strategy driving product metrics, company-wide design operations (DesignOps), design sprint facilitation, brand synthesis, and design mentorship.",
                "expected_skills": ["design thinking methodology", "quantitative ux metrics", "design sprint facilitation", "motion design", "product strategy collaboration"],
                "projects": ["Global E-Commerce Omnichannel Checkout Architecture", "Zero-to-One Autonomous AI Agent Interface System", "Enterprise DesignOps Framework & Token Pipeline"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "UX Foundations & Design Thinking",
                "skills": ["design thinking methodology", "user persona & empathy mapping", "user research & usability testing"],
                "description": "5 stages of design thinking, user interview techniques, affinity mapping, and identifying core pain points.",
                "resources": [
                    {"title": "Nielsen Norman Group UX Articles", "url": "https://www.nngroup.com/articles/", "type": "free_doc"},
                    {"title": "Interaction Design Foundation Open Literature", "url": "https://www.interaction-design.org/literature", "type": "free_doc"}
                ]
            },
            {
                "step": 2,
                "topic": "Information Architecture & Wireframing",
                "skills": ["information architecture", "wireframing & low-fidelity prototyping", "customer journey mapping"],
                "description": "Card sorting, site mapping, low-fidelity wireframing in Figma/FigJam, and task flow diagrams.",
                "resources": [
                    {"title": "Figma Learn: Wireframing & Prototyping", "url": "https://help.figma.com/hc/en-us/categories/360002051613-Get-started", "type": "free_doc"},
                    {"title": "UXPin Information Architecture Guide", "url": "https://www.uxpin.com/studio/blog/information-architecture/", "type": "free_doc"}
                ]
            },
            {
                "step": 3,
                "topic": "Visual UI Design, Color & Typography",
                "skills": ["high-fidelity ui design", "grid systems & layout", "accessibility standards"],
                "description": "Typography scales, 8pt spacing grids, color harmony, visual hierarchy, and WCAG 2.1 AA accessibility guidelines.",
                "resources": [
                    {"title": "Google Material Design 3 Guidelines", "url": "https://m3.material.io", "type": "free_doc"},
                    {"title": "Apple Human Interface Guidelines", "url": "https://developer.apple.com/design/human-interface-guidelines", "type": "free_doc"}
                ]
            },
            {
                "step": 4,
                "topic": "Design Systems & Component Architecture",
                "skills": ["figma", "design systems", "developer handoff"],
                "description": "Figma auto-layout, variants, component properties, design tokens, and preparing pixel-perfect developer specs.",
                "resources": [
                    {"title": "Design Systems Handbook by InVision", "url": "https://www.designbetter.co/design-systems-handbook", "type": "free_doc"},
                    {"title": "Figma Community Design Systems Explorer", "url": "https://help.figma.com/hc/en-us/articles/360039238353-Guide-to-design-systems-in-Figma", "type": "free_interactive"}
                ]
            },
            {
                "step": 5,
                "topic": "Prototyping, Usability Testing & Portfolio",
                "skills": ["interaction design", "user research & usability testing", "visual storytelling & presentation"],
                "description": "Interactive transitions, conducting remote usability tests in Maze, analyzing metrics (SUS), and case study writing.",
                "resources": [
                    {"title": "Maze Usability Testing Guide", "url": "https://maze.co/guides/usability-testing/", "type": "free_doc"},
                    {"title": "Case Study Club - Best UX Case Studies", "url": "https://www.casestudy.club", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://roadmap.sh/ux-design",
            "https://www.nngroup.com/articles/",
            "https://www.onetonline.org/link/summary/15-1255.00",
            "https://m3.material.io"
        ],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Business Analyst",
        "slug": "business-analyst",
        "aliases": ["IT Business Analyst", "Systems Analyst", "Business Systems Analyst", "Functional Consultant"],
        "model_classes": {"Business Analyst": 0.70, "Database": 0.20, "Operations Manager": 0.10},
        "action_verbs": ["elicited", "modeled", "streamlined", "formulated", "facilitated", "analyzed", "documented", "validated", "championed"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": False
        },
        "critical_skills": [
            "requirements gathering & elicitation", "business process modeling", "brd & frd documentation",
            "user stories & acceptance criteria", "sql for business analysis", "data analysis & interpretation",
            "microsoft excel", "stakeholder management & conflict resolution",
            "gap analysis & root cause analysis", "agile & scrum methodologies",
            "use case modeling & uml diagrams", "business case development", "feasibility analysis",
            "process optimization & re-engineering", "change management basics",
            "jira & confluence for requirements tracking"
        ],
        "bonus_skills": [
            "business intelligence tools", "data modeling & er diagrams", "python for business analytics",
            "software testing & uat coordination", "risk management & assessment",
            "six sigma / lean methodologies", "api & integration understanding", "erp / crm systems",
            "financial modeling & forecasting", "decision matrix analysis",
            "compliance & regulatory standards", "customer journey analysis",
            "workshop facilitation techniques", "benchmarking & market research",
            "lucidchart & visio diagramming"
        ],
        "skill_synonyms": {
            "requirements gathering & elicitation": ["requirements elicitation", "stakeholder interviews", "requirements gathering"],
            "business process modeling": ["bpmn", "bpmn 2.0", "process mapping", "workflow design", "as-is to-be"],
            "brd & frd documentation": ["brd", "frd", "functional requirements", "business requirements document"],
            "user stories & acceptance criteria": ["user stories", "acceptance criteria", "invest criteria", "definition of done"],
            "sql for business analysis": ["sql", "sql queries", "data extraction", "joins", "aggregations"],
            "data analysis & interpretation": ["data analysis", "trend analysis", "variance analysis"],
            "microsoft excel": ["excel", "advanced excel", "pivot tables", "financial formulas"],
            "stakeholder management & conflict resolution": ["stakeholder management", "stakeholder communication"],
            "gap analysis & root cause analysis": ["gap analysis", "root cause analysis", "5 whys", "fishbone diagram"],
            "agile & scrum methodologies": ["scrum", "agile", "sprint refinement", "backlog management"],
            "use case modeling & uml diagrams": ["use cases", "uml", "activity diagrams", "sequence diagrams"],
            "business case development": ["business case", "cost-benefit analysis", "roi calculation"],
            "feasibility analysis": ["feasibility study", "technical feasibility", "operational feasibility"],
            "process optimization & re-engineering": ["bpr", "business process re-engineering", "lean process"],
            "change management basics": ["change management", "user adoption", "training plans"],
            "jira & confluence for requirements tracking": ["jira", "confluence", "requirements traceability matrix", "rtm"],
            "business intelligence tools": ["power bi", "tableau", "bi dashboards"],
            "data modeling & er diagrams": ["er diagrams", "entity relationship diagram"],
            "python for business analytics": ["python", "pandas for analytics"],
            "software testing & uat coordination": ["uat", "user acceptance testing", "uat signoff"],
            "risk management & assessment": ["risk matrix", "risk mitigation"],
            "six sigma / lean methodologies": ["six sigma", "dmaic", "lean"],
            "api & integration understanding": ["apis", "swagger docs", "integration specs"],
            "erp / crm systems": ["salesforce", "sap", "erp"],
            "financial modeling & forecasting": ["financial forecasting", "budget modeling"],
            "decision matrix analysis": ["decision matrix", "pugh matrix"],
            "compliance & regulatory standards": ["sox compliance", "gdpr", "hipaa"],
            "customer journey analysis": ["customer journeys"],
            "workshop facilitation techniques": ["facilitation", "requirements workshops"],
            "benchmarking & market research": ["market benchmarking"],
            "lucidchart & visio diagramming": ["lucidchart", "visio", "diagramming"]
        },
        "tools": ["Jira", "Confluence", "Lucidchart", "Microsoft Excel", "Power BI", "SQL Server", "Miro"],
        "certifications": [
            "IIBA Entry Certificate in Business Analysis (ECBA)",
            "IIBA Certified Business Analysis Professional (CBAP)",
            "PMI Professional in Business Analysis (PMI-PBA)"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Conducting stakeholder interviews, mapping AS-IS/TO-BE processes in BPMN, authoring clear user stories with acceptance criteria, and SQL querying.",
                "expected_skills": ["requirements gathering & elicitation", "business process modeling", "user stories & acceptance criteria", "sql for business analysis", "microsoft excel"],
                "projects": ["Business Requirements Document (BRD) for Banking Loan Origination", "BPMN 2.0 Process Re-Engineering for Order Fulfillment", "SQL Financial Variance & Trend Analysis Report"]
            },
            "mid": {
                "focus": "End-to-end Requirements Traceability Matrix (RTM), coordinating UAT testing and sign-off, cost-benefit ROI modeling, and facilitating cross-functional sprint planning.",
                "expected_skills": ["brd & frd documentation", "gap analysis & root cause analysis", "software testing & uat coordination", "use case modeling & uml diagrams", "jira & confluence for requirements tracking"],
                "projects": ["CRM Integration Business Case & Functional Specification", "Enterprise ERP Migration Gap Analysis & RTM", "Automated Claims Processing System Flowchart & User Acceptance Plan"]
            },
            "senior": {
                "focus": "Enterprise digital transformation strategy, strategic change management, executive risk governance, business architecture alignment, and leading BA practices.",
                "expected_skills": ["business case development", "feasibility analysis", "process optimization & re-engineering", "change management basics", "stakeholder management & conflict resolution"],
                "projects": ["Enterprise-Wide Digital Core Transformation Business Blueprint", "Multi-Million Dollar Cloud Migration Cost-Benefit Matrix", "Merger & Acquisition Operational Systems Harmonization Roadmap"]
            }
        },
        "roadmap": [
            {
                "step": 1,
                "topic": "Business Analysis Foundations & Elicitation",
                "skills": ["requirements gathering & elicitation", "stakeholder management & conflict resolution"],
                "description": "BABOK guide principles, stakeholder discovery techniques (interviews, surveys, focus groups), and conflict resolution.",
                "resources": [
                    {"title": "IIBA Business Analysis Open Standards & Core Concepts", "url": "https://www.iiba.org/standards-and-resources/babok/", "type": "free_doc"},
                    {"title": "Modern Analyst - BA Fundamentals", "url": "https://www.modernanalyst.com", "type": "free_doc"}
                ]
            },
            {
                "step": 2,
                "topic": "Process Modeling & BPMN 2.0",
                "skills": ["business process modeling", "gap analysis & root cause analysis"],
                "description": "BPMN 2.0 notation (pools, lanes, gateways, events), AS-IS vs TO-BE mapping, and root cause analysis (Fishbone, 5 Whys).",
                "resources": [
                    {"title": "BPMN.org Interactive Notation Guide", "url": "https://www.bpmn.org", "type": "free_doc"},
                    {"title": "Lucidchart BPMN Tutorial", "url": "https://camunda.com/bpmn/", "type": "free_doc"}
                ]
            },
            {
                "step": 3,
                "topic": "Requirements Documentation & Agile User Stories",
                "skills": ["brd & frd documentation", "user stories & acceptance criteria", "use case modeling & uml diagrams"],
                "description": "Authoring BRDs, FRDs, UML activity/sequence diagrams, user stories with INVEST criteria, and Gherkin acceptance criteria.",
                "resources": [
                    {"title": "Atlassian User Stories Guide", "url": "https://www.atlassian.com/agile/project-management/user-stories", "type": "free_doc"},
                    {"title": "UML Diagrams Tutorial", "url": "https://www.uml-diagrams.org", "type": "free_doc"}
                ]
            },
            {
                "step": 4,
                "topic": "Data Literacy, SQL & Advanced Excel",
                "skills": ["sql for business analysis", "microsoft excel", "data analysis & interpretation"],
                "description": "SQL SELECT, JOINs, aggregations, reconciling data in Excel with Pivot Tables/VLOOKUP, and business variance analysis.",
                "resources": [
                    {"title": "Mode Analytics SQL for Data Analysis", "url": "https://mode.com/sql-tutorial/", "type": "free_doc"},
                    {"title": "Microsoft Excel Business Modeling", "url": "https://support.microsoft.com/en-us/excel", "type": "free_doc"}
                ]
            },
            {
                "step": 5,
                "topic": "UAT Coordination & Change Management",
                "skills": ["software testing & uat coordination", "change management basics", "business case development"],
                "description": "Requirements Traceability Matrix (RTM), writing test scripts, managing user acceptance testing (UAT), and training plans.",
                "resources": [
                    {"title": "Software Testing Help UAT Guide", "url": "https://www.guru99.com/user-acceptance-testing.html", "type": "free_doc"},
                    {"title": "Prosci Change Management Overview", "url": "https://www.prosci.com/resources/articles", "type": "free_doc"}
                ]
            }
        ],
        "sources": [
            "https://www.onetonline.org/link/summary/13-1111.00",
            "https://www.iiba.org/standards-and-resources/babok/",
            "https://bpmn.org"
        ],
        "last_updated": "2026-10-22"
    },
    # Existing 5 roles updated into the exact same rich JSON schema:
    {
        "role": "AI Engineer",
        "slug": "ai-engineer",
        "aliases": ["Artificial Intelligence Engineer", "LLM Engineer", "GenAI Engineer", "AI/ML Systems Engineer"],
        "model_classes": {"Data Science": 0.65, "Python Developer": 0.35},
        "action_verbs": ["fine-tuned", "architected", "deployed", "optimized", "benchmarked", "accelerated", "implemented", "trained"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": True
        },
        "critical_skills": [
            "python", "pytorch", "transformers", "vector database", "rag",
            "langchain", "docker", "fastapi", "cuda", "model evaluation",
            "mlops", "fine-tuning", "prompt engineering", "embeddings",
            "large language models", "api integration", "git"
        ],
        "bonus_skills": [
            "kubernetes", "tensorrt", "aws", "ci/cd", "triton",
            "scikit-learn", "numpy", "pandas", "lora", "vllm",
            "onnx", "llamaindex", "deep learning", "graph neural networks",
            "ray", "guardrails"
        ],
        "skill_synonyms": {
            "python": ["python 3", "python3", "py"],
            "pytorch": ["torch", "pytorch lightning", "lightning"],
            "transformers": ["hugging face", "huggingface", "transformer models", "bert", "gpt", "roberta"],
            "vector database": ["vector db", "faiss", "pinecone", "chroma", "chromadb", "qdrant", "weaviate", "milvus"],
            "rag": ["retrieval-augmented generation", "hybrid rag", "retrieval augmented generation", "advanced rag"],
            "langchain": ["langsmith", "langgraph", "llamaindex", "semantic kernel"],
            "docker": ["containerization", "containers", "dockerfile", "docker compose"],
            "fastapi": ["rest api", "python backend", "starlette", "uvicorn", "pydantic"],
            "cuda": ["gpu programming", "nvidia cuda", "tensorrt", "triton", "gpu acceleration"],
            "model evaluation": ["evals", "ragas", "benchmarking", "perplexity", "deepeval"],
            "mlops": ["weights & biases", "wandb", "mlflow", "dvc", "neptune.ai", "clearml"],
            "fine-tuning": ["sft", "lora", "qlora", "peft", "rlhf", "dpo", "instruction tuning"],
            "prompt engineering": ["few-shot prompting", "chain of thought", "cot", "system prompts"],
            "embeddings": ["dense embeddings", "text-embedding", "sentence-transformers", "vector embeddings"],
            "large language models": ["llms", "gpt-4", "llama", "mistral", "claude", "foundation models"],
            "api integration": ["openai api", "anthropic api", "rest apis", "restful api"],
            "git": ["github", "gitlab", "version control"],
            "kubernetes": ["k8s", "k8s cluster"],
            "tensorrt": ["tensorrt-llm", "trt"],
            "aws": ["amazon web services", "sagemaker", "bedrock"],
            "ci/cd": ["continuous integration", "github actions"],
            "triton": ["triton inference server"],
            "scikit-learn": ["sklearn", "scikit learn"],
            "numpy": ["numerical python"],
            "pandas": ["dataframes"],
            "lora": ["qlora", "low-rank adaptation"],
            "vllm": ["tgi", "text generation inference", "llm serving"],
            "onnx": ["onnx runtime"],
            "deep learning": ["neural networks", "deep neural networks"],
            "ray": ["ray train", "ray serve", "distributed training"],
            "guardrails": ["nemo guardrails", "guardrails ai", "hallucination detection"]
        },
        "tools": ["PyTorch", "Hugging Face", "Docker", "FastAPI", "Weights & Biases", "Ollama", "VS Code"],
        "certifications": [
            "AWS Certified Machine Learning - Specialty",
            "NVIDIA Certified Associate: Generative AI",
            "DeepLearning.AI LangChain Certification"
        ],
        "level_expectations": {
            "fresher": {
                "focus": "Building RAG pipelines with LangChain/LlamaIndex, vector databases, integrating LLM APIs, and deploying with FastAPI.",
                "expected_skills": ["python", "vector database", "rag", "langchain", "fastapi", "git"],
                "projects": ["RAG Q&A System over Company PDFs with FAISS", "Multi-Agent Research Assistant using LangGraph", "Fine-Tuned Sentiment Classifier with Hugging Face"]
            },
            "mid": {
                "focus": "Fine-tuning open weights (LoRA/QLoRA), high-throughput inference serving with vLLM/Triton, automated evaluation pipelines (Ragas), and Docker deployment.",
                "expected_skills": ["pytorch", "transformers", "fine-tuning", "docker", "model evaluation", "mlops"],
                "projects": ["Production vLLM Inference Microservice on AWS", "Domain Adaptation LoRA Fine-Tuning on Mistral 7B", "Hybrid RAG Engine with Cross-Encoder Re-Ranking"]
            },
            "senior": {
                "focus": "Distributed model training (DeepSpeed), TensorRT-LLM quantization, LLM safety guardrails, low-latency streaming architecture, and AI governance.",
                "expected_skills": ["cuda", "kubernetes", "tensorrt", "large language models"],
                "projects": ["Enterprise Multi-Tenant GenAI Gateway with Caching & Rate Limiting", "TensorRT-LLM Quantized Real-Time Copilot Engine", "Autonomous Multi-Agent Workflow Engine"]
            }
        },
        "roadmap": [
            {"step": 1, "topic": "Python & Deep Learning Foundations", "skills": ["python", "pytorch"], "description": "Python, Tensors, PyTorch autograd, and neural network basics.", "resources": [{"title": "PyTorch Official Tutorials", "url": "https://pytorch.org/tutorials/", "type": "free_doc"}]},
            {"step": 2, "topic": "Transformers & Hugging Face", "skills": ["transformers", "embeddings"], "description": "Attention mechanisms, BERT, GPT, and tokenization pipelines.", "resources": [{"title": "Hugging Face NLP Course", "url": "https://huggingface.co/learn/nlp-course", "type": "free_course"}]},
            {"step": 3, "topic": "RAG & Vector Databases", "skills": ["rag", "vector database", "langchain"], "description": "Chunking strategies, dense embeddings, vector indexing, and LangChain/LlamaIndex.", "resources": [{"title": "Pinecone Learning Center", "url": "https://www.pinecone.io/learn/", "type": "free_doc"}]},
            {"step": 4, "topic": "Fine-Tuning & Quantization", "skills": ["fine-tuning", "model evaluation"], "description": "LoRA, QLoRA, PEFT, quantization, and evaluation benchmarks.", "resources": [{"title": "Hugging Face PEFT Documentation", "url": "https://huggingface.co/docs/peft/index", "type": "free_doc"}]},
            {"step": 5, "topic": "Production Deployment & Serving", "skills": ["fastapi", "docker", "mlops"], "description": "FastAPI endpoints, vLLM/Triton serving, Dockerization, and latency profiling.", "resources": [{"title": "vLLM Documentation", "url": "https://github.com/vllm-project/vllm", "type": "free_doc"}]}
        ],
        "sources": ["https://roadmap.sh/ai-data-scientist", "https://huggingface.co", "https://www.onetonline.org/link/summary/15-2051.00"],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Full Stack Developer",
        "slug": "full-stack-developer",
        "aliases": ["Full Stack Engineer", "Web Developer", "Full-Stack Software Engineer"],
        "model_classes": {"Web Designing": 0.50, "Python Developer": 0.25, "Java Developer": 0.25},
        "action_verbs": ["built", "scaled", "designed", "integrated", "refactored", "shipped", "developed", "engineered"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": True
        },
        "critical_skills": [
            "typescript", "react", "node.js", "next.js", "postgresql",
            "tailwind css", "rest api", "graphql", "docker", "git",
            "html5", "css3", "javascript", "state management", "database modeling",
            "api authentication"
        ],
        "bonus_skills": [
            "redis", "aws", "jest", "ci/cd", "microservices", "mongodb",
            "websockets", "prisma", "trpc", "playwright", "serverless",
            "stripe integration", "linux", "vitest", "electron", "kafka"
        ],
        "skill_synonyms": {
            "typescript": ["ts"],
            "react": ["react.js", "reactjs", "react 18", "react 19"],
            "node.js": ["nodejs", "node", "express", "express.js", "fastify", "nest.js"],
            "next.js": ["nextjs", "next.js 14", "next.js 13", "app router"],
            "postgresql": ["postgres", "sql", "psql", "relational database"],
            "tailwind css": ["tailwind", "tailwindcss"],
            "rest api": ["restful api", "restful apis", "rest endpoints", "json api"],
            "graphql": ["apollo server", "apollo client", "relay"],
            "docker": ["containers", "containerization", "docker-compose"],
            "git": ["github", "gitlab", "version control"],
            "html5": ["html", "semantic html"],
            "css3": ["css", "modern css", "flexbox", "css grid"],
            "javascript": ["js", "es6", "es6+", "ecmascript", "vanilla js"],
            "state management": ["redux", "redux toolkit", "zustand", "context api"],
            "database modeling": ["data modeling", "erd", "schema design"],
            "api authentication": ["jwt", "oauth", "oauth2", "next-auth", "clerk"],
            "redis": ["caching", "in-memory cache", "key-value store"],
            "aws": ["amazon web services", "cloud services"],
            "jest": ["unit testing", "vitest", "testing library"],
            "ci/cd": ["continuous integration", "continuous deployment", "github actions"],
            "microservices": ["microservice architecture", "distributed services"],
            "mongodb": ["mongo", "nosql", "document database"],
            "websockets": ["socket.io", "web sockets", "real-time communication"],
            "prisma": ["prisma orm", "orm", "drizzle"],
            "trpc": ["end-to-end typesafe apis"],
            "playwright": ["e2e testing", "cypress", "end-to-end testing"],
            "serverless": ["aws lambda", "serverless functions"],
            "stripe integration": ["stripe", "payment processing"],
            "linux": ["ubuntu", "bash"]
        },
        "tools": ["VS Code", "Postman", "Docker", "Chrome DevTools", "GitHub", "Vercel"],
        "certifications": ["Meta Full-Stack Developer Professional Certificate", "AWS Certified Developer - Associate"],
        "level_expectations": {
            "fresher": {"focus": "Full stack CRUD apps with React, Node/Express, PostgreSQL, and Git.", "expected_skills": ["javascript", "react", "node.js", "postgresql", "html5", "css3"], "projects": ["Full-Stack Task Management App", "E-Commerce Storefront"]},
            "mid": {"focus": "Next.js App Router, TypeScript end-to-end, Prisma ORM, Redis caching, Docker, and CI/CD.", "expected_skills": ["typescript", "next.js", "docker", "redis", "tailwind css", "jest"], "projects": ["SaaS Platform with Stripe Payments", "Real-Time Collaboration Workspace"]},
            "senior": {"focus": "System architecture, micro-frontends, high-throughput microservices, database scaling, and security hardening.", "expected_skills": ["microservices", "aws", "graphql", "ci/cd"], "projects": ["Enterprise Multi-Tenant Cloud Application", "High-Volume Real-Time Streaming Platform"]}
        },
        "roadmap": [
            {"step": 1, "topic": "Frontend Core & TypeScript", "skills": ["react", "typescript", "tailwind css"], "description": "React components, TypeScript typing, and Tailwind styling.", "resources": [{"title": "React.dev", "url": "https://react.dev", "type": "free_doc"}]},
            {"step": 2, "topic": "Backend APIs & Databases", "skills": ["node.js", "postgresql", "rest api"], "description": "Express/Fastify, SQL schema design, PostgreSQL queries, and JWT auth.", "resources": [{"title": "The Odin Project (Node Path)", "url": "https://www.theodinproject.com", "type": "free_course"}]},
            {"step": 3, "topic": "Full-Stack Meta-Frameworks", "skills": ["next.js"], "description": "Next.js App Router, Server Actions, SSR, and API routes.", "resources": [{"title": "Next.js Learn", "url": "https://nextjs.org/learn", "type": "free_course"}]},
            {"step": 4, "topic": "Caching, Containers & Deployment", "skills": ["docker", "redis", "ci/cd"], "description": "Dockerizing apps, Redis caching, and automated deployment.", "resources": [{"title": "Docker Official Docs", "url": "https://docs.docker.com", "type": "free_doc"}]}
        ],
        "sources": ["https://roadmap.sh/full-stack", "https://www.onetonline.org/link/summary/15-1254.00"],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Cloud & DevOps Engineer",
        "slug": "cloud-devops-engineer",
        "aliases": ["DevOps Engineer", "Cloud Engineer", "Infrastructure Engineer"],
        "model_classes": {"DevOps Engineer": 0.60, "Network Security Engineer": 0.20, "Database": 0.20},
        "action_verbs": ["automated", "orchestrated", "provisioned", "migrated", "hardened", "monitored", "deployed", "configured"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": False
        },
        "critical_skills": [
            "kubernetes", "docker", "terraform", "aws", "ci/cd",
            "linux", "prometheus", "grafana", "python", "bash",
            "git", "networking protocols", "helm", "cloud security",
            "infrastructure as code"
        ],
        "bonus_skills": [
            "argo cd", "istio", "ansible", "gcp", "azure",
            "cloudformation", "jenkins", "vault", "elk", "finops",
            "cilium", "sonarqube", "open policy agent", "packer", "traefik"
        ],
        "skill_synonyms": {
            "kubernetes": ["k8s", "kubernetes cluster", "kubectl", "eks", "gke", "aks"],
            "docker": ["containers", "containerization", "dockerfile", "docker compose"],
            "terraform": ["iac", "opentofu", "hashicorp terraform"],
            "aws": ["amazon web services", "cloud computing", "ec2", "s3", "iam"],
            "ci/cd": ["continuous integration", "continuous delivery", "github actions", "gitlab ci", "jenkins"],
            "linux": ["bash", "shell scripting", "rhel", "ubuntu", "systemd"],
            "prometheus": ["metrics collection", "promql", "alertmanager"],
            "grafana": ["dashboards", "monitoring dashboards"],
            "python": ["python3", "automation scripts"],
            "bash": ["shell scripting", "sh", "zsh", "cli scripting"],
            "git": ["github", "gitlab", "version control"],
            "networking protocols": ["tcp/ip", "dns", "http/https", "ssl/tls", "load balancing"],
            "helm": ["helm charts", "k8s package manager"],
            "cloud security": ["iam policies", "least privilege", "soc2", "zero trust"],
            "infrastructure as code": ["iac", "declarative configuration"],
            "argo cd": ["argocd", "gitops", "fluxcd"],
            "istio": ["service mesh", "envoy"],
            "ansible": ["configuration management", "playbooks"],
            "gcp": ["google cloud platform", "google cloud"],
            "azure": ["microsoft azure", "azure cloud"],
            "cloudformation": ["aws cfn", "cdk", "aws cdk"],
            "jenkins": ["jenkins pipelines", "ci server"],
            "vault": ["hashicorp vault", "secrets management"],
            "elk": ["elasticsearch", "logstash", "kibana", "elastic stack"],
            "finops": ["cloud cost optimization", "cost allocation"],
            "cilium": ["ebpf", "kubernetes cni"],
            "sonarqube": ["static code analysis", "sast"]
        },
        "tools": ["Kubernetes", "Docker", "Terraform", "AWS", "Prometheus", "Grafana", "GitHub Actions"],
        "certifications": ["Certified Kubernetes Administrator (CKA)", "AWS Certified DevOps Engineer - Professional"],
        "level_expectations": {
            "fresher": {"focus": "Linux administration, Bash automation, Dockerfiles, and setting up simple CI/CD in GitHub Actions.", "expected_skills": ["linux", "bash", "docker", "git", "ci/cd"], "projects": ["Automated CI/CD Pipeline for Web App", "Dockerized Multi-Container Application"]},
            "mid": {"focus": "Kubernetes administration, Terraform provisioning on AWS/GCP, Prometheus/Grafana monitoring, and GitOps with ArgoCD.", "expected_skills": ["kubernetes", "terraform", "aws", "prometheus", "grafana"], "projects": ["Terraform-Provisioned Kubernetes Cluster on AWS", "GitOps Deployment Pipeline with ArgoCD"]},
            "senior": {"focus": "Enterprise cloud security, multi-region architecture, service mesh (Istio), FinOps optimization, and disaster recovery.", "expected_skills": ["istio", "vault", "finops", "cloud security"], "projects": ["Enterprise Multi-Account Cloud Migration", "Zero-Trust Service Mesh Architecture"]}
        },
        "roadmap": [
            {"step": 1, "topic": "Linux & Bash Automation", "skills": ["linux", "bash"], "description": "Linux command line, networking, and shell scripting.", "resources": [{"title": "Linux Journey", "url": "https://linuxjourney.com", "type": "free_interactive"}]},
            {"step": 2, "topic": "Containers & CI/CD", "skills": ["docker", "ci/cd"], "description": "Docker containerization and automated GitHub Actions pipelines.", "resources": [{"title": "Docker Documentation", "url": "https://docs.docker.com", "type": "free_doc"}]},
            {"step": 3, "topic": "Cloud & Infrastructure as Code", "skills": ["aws", "terraform"], "description": "AWS core infrastructure and Terraform IaC.", "resources": [{"title": "Terraform Tutorials", "url": "https://developer.hashicorp.com/terraform/tutorials", "type": "free_doc"}]},
            {"step": 4, "topic": "Kubernetes & Monitoring", "skills": ["kubernetes", "prometheus", "grafana"], "description": "Kubernetes cluster administration and observability with Prometheus.", "resources": [{"title": "Kubernetes Documentation", "url": "https://kubernetes.io/docs/", "type": "free_doc"}]}
        ],
        "sources": ["https://roadmap.sh/devops"],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Data Engineer",
        "slug": "data-engineer",
        "aliases": ["Big Data Engineer", "Data Pipeline Engineer", "Data Infrastructure Engineer"],
        "model_classes": {"Database": 0.55, "Data Science": 0.30, "Python Developer": 0.15},
        "action_verbs": ["architected", "orchestrated", "streamed", "transformed", "optimized", "pipelined", "ingested", "scaled"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": False
        },
        "critical_skills": [
            "python", "sql", "spark", "kafka", "airflow",
            "snowflake", "data modeling", "etl", "docker", "dbt",
            "data warehousing", "git", "linux", "database indexing", "distributed computing"
        ],
        "bonus_skills": [
            "aws", "bigquery", "flink", "hadoop", "postgresql",
            "scala", "databricks", "delta lake", "presto", "iceberg",
            "clickhouse", "apache beam", "trino", "hive", "redshift"
        ],
        "skill_synonyms": {
            "python": ["python3", "py"],
            "sql": ["advanced sql", "ansi sql", "stored procedures", "window functions"],
            "spark": ["pyspark", "apache spark", "spark sql", "spark streaming"],
            "kafka": ["apache kafka", "kafka streams", "event streaming"],
            "airflow": ["apache airflow", "airflow dags", "prefect", "dagster"],
            "snowflake": ["snowflake data warehouse", "snowpipe"],
            "data modeling": ["dimensional modeling", "star schema", "snowflake schema", "3nf"],
            "etl": ["elt", "data pipeline", "batch processing", "data ingestion"],
            "docker": ["containers", "containerization"],
            "dbt": ["data build tool", "dbt core", "dbt cloud"],
            "data warehousing": ["edw", "data warehouse", "lakehouse", "data lake"],
            "git": ["github", "gitlab", "version control"],
            "linux": ["bash", "shell scripting"],
            "database indexing": ["query optimization", "partitioning", "clustering"],
            "distributed computing": ["mapreduce", "distributed systems", "cluster computing"],
            "aws": ["amazon web services", "s3", "emr", "glue", "redshift"],
            "bigquery": ["google bigquery", "bq"],
            "flink": ["apache flink", "stream processing"],
            "hadoop": ["hdfs", "yarn", "hive"],
            "postgresql": ["postgres", "rdbms"],
            "scala": ["scala programming"],
            "databricks": ["databricks lakehouse", "delta lake", "unity catalog"],
            "delta lake": ["delta tables", "acid transactions"],
            "iceberg": ["apache iceberg", "table format"],
            "clickhouse": ["columnar database", "olap"],
            "apache beam": ["beam pipelines", "google dataflow"]
        },
        "tools": ["Apache Spark", "Airflow", "Kafka", "Snowflake", "dbt", "Docker", "PostgreSQL"],
        "certifications": ["Databricks Certified Data Engineer Associate", "AWS Certified Data Analytics - Specialty"],
        "level_expectations": {
            "fresher": {"focus": "SQL transformations, writing automated Python ETL scripts, and building dimensional schemas.", "expected_skills": ["python", "sql", "etl", "data modeling"], "projects": ["Automated Data Ingestion Pipeline with PostgreSQL", "Dimensional Data Warehouse in SQLite"]},
            "mid": {"focus": "Distributed data processing with PySpark, orchestrating DAGs in Airflow, dbt modeling, and Snowflake data warehouses.", "expected_skills": ["spark", "airflow", "snowflake", "dbt", "docker"], "projects": ["End-to-End Batch Lakehouse Pipeline with Airflow & Spark", "Real-Time Log Stream Processing with Kafka"]},
            "senior": {"focus": "Real-time stream processing with Kafka and Flink, Lakehouse table formats (Delta/Iceberg), data mesh governance, and petabyte-scale tuning.", "expected_skills": ["kafka", "flink", "bigquery", "data warehousing"], "projects": ["Petabyte-Scale Real-Time Streaming Analytics Architecture", "Automated Enterprise Data Quality & Lineage Platform"]}
        },
        "roadmap": [
            {"step": 1, "topic": "SQL & Data Modeling", "skills": ["sql", "data modeling"], "description": "Advanced SQL, dimensional modeling, and database indexing.", "resources": [{"title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "free_doc"}]},
            {"step": 2, "topic": "Python & Data Warehousing", "skills": ["python", "snowflake", "dbt"], "description": "Python data processing, cloud data warehouses, and dbt modeling.", "resources": [{"title": "dbt Learn", "url": "https://courses.getdbt.com", "type": "free_course"}]},
            {"step": 3, "topic": "Orchestration with Airflow", "skills": ["airflow", "etl"], "description": "Writing robust DAGs, sensors, and task dependencies.", "resources": [{"title": "Apache Airflow Documentation", "url": "https://airflow.apache.org/docs/", "type": "free_doc"}]},
            {"step": 4, "topic": "Distributed Processing & Streaming", "skills": ["spark", "kafka"], "description": "PySpark distributed computation and Kafka event streaming.", "resources": [{"title": "Spark Official Documentation", "url": "https://spark.apache.org/docs/latest/", "type": "free_doc"}]}
        ],
        "sources": ["https://roadmap.sh/data-engineer", "https://www.onetonline.org/link/summary/15-1243.00"],
        "last_updated": "2026-10-22"
    },
    {
        "role": "Cybersecurity Analyst",
        "slug": "cybersecurity-analyst",
        "aliases": ["Information Security Analyst", "SOC Analyst", "Security Engineer", "Cyber Threat Analyst"],
        "model_classes": {"Network Security Engineer": 0.70, "DevOps Engineer": 0.20, "Database": 0.10},
        "action_verbs": ["mitigated", "triaged", "investigated", "hardened", "audited", "defended", "neutralized", "patched"],
        "role_specific_rules": {
            "portfolio_required": False,
            "min_bullet_points": 4,
            "prefer_live_links": False
        },
        "critical_skills": [
            "network security", "threat intelligence", "soc", "siem", "vulnerability assessment",
            "wireshark", "penetration testing", "incident response", "linux", "firewall",
            "cryptography", "iam", "cloud security", "mitre att&ck", "endpoint security"
        ],
        "bonus_skills": [
            "owasp", "burp suite", "python", "edr", "splunk",
            "metasploit", "snort", "suricata", "reverse engineering",
            "malware analysis", "zero trust", "trivy", "zeek", "ossec", "yara"
        ],
        "skill_synonyms": {
            "network security": ["network defense", "tcp/ip security", "ids/ips", "network segmentation"],
            "threat intelligence": ["cti", "cyber threat intelligence", "threat hunting", "ioc"],
            "soc": ["security operations center", "soc operations", "tier 1 soc"],
            "siem": ["splunk", "qradar", "microsoft sentinel", "sentinel", "log analysis", "wazuh"],
            "vulnerability assessment": ["vulnerability scanning", "nessus", "qualys", "cve analysis"],
            "wireshark": ["packet analysis", "pcap", "tcpdump", "traffic analysis"],
            "penetration testing": ["pentesting", "ethical hacking", "red teaming", "offensive security"],
            "incident response": ["ir", "dfir", "digital forensics", "containment"],
            "linux": ["kali linux", "linux cli", "bash"],
            "firewall": ["next-gen firewall", "ngfw", "palo alto", "fortinet"],
            "cryptography": ["encryption", "pki", "tls/ssl", "hashing"],
            "iam": ["identity and access management", "active directory", "okta", "rbac"],
            "cloud security": ["aws security", "cspm", "azure security"],
            "mitre att&ck": ["att&ck framework", "tactic technique procedure", "ttp"],
            "endpoint security": ["edr", "crowdstrike", "sentinelone", "xdr"],
            "owasp": ["owasp top 10", "web application security", "appsec"],
            "burp suite": ["burp", "web proxy", "burpsuite pro"],
            "python": ["security automation", "python scripting"],
            "zero trust": ["zero trust architecture", "zta"],
            "malware analysis": ["reverse engineering", "sandbox analysis"],
            "splunk": ["splunk es", "splunk spl"],
            "snort": ["ids rules", "suricata rules"],
            "trivy": ["container security scanning"],
            "yara": ["yara rules", "malware signatures"],
            "ossec": ["hids", "host intrusion detection"]
        },
        "tools": ["Wireshark", "Splunk", "Burp Suite", "Nmap", "Metasploit", "Kali Linux", "Snort"],
        "certifications": ["CompTIA Security+", "Certified Ethical Hacker (CEH)", "GIAC Security Essentials (GSEC)"],
        "level_expectations": {
            "fresher": {"focus": "Log analysis in SIEM (Splunk), packet inspection in Wireshark, identifying common CVE vulnerabilities, and network defense basics.", "expected_skills": ["network security", "wireshark", "linux", "siem", "firewall"], "projects": ["SOC Lab with Wireshark & Suricata IDS", "Vulnerability Assessment Report of Virtual Lab"]},
            "mid": {"focus": "Incident response triage, threat hunting using MITRE ATT&CK, automated vulnerability scanning with Nessus, and web application pentesting with Burp Suite.", "expected_skills": ["incident response", "mitre att&ck", "penetration testing", "vulnerability assessment", "iam"], "projects": ["End-to-End Web App Security Audit against OWASP Top 10", "Automated Threat Hunting Script in Python"]},
            "senior": {"focus": "Enterprise zero-trust architecture, cloud security posture management (CSPM), malware analysis, compliance auditing, and security orchestration (SOAR).", "expected_skills": ["cloud security", "cryptography", "threat intelligence", "zero trust"], "projects": ["Enterprise SOAR Automated Incident Containment Pipeline", "Zero-Trust Architecture Transition Strategy"]}
        },
        "roadmap": [
            {"step": 1, "topic": "Networking & Security Fundamentals", "skills": ["network security", "wireshark", "linux"], "description": "TCP/IP layers, packet capture with Wireshark, and Linux system security.", "resources": [{"title": "Cybrary Free Security Courses", "url": "https://www.cybrary.it", "type": "free_course"}]},
            {"step": 2, "topic": "Threat Detection & SIEM", "skills": ["siem", "soc", "mitre att&ck"], "description": "SIEM configuration, Splunk search syntax, alert triaging, and MITRE ATT&CK.", "resources": [{"title": "Splunk Free Training", "url": "https://www.splunk.com/en_us/training/free-courses/overview.html", "type": "free_course"}]},
            {"step": 3, "topic": "Vulnerability Assessment & Pentesting", "skills": ["vulnerability assessment", "penetration testing"], "description": "OWASP Top 10, scanning with Nmap/Nessus, and web testing with Burp Suite.", "resources": [{"title": "PortSwigger Web Security Academy", "url": "https://portswigger.net/web-security", "type": "free_interactive"}]},
            {"step": 4, "topic": "Cloud Security & Incident Response", "skills": ["cloud security", "incident response", "iam"], "description": "IAM policies, cloud threat modeling, and containment workflows.", "resources": [{"title": "CISA Incident Response Resources", "url": "https://www.cisa.gov", "type": "free_doc"}]}
        ],
        "sources": ["https://roadmap.sh/cyber-security", "https://www.onetonline.org/link/summary/15-1212.00"],
        "last_updated": "2026-10-22"
    }
]

ONET_METADATA = {
    "Frontend Developer": {"code": "15-1254.00", "title": "Web Developers", "status": "reference_only", "match_type": "exact_match", "notes": "Exact match: Official SOC classification for web and frontend developers."},
    "Backend Developer": {"code": "15-1252.00", "title": "Software Developers", "status": "reference_only", "match_type": "exact_match", "notes": "Exact match: Official SOC classification for software developers building applications and services."},
    "Data Analyst": {"code": "15-2051.01", "title": "Business Intelligence Analysts", "status": "reference_only", "match_type": "exact_match", "notes": "Exact match: Official SOC classification for BI analysts and data analysts."},
    "Data Scientist/ML Engineer": {"code": "15-2051.00", "title": "Data Scientists", "status": "reference_only", "match_type": "exact_match", "notes": "Exact match: Official SOC classification for data scientists and ML modeling specialists."},
    "Mobile App Developer": {"code": "15-1252.00", "title": "Software Developers", "status": "reference_only", "match_type": "exact_match", "notes": "Exact match: Official SOC classification covering mobile application developers."},
    "QA/Test Automation Engineer": {"code": "15-1253.00", "title": "Software Quality Assurance Analysts and Testers", "status": "reference_only", "match_type": "exact_match", "notes": "Exact match: Official SOC classification for software QA and test automation engineers."},
    "Software Engineer (generic)": {"code": "15-1252.00", "title": "Software Developers", "status": "reference_only", "match_type": "exact_match", "notes": "Exact match: Official SOC classification for core software developers."},
    "SRE": {"code": None, "title": None, "status": "reference_only", "match_type": "no_direct_match", "notes": "No direct match: O*NET code 15-1244.00 is Network/Systems Administrators; Site Reliability Engineering is a software discipline and lacks an individual SOC code."},
    "Product Manager": {"code": None, "title": None, "status": "reference_only", "match_type": "no_direct_match", "notes": "No direct match: O*NET code 11-2021.00 is Marketing Managers, which is inaccurate for software product management. Tech PM lacks an official O*NET SOC code."},
    "UI/UX Designer": {"code": "15-1255.00", "title": "Web and Digital Interface Designers", "status": "reference_only", "match_type": "exact_match", "notes": "Exact match: Official SOC classification for UI, UX, and digital interface designers."},
    "Business Analyst": {"code": "13-1111.00", "title": "Management Analysts", "status": "reference_only", "match_type": "loose_match", "notes": "Loose match: Mapped to Management Analysts (13-1111.00); encompasses IT Business Analysts, BPMN process specialists, and requirements analysts."},
    "AI Engineer": {"code": "15-2051.00", "title": "Data Scientists", "status": "reference_only", "match_type": "loose_match", "notes": "Loose match: Mapped to Data Scientists (15-2051.00); modern LLM/GenAI systems engineering is an emerging field not yet separately distinguished in SOC taxonomy."},
    "Full Stack Developer": {"code": "15-1254.00", "title": "Web Developers", "status": "reference_only", "match_type": "exact_match", "notes": "Exact match: Official SOC classification for web and full stack developers."},
    "Cloud & DevOps Engineer": {"code": None, "title": None, "status": "reference_only", "match_type": "no_direct_match", "notes": "No direct match: Cloud infrastructure and DevOps automation currently lack a distinct standalone SOC code in O*NET."},
    "Data Engineer": {"code": "15-1243.00", "title": "Database Architects", "status": "reference_only", "match_type": "loose_match", "notes": "Loose match: Mapped to Database Architects (15-1243.00) as modern cloud data engineering and streaming pipelines lack an independent O*NET SOC code."},
    "Cybersecurity Analyst": {"code": "15-1212.00", "title": "Information Security Analysts", "status": "reference_only", "match_type": "exact_match", "notes": "Exact match: Official SOC classification for information security and cybersecurity analysts."}
}

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(script_dir)
    roles_dir = os.path.join(backend_dir, "data", "roles")
    os.makedirs(roles_dir, exist_ok=True)

    print(f"Generating authoritative role benchmark files in: {roles_dir}")
    print("=" * 80)

    summary = []
    for role_item in ROLES_DATA:
        role_name = role_item["role"]
        if role_name in ONET_METADATA:
            role_item["onet"] = ONET_METADATA[role_name]
        filename = f"{role_item['slug']}.json"
        filepath = os.path.join(roles_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(role_item, f, indent=2)

        crit_count = len(role_item["critical_skills"])
        bonus_count = len(role_item["bonus_skills"])
        synonym_count = len(role_item.get("skill_synonyms", {}))
        roadmap_steps = len(role_item.get("roadmap", []))

        summary.append({
            "Role": role_item["role"],
            "Slug": role_item["slug"],
            "Critical Skills": crit_count,
            "Bonus Skills": bonus_count,
            "Synonyms": synonym_count,
            "Roadmap Steps": roadmap_steps,
            "Portfolio Required": role_item.get("role_specific_rules", {}).get("portfolio_required", False),
            "Sources": role_item.get("sources", [])
        })
        print(f"[OK] Created {filename:35s} | Critical: {crit_count:2d} | Bonus: {bonus_count:2d} | Roadmap: {roadmap_steps} steps")

    print("=" * 80)
    print(f"Successfully generated {len(summary)} versioned role definitions.")

if __name__ == "__main__":
    main()
