import os
import re

BENCHMARK_PATH = os.path.join(os.path.dirname(__file__), "generate_role_benchmarks.py")

with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update URLs
content = content.replace(
    'https://developer.android.com/distribute/best-practices/launch/launch-checklist',
    'https://developer.android.com/distribute/best-practices/launch'
)
content = content.replace(
    'https://roadmap.sh/software-design',
    'https://roadmap.sh/software-architect'
)
content = content.replace(
    'https://www.figma.com/community',
    'https://help.figma.com/hc/en-us/articles/360039238353-Guide-to-design-systems-in-Figma'
)
content = content.replace(
    'https://www.lucidchart.com/pages/bpmn-symbols-and-notation',
    'https://camunda.com/bpmn/'
)
content = content.replace(
    'https://www.softwaretestinghelp.com/user-acceptance-testing-uat/',
    'https://www.guru99.com/user-acceptance-testing.html'
)
content = content.replace(
    '"url": "https://docs.vllm.ai"',
    '"url": "https://docs.vllm.ai/en/latest/"'
)

# 2. Update O*NET codes
# Mobile App Developer: add 15-1252.00
old_mobile_sources = '''        "sources": [
            "https://roadmap.sh/flutter",
            "https://roadmap.sh/android",
            "https://roadmap.sh/react-native",
            "https://developer.android.com",
            "https://developer.apple.com"
        ],'''
new_mobile_sources = '''        "sources": [
            "https://roadmap.sh/flutter",
            "https://roadmap.sh/android",
            "https://roadmap.sh/react-native",
            "https://developer.android.com",
            "https://developer.apple.com",
            "https://www.onetonline.org/link/summary/15-1252.00"
        ],'''
content = content.replace(old_mobile_sources, new_mobile_sources)

# SRE: remove 15-1244.00
old_sre_sources = '''        "sources": [
            "https://roadmap.sh/devops",
            "https://sre.google/sre-book/table-of-contents/",
            "https://kubernetes.io/docs/",
            "https://www.onetonline.org/link/summary/15-1244.00"
        ],'''
new_sre_sources = '''        "sources": [
            "https://roadmap.sh/devops",
            "https://sre.google/sre-book/table-of-contents/",
            "https://kubernetes.io/docs/"
        ],'''
content = content.replace(old_sre_sources, new_sre_sources)

# Product Manager: remove 11-2021.00
old_pm_sources = '''        "sources": [
            "https://roadmap.sh/product-manager",
            "https://www.onetonline.org/link/summary/11-2021.00",
            "https://www.mindtheproduct.com"
        ],'''
new_pm_sources = '''        "sources": [
            "https://roadmap.sh/product-manager",
            "https://www.mindtheproduct.com"
        ],'''
content = content.replace(old_pm_sources, new_pm_sources)

# UI/UX Designer: 15-1255.01 -> 15-1255.00
content = content.replace(
    'https://www.onetonline.org/link/summary/15-1255.01',
    'https://www.onetonline.org/link/summary/15-1255.00'
)

# Cloud & DevOps: remove 15-1244.00
old_devops_sources = '''        "sources": ["https://roadmap.sh/devops", "https://www.onetonline.org/link/summary/15-1244.00"],'''
new_devops_sources = '''        "sources": ["https://roadmap.sh/devops"],'''
content = content.replace(old_devops_sources, new_devops_sources)

# Data Engineer: 15-2051.00 -> 15-1243.00
old_de_sources = '''        "sources": ["https://roadmap.sh/data-engineer", "https://www.onetonline.org/link/summary/15-2051.00"],'''
new_de_sources = '''        "sources": ["https://roadmap.sh/data-engineer", "https://www.onetonline.org/link/summary/15-1243.00"],'''
content = content.replace(old_de_sources, new_de_sources)

# 3. Expand Skill Synonyms for the 5 original roles
# AI Engineer Synonyms
old_ai_synonyms = '''        "skill_synonyms": {
            "python": ["python 3", "py"],
            "pytorch": ["torch"],
            "transformers": ["hugging face", "huggingface", "transformer models"],
            "vector database": ["vector db", "faiss", "pinecone", "chroma", "qdrant", "weaviate", "milvus"],
            "rag": ["retrieval-augmented generation", "hybrid rag", "retrieval augmented generation"],
            "langchain": ["langsmith", "langgraph"],
            "docker": ["containerization", "containers"],
            "fastapi": ["rest api", "python backend"],
            "cuda": ["gpu programming", "nvidia cuda", "tensorrt"],
            "model evaluation": ["evals", "ragas", "benchmarking", "perplexity"],
            "mlops": ["weights & biases", "wandb", "mlflow", "dvc"],
            "fine-tuning": ["sft", "lora", "qlora", "peft", "rlhf"],
            "large language models": ["llms", "gpt-4", "llama", "mistral", "claude"]
        },'''

new_ai_synonyms = '''        "skill_synonyms": {
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
        },'''
content = content.replace(old_ai_synonyms, new_ai_synonyms)

# Full Stack Developer Synonyms
old_fs_synonyms = '''        "skill_synonyms": {
            "typescript": ["ts"],
            "react": ["react.js", "reactjs"],
            "node.js": ["nodejs", "express", "express.js"],
            "next.js": ["nextjs"],
            "postgresql": ["postgres", "sql"],
            "tailwind css": ["tailwind"],
            "rest api": ["restful api", "restful apis"],
            "docker": ["containers"],
            "git": ["github", "gitlab"],
            "redis": ["caching", "in-memory cache"]
        },'''

new_fs_synonyms = '''        "skill_synonyms": {
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
        },'''
content = content.replace(old_fs_synonyms, new_fs_synonyms)

# Cloud & DevOps Engineer Synonyms
old_devops_synonyms = '''        "skill_synonyms": {
            "kubernetes": ["k8s"],
            "terraform": ["iac", "opentofu"],
            "ci/cd": ["github actions", "gitlab ci", "continuous integration"],
            "linux": ["bash", "shell scripting"],
            "aws": ["amazon web services"]
        },'''

new_devops_synonyms = '''        "skill_synonyms": {
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
        },'''
content = content.replace(old_devops_synonyms, new_devops_synonyms)

# Data Engineer Synonyms
old_de_synonyms = '''        "skill_synonyms": {
            "spark": ["pyspark", "apache spark"],
            "kafka": ["apache kafka"],
            "airflow": ["apache airflow"],
            "dbt": ["data build tool"],
            "snowflake": ["snowflake data warehouse"],
            "etl": ["elt", "data pipeline"]
        },'''

new_de_synonyms = '''        "skill_synonyms": {
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
        },'''
content = content.replace(old_de_synonyms, new_de_synonyms)

# Cybersecurity Analyst Synonyms
old_sec_synonyms = '''        "skill_synonyms": {
            "network security": ["network defense", "tcp/ip security"],
            "siem": ["splunk", "qradar", "sentinel"],
            "soc": ["security operations center"],
            "penetration testing": ["pentesting", "ethical hacking"],
            "incident response": ["ir", "dfir"],
            "mitre att&ck": ["att&ck framework"]
        },'''

new_sec_synonyms = '''        "skill_synonyms": {
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
        },'''
content = content.replace(old_sec_synonyms, new_sec_synonyms)

with open(BENCHMARK_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updates successfully applied to generate_role_benchmarks.py!")
