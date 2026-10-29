# AgentSquad Enterprise: Autonomous AI Workforce Platform
> **DEPI Graduation Project — Complete Engineering Documentation & Developer Guide**

---

## 1. Executive Summary & Vision

**AgentSquad Enterprise** is an autonomous AI workforce operating platform designed for solo founders, startups, and growing businesses. Rather than presenting generative AI as a generic chatbot with disposable prompts, the platform provides persistent, role-specialized **AI Employees** that understand the founder's brand context over time.

Each AI agent operates inside an isolated brand workspace, produces structured, versioned, and auditable deliverables (e.g., 30-day growth sprints, unit economics models, pitch deck narratives), and synchronizes outputs directly to external productivity tools like **Notion**, **Google Drive**, and corporate messaging channels.

### The 6 Core AI Employees

| # | Role Title | Persona | Commercial Model | Primary Strategic Responsibility |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Alex** — AI Cofounder / Orchestrator | Strategic Leader | Core (Included) | Company-wide reasoning, task delegation, team synthesis, and memory preservation. |
| **2** | **Nora** — Marketing Specialist | Growth Marketer | Hireable ($5/mo) | Go-to-market strategies, platform-specific content calendars, and campaign execution. |
| **3** | **Karim** — Sales Specialist | Deal Closer | Hireable ($5/mo) | Conversion funnels, discovery scripts, objection-handling playbooks, and outbound prep. |
| **4** | **Tarek** — Market & Customer Researcher | Evidence Analyst | Hireable ($5/mo) | Market sizing, competitor benchmarking, Ideal Customer Profiles (ICPs), and validation. |
| **5** | **Salma** — Financial Analyst | Quant Modeler | Hireable ($5/mo) | Assumption-driven financial modeling, CAC/LTV unit economics, and runway forecasting. |
| **6** | **Youssef** — Pitch Advisor | Investor Whisperer | Hireable ($5/mo) | Investor storyline development, pitch-deck generation/review, and VC Q&A practice. |

---

## 2. System Architecture & Flow

```text
  [ Founder / User ]
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              Streamlit Frontend (Port 8501)                 │
│  - 1_Login & 2_Register (Auth Sessions)                     │
│  - 3_Marketplace (Agent Catalog & Hiring)                   │
│  - 4_Agent_Chat (1-on-1 Direct Chat & Deliverable Cards)    │
│  - 5_My_Employees (Active Provisioned Workforce)            │
│  - 6_Integrations (Notion, Drive, WhatsApp Connectors)      │
│  - 7_Pricing_Plans (Tier Management & Billing Overview)     │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / REST API (Port 8001)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 FastAPI Backend Service                     │
│  - Routers: Auth, Workspaces, Agents, Chats, RAG, Billing   │
│  - Dependencies: Security (JWT), Workspace Tenant Resolution│
├─────────────────────────────────────────────────────────────┤
│                    Controllers Layer                        │
│  - DataController: File sanitization, MIME & size checks    │
│  - ProcessController: Text extraction & recursive chunking  │
│  - NLPController: Multi-tenant ChromaDB collection scoping  │
│  - AgentController: LangGraph dispatch & deliverable logging│
├──────────────────────────────┬──────────────────────────────┤
│      Beanie ODM (MongoDB)    │      RAG Engine (ChromaDB)   │
│  - Users, Workspaces         │  - Hybrid Search (BM25 +     │
│  - AgentCatalog, HiredAgents │    MiniLM Vector Embeddings) │
│  - Chats, Deliverables       │  - Cross-Encoder Re-ranker   │
│  - Subscriptions, Audits     │  - Strict workspace scoping  │
└──────────────────────────────┴──────────────────────────────┘
```

---

## 3. Complete Project Directory & File Guide

Below is the directory structure. Every file has a designated role in the system:

```text
DEPI_Graduation_Project/
├── docker-compose.yml             # Orchestrates MongoDB, ChromaDB, FastAPI, and Streamlit
├── .env                           # Local environment secrets and connection strings
├── .env.example                   # Template environment file for deployment
├── .gitignore                     # Prevents virtualenvs, binaries, and keys from committing
├── README.md                      # Complete system documentation and onboarding manual
│
├── backend/
│   ├── Dockerfile                 # Container image specification for FastAPI backend
│   ├── requirements.txt           # Python backend dependencies
│   ├── pytest.ini                 # Pytest configuration for running test suites
│   ├── app/
│   │   ├── main.py                # FastAPI app initialization, lifespan, CORS & health routes
│   │   ├── core/
│   │   │   ├── config.py          # Pydantic Settings reading .env variables
│   │   │   └── database.py        # MongoDB (Motor/Beanie) & ChromaDB client connection managers
│   │   ├── routes/                # Modular API routers defining all HTTP endpoints
│   │   │   ├── base.py            # Welcome & health check endpoint
│   │   │   ├── auth.py            # User registration & authentication endpoints
│   │   │   ├── workspaces.py      # Brand workspace management endpoints
│   │   │   ├── agents.py          # Agent catalog, hiring, and workforce endpoints
│   │   │   ├── data.py            # Document upload & ingestion endpoints
│   │   │   ├── nlp.py             # Semantic search & RAG query answer endpoints
│   │   │   ├── schemas/           # Pydantic Data Transfer Objects (DTOs) for request/response validation
│   │   │   │   ├── auth_schema.py      # Register & Login request/response models
│   │   │   │   ├── workspace_schema.py # Workspace creation & switching schemas
│   │   │   │   ├── agent_schema.py     # Hiring and workforce query schemas
│   │   │   │   ├── data_schema.py      # Document upload result schemas
│   │   │   │   ├── nlp_schema.py       # Semantic search & RAG answer schemas
│   │   │   │   └── __init__.py         # Consolidated DTO exports
│   │   │   └── __init__.py        # Export all API routers for FastAPI inclusion
│   │   ├── controllers/           # Business logic layer isolating API routes from domain logic
│   │   │   └── __init__.py        # Controller specifications guide for the engineering team
│   │   ├── enums/                 # Strongly-typed enumerations (each in its own file)
│   │   │   ├── agent_category.py  # 6 Functional agent categories
│   │   │   ├── agent_source.py    # Official, Partner, or Community source tags
│   │   │   ├── agent_status.py    # Active, Paused, or Terminated status
│   │   │   ├── deliverable_status.py # Draft, Needs Work, Approved, Synced
│   │   │   ├── deliverable_type.py# Marketing Plan, Financial Model, Pitch Deck, etc.
│   │   │   ├── integration_type.py# Notion, Google Drive, WhatsApp, Slack
│   │   │   ├── integration_status.py # Connected, Disconnected, Error
│   │   │   ├── message_sender.py  # User, Agent, or System message origins
│   │   │   ├── plan_type.py       # Free ($0), Pay as You Hire ($5), Scale ($50)
│   │   │   ├── response_signals.py# Standardized API response codes and signals
│   │   │   └── __init__.py        # Central export for all project enums
│   │   ├── models/                # MongoDB document definitions using Beanie ODM
│   │   │   ├── base.py            # AppBaseDocument & WorkspaceScopedDocument (Multi-tenancy)
│   │   │   ├── user.py            # User account model (Bcrypt hashing, active workspace pointer)
│   │   │   ├── workspace.py       # Workspace/Brand model (Name, industry, goals, settings)
│   │   │   ├── agent.py           # AgentCatalog (Marketplace) & HiredAgent (Provisioned instances)
│   │   │   ├── chat.py            # Conversation threads & individual ChatMessages
│   │   │   ├── deliverable.py     # Versioned deliverables (Code, summary, markdown, sync state)
│   │   │   ├── integration.py     # Connected third-party OAuth/API credentials
│   │   │   ├── subscription.py    # Workspace billing and active subscription calculator
│   │   │   ├── memory.py          # BrandMemory facts & DocumentMetadata for indexed RAG files
│   │   │   ├── assignment.py      # Structured tasks, agent dependencies, and deadlines
│   │   │   ├── approval.py        # Human-in-the-loop external action review queue
│   │   │   └── __init__.py        # All document models export list for Beanie initialization
│   │   ├── db/
│   │   │   └── seed_catalog.py    # Seeder script populating MongoDB with the 6 core AI employees
│   │   └── rag/                   # Dedicated Retrieval-Augmented Generation Engine
│   │       ├── __init__.py        # Exports RAGService
│   │       ├── data/              # Workspace sample documents, metadata, evaluations, and VS
│   │       ├── ingestion/
│   │       │   ├── loader.py      # Extract text from PDF, Markdown, and TXT files
│   │       │   └── chunker.py     # Recursive text splitter with overlap configuration
│   │       ├── retrieval/
│   │       │   ├── embedding.py   # HuggingFace MiniLM vector embeddings generator
│   │       │   ├── vector_store.py# ChromaDB client & vector index management
│   │       │   └── retriver.py    # Hybrid search (Dense vector + BM25 sparse lexical search)
│   │       ├── generation/
│   │       │   ├── llm.py         # LLM client setup (Groq / OpenAI)
│   │       │   └── prompt.py      # Context-grounded system prompts with anti-hallucination rules
│   │       ├── configuration/
│   │       │   └── settings.py    # Internal RAG parameters (k, chunk size, models, local paths)
│   │       └── application/
│   │           └── rag_service.py # Central orchestrator (retrieve -> rerank -> generate -> citations)
│   └── tests/
│       └── rag/                   # Comprehensive RAG test suite
│           ├── test_ingestion.py  # Tests loaders and chunking boundaries
│           ├── test_retrieval.py  # Tests ChromaDB storage, query, and BM25 search
│           ├── test_generation.py # Tests LLM prompting and output parsing
│           └── test_rag_service.py# End-to-end workflow verification
│
└── frontend/
    ├── Dockerfile                 # Container image specification for Streamlit frontend
    ├── requirements.txt           # Python dependencies for UI
    ├── app.py                     # Main dashboard, brand switcher, and executive summary
    └── pages/
        ├── 1_Login.py             # User authentication and session establishment
        ├── 2_Register.py          # Account creation & initial workspace setup
        ├── 3_Marketplace.py       # Catalog browsing, filtering, and agent hiring ($5/mo)
        ├── 4_Agent_Chat.py        # 1-on-1 channel (# dm-agent), deliverable cards, and Notion push
        ├── 5_My_Employees.py      # Deployed workforce directory for active workspace
        ├── 6_Integrations.py      # Connect Notion, Google Drive, WhatsApp, and Slack
        └── 7_Pricing_Plans.py     # Transparent billing breakdown (Free, Pay as You Hire, Scale)
```

---

## 4. Comprehensive Database Schema Reference (MongoDB Models & Fields)

Every database document inherits from either `AppBaseDocument` (for system-wide records) or `WorkspaceScopedDocument` (for brand-specific records).

### Base Models (`app/models/base.py`)

#### `AppBaseDocument`
Base class providing audit timestamps and soft-delete capabilities.
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `PydanticObjectId` | Unique document identifier in MongoDB (`_id`). |
| `created_at` | `datetime` | UTC timestamp when the record was initially created. |
| `updated_at` | `datetime` | UTC timestamp automatically refreshed on every `.save()`. |
| `is_deleted` | `bool` | Soft-delete flag; enables data recovery without hard deletions. |

#### `WorkspaceScopedDocument`
Inherits from `AppBaseDocument`. **Guarantees multi-tenant isolation.**
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Indexed foreign key tying this document to a specific brand workspace. |

---

### User & Workspace Models

#### `User` (`app/models/user.py` — Collection: `users`)
Represents the human founder or operator.
| Field | Type | Description |
| :--- | :--- | :--- |
| `email` | `EmailStr` | Unique login email address (indexed). |
| `hashed_password` | `str` | Bcrypt-hashed password. Plain text is never persisted. |
| `full_name` | `str` | Display name of the founder. |
| `avatar_url` | `Optional[str]` | Optional URL for user avatar image. |
| `is_active` | `bool` | Whether the account is permitted to authenticate. |
| `is_superuser` | `bool` | Administrator flag for platform operators. |
| `current_active_workspace_id` | `Optional[PydanticObjectId]` | Pointer to the workspace currently selected in the UI. |

#### `Workspace` (`app/models/workspace.py` — Collection: `workspaces`)
The primary boundary container for a brand or company.
| Field | Type | Description |
| :--- | :--- | :--- |
| `owner_id` | `PydanticObjectId` | Indexed reference to the owning `User`. |
| `name` | `str` | Company/Brand name (e.g., `Daz Apparel`). |
| `slug` | `str` | URL-friendly unique identifier. |
| `brand_description` | `Optional[str]` | High-level summary of products, mission, and value proposition. |
| `website_url` | `Optional[str]` | Brand website or store URL. |
| `industry` | `Optional[str]` | Business sector (e.g., E-Commerce, HealthTech). |
| `target_audience` | `Optional[str]` | Target persona or Ideal Customer Profile (ICP) definition. |
| `settings` | `WorkspaceSettings` | Embedded sub-document with model configs, temperature, and brand tone. |

---

### Agent Models (`app/models/agent.py`)

#### `AgentCatalog` (Collection: `agent_catalog`)
The system-wide marketplace catalog defining available AI employees.
| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | `str` | Agent display name (e.g., `Cole`, `Alex`, `Nora`). |
| `title` | `str` | Official job title (e.g., `Marketing & Growth Strategist`). |
| `category` | `AgentCategory` | Indexed role classification enum. |
| `source` | `AgentSource` | Origin enum: `OFFICIAL`, `BUILT_BY_PARTNER`, or `COMMUNITY`. |
| `avatar_url` | `str` | URL pointing to agent avatar image. |
| `short_bio` | `str` | Concise overview of responsibilities and capabilities. |
| `rating` | `float` | Marketplace user rating out of 5.0. |
| `reviews_count` | `int` | Total number of recorded user reviews. |
| `is_star_agent` | `bool` | Badge highlighting top-performing agents. |
| `is_official` | `bool` | Verified badge indicating core platform certification. |
| `built_by` | `str` | Credit attribution to agent author/team. |
| `tags` | `List[str]` | Skill tags (e.g., `["GTM Strategy", "Notion Sync"]`). |
| `monthly_price` | `float` | Recurring monthly subscription fee in USD ($5.00/mo or $0 for core). |
| `system_prompt_template`| `str` | Foundational system prompt defining agent persona, constraints, and format. |
| `capabilities` | `List[str]` | Identifiers for registered tools the agent is permitted to execute. |

#### `HiredAgent` (Collection: `hired_agents`)
An active instance of an agent provisioned inside a brand workspace.
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Associated workspace ID (Scoped). |
| `catalog_id` | `PydanticObjectId` | Reference back to the origin `AgentCatalog` record. |
| `name` | `str` | Agent name. |
| `title` | `str` | Agent title. |
| `category` | `AgentCategory` | Functional category. |
| `avatar_url` | `str` | Avatar image URL. |
| `status` | `AgentStatus` | `ACTIVE`, `PAUSED`, or `TERMINATED`. |
| `monthly_price` | `float` | Monthly billing rate locked upon hiring. |
| `custom_instructions` | `Optional[str]` | Founder-specified tone overrides or brand preferences. |

---

### Chat & Deliverable Models

#### `Conversation` (`app/models/chat.py` — Collection: `conversations`)
A communication thread between the founder and a hired agent.
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Scoped brand workspace. |
| `hired_agent_id`| `PydanticObjectId` | Associated hired agent. |
| `title` | `str` | Topic title (e.g., `30-Day Growth Sprint Strategy`). |
| `is_pinned` | `bool` | Whether the thread is pinned to the top of the sidebar. |

#### `ChatMessage` (`app/models/chat.py` — Collection: `chat_messages`)
Individual messages exchanged inside a conversation.
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Scoped brand workspace. |
| `conversation_id`| `PydanticObjectId` | Parent conversation reference. |
| `sender` | `MessageSender` | Author enum: `USER`, `AGENT`, or `SYSTEM`. |
| `sender_name` | `str` | Display name of the sender. |
| `content` | `str` | The actual text message or prompt. |
| `thought_process`| `Optional[str]` | Agent chain-of-thought / reasoning steps before answering. |
| `deliverable_ids`| `List[PydanticObjectId]`| References to deliverables generated during this turn. |
| `metadata` | `Dict[str, Any]` | Extensible bag for token usage, tool calls, or citation links. |

#### `Deliverable` (`app/models/deliverable.py` — Collection: `deliverables`)
Structured work artifacts produced by agents (growth sprints, decks, models).
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Scoped brand workspace. |
| `hired_agent_id`| `PydanticObjectId` | Agent that authored the deliverable. |
| `conversation_id`| `PydanticObjectId`| Chat thread where the deliverable was created. |
| `tracking_code` | `str` | Human-readable tracking identifier (e.g., `STRAT-6`, `DOC-12`). |
| `title` | `str` | Title (e.g., `30-Day Growth Sprint Plan`). |
| `deliverable_type`| `DeliverableType` | Enum: `MARKETING_PLAN`, `FINANCIAL_MODEL`, `PITCH_DECK`, etc. |
| `summary` | `str` | Executive summary or preview paragraph. |
| `content_markdown`| `str` | Comprehensive report content formatted in Markdown. |
| `structured_data`| `Dict[str, Any]` | Raw tabular JSON (e.g., financial formula cells, slide arrays). |
| `status` | `DeliverableStatus`| Review state: `DRAFT`, `NEEDS_WORK`, `APPROVED`, `SYNCED_TO_INTEGRATION`. |
| `user_feedback` | `Optional[str]` | Rejection notes or revision instructions from founder. |
| `synced_integration`| `Optional[str]` | External destination platform name (e.g., `Notion`, `Google Drive`). |
| `synced_external_url`| `Optional[str]`| Direct link to the created document in the external service. |

---

### Integrations & Billing Models

#### `UserIntegration` (`app/models/integration.py` — Collection: `user_integrations`)
External productivity connectors configured for a workspace.
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Scoped brand workspace. |
| `provider` | `IntegrationType` | Service enum: `NOTION`, `GOOGLE_DRIVE`, `WHATSAPP`, `SLACK`. |
| `status` | `IntegrationStatus`| Connection state: `CONNECTED`, `DISCONNECTED`, `ERROR`. |
| `account_name` | `Optional[str]` | External connected account identifier (e.g., Notion Workspace name). |
| `access_token` | `Optional[str]` | Encrypted OAuth or API credential. |
| `refresh_token` | `Optional[str]` | Token refresh credential. |
| `config` | `Dict[str, Any]` | Service settings (e.g., target Notion parent page ID, Drive folder ID). |

#### `WorkspaceSubscription` (`app/models/subscription.py` — Collection: `workspace_subscriptions`)
Workforce capacity tracking and monthly fee calculation.
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Scoped brand workspace. |
| `plan` | `PlanType` | Plan tier: `FREE`, `PAY_AS_YOU_HIRE`, or `SCALE`. |
| `hired_agents_count`| `int` | Total count of currently active hired agents. |
| `monthly_amount` | `float` | Calculated monthly bill in USD. |
| `is_active` | `bool` | Subscription active flag. |
| `next_billing_date`| `Optional[datetime]`| Next scheduled invoice generation date. |

---

### Knowledge Base & Governance Models

#### `DocumentMetadata` (`app/models/memory.py` — Collection: `uploaded_documents`)
Tracks founder-uploaded files indexed into ChromaDB.
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Scoped brand workspace. |
| `filename` | `str` | Original uploaded filename. |
| `file_size_bytes` | `int` | File size in bytes. |
| `mime_type` | `str` | Detected MIME type (e.g., `application/pdf`). |
| `chroma_collection_name`| `str` | ChromaDB collection storing the embeddings (`workspace_{id}`). |
| `chunks_count` | `int` | Number of text chunks generated and stored. |
| `summary` | `Optional[str]` | High-level summary of the document. |

#### `BrandMemory` (`app/models/memory.py` — Collection: `brand_memories`)
Durable ground-truth facts (voice tone, target customer, proven decisions) accessible to all agents.
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Scoped brand workspace. |
| `title` | `str` | Fact headline or policy name. |
| `content` | `str` | The context or policy text. |
| `category` | `str` | Categorization tag (e.g., `brand_guidelines`, `pricing_rules`). |
| `tags` | `List[str]` | Searchable keywords. |

#### `Assignment` (`app/models/assignment.py` — Collection: `assignments`)
Multi-agent task tracking and dependencies.
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Scoped brand workspace. |
| `assigned_by` | `AssignedByType` | Task creator: `FOUNDER` or `COFOUNDER`. |
| `assigned_to_hired_employee_id`| `PydanticObjectId`| Designated hired agent responsible for the deliverable. |
| `title` | `str` | Task headline. |
| `goal` | `str` | Clear objective to be achieved. |
| `context` | `str` | Background documents and constraints provided. |
| `status` | `AssignmentStatus`| `DRAFT`, `PENDING`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`. |
| `priority` | `AssignmentPriority`| `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. |
| `dependency_assignment_ids`| `List[PydanticObjectId]`| Prerequisite tasks that must complete first. |
| `deliverable_artifact_ids`| `List[PydanticObjectId]`| Output deliverables produced upon task completion. |

#### `ApprovalRequest` (`app/models/approval.py` — Collection: `approval_requests`)
Human-in-the-loop review queue for external agent actions (social posts, emails, calls).
| Field | Type | Description |
| :--- | :--- | :--- |
| `workspace_id` | `PydanticObjectId` | Scoped brand workspace. |
| `proposed_by_employee_id`| `PydanticObjectId`| The agent requesting to execute an action. |
| `action_type` | `ExternalActionType`| `SOCIAL_MEDIA_POST`, `EMAIL_OUTREACH`, `WHATSAPP_MESSAGE`, etc. |
| `destination_platform`| `str` | Target platform (e.g., `LinkedIn`, `WhatsApp`). |
| `proposed_payload`| `Dict[str, Any]` | Exact proposed post text, recipient list, or parameters. |
| `justification_reason`| `str` | Agent's reasoning why this action is recommended. |
| `context_summary`| `str` | Background context for the founder. |
| `status` | `ApprovalStatus` | `PENDING`, `APPROVED`, `EDITED_AND_APPROVED`, `REJECTED`, `EXECUTED`. |
| `founder_modified_payload`| `Optional[Dict[str, Any]]`| Founder's edited version if modified before approval. |
| `founder_feedback`| `Optional[str]` | Feedback or rejection justification. |
| `execution_result`| `Optional[Dict[str, Any]]`| API response or audit log after external execution. |

---

## 5. Software Engineering Design: The Controllers Pattern (`backend/app/controllers/`)

To guarantee code maintainability, clean architecture, and testability, all business logic is isolated into a dedicated **Controllers** layer:

### Why Use Controllers?
1. **Skinny Routers:** FastAPI route handlers should only handle HTTP concerns: deserializing requests, validating query parameters, and returning response models.
2. **Fat Controllers / Services:** Complex operations (e.g., file validation, security sanitation, vector index operations, LangGraph invocations) reside in controllers.
3. **Reusability:** A controller function can be invoked from a FastAPI endpoint, a Celery worker, a CLI script, or unit tests without duplicating logic.

### Team Implementation Guide: Planned Controllers
When contributing to `backend/app/controllers/`, structure your code as follows:
* **`DataController`**:
  * `validate_upload_file(file)`: Verifies file size <= 25MB and MIME type (PDF, Markdown, TXT, CSV).
  * `get_clean_filename(name)`: Strips unsafe characters and prevents directory traversal attacks.
  * `generate_unique_filepath(name, workspace_id)`: Generates non-colliding paths inside `data/assets/files/ws_{workspace_id}/`.
* **`ProcessController`**:
  * `extract_text_from_file(path)`: Uses `pypdf.PdfReader` for PDFs and standard text decoding for markdown/text.
  * `chunk_document(text, source)`: Applies `RecursiveCharacterTextSplitter` (chunk_size=500, overlap=50).
* **`NLPController`**:
  * `create_collection_name(workspace_id)`: Enforces `workspace_{workspace_id}` collection names in ChromaDB.
  * `index_chunks(chunks)`: Adds text chunks and metadata into ChromaDB.
  * `search_similar(query, limit)`: Runs semantic vector similarity queries.
  * `answer_rag_question(query)`: Bridges retrieved chunks to `RAGService` to produce grounded answers with citations.
* **`AgentController`**:
  * Coordinates LangGraph orchestrator execution, manages state checkpoints, and logs deliverables into MongoDB.

---

## 6. Modular API Routing & Pydantic Validation (`backend/app/routes/` & `backend/app/routes/schemas/`)

To adhere to the reference architecture and maintain clean separation of concerns, the API layer is organized into **modular routers** with dedicated **Pydantic Data Transfer Objects (DTOs)**:

### Architecture: The 4-Tier Separation

```text
  [ Client Request ]
         │
         ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  1. routes/ (FastAPI APIRouters)                            │
  │     - Route path mapping, HTTP verbs, and status codes      │
  │     - Dependency injection (Authentication, DB sessions)    │
  └──────────────────────────────┬──────────────────────────────┘
                                 │ Validates payload via
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  2. routes/schemas/ (Pydantic DTOs)                         │
  │     - Enforces strict input constraints (Email, string len) │
  │     - Strips sensitive internal fields from responses       │
  └──────────────────────────────┬──────────────────────────────┘
                                 │ Dispatches to
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  3. controllers/ (Business Logic & Orchestration)           │
  │     - Multi-step validation, file sanitization, RAG calls   │
  │     - Independent from HTTP context (reusable in CLI/tests) │
  └──────────────────────────────┬──────────────────────────────┘
                                 │ Persists / Queries
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  4. models/ (MongoDB Beanie Documents & ChromaDB Vectors)   │
  │     - Database persistence and multi-tenant workspace scope │
  └─────────────────────────────────────────────────────────────┘
```

### Modular Router Breakdown

Every router is self-contained with its own prefix and OpenAPI tag, registered centrally in `app/main.py`:

| Router File | URL Prefix | Primary Responsibility | Standard Response Signals |
| :--- | :--- | :--- | :--- |
| **`base.py`** | `/api/v1` | Health checks and root API service discovery | `HEALTH_CHECK_SUCCESS` |
| **`auth.py`** | `/api/v1/auth` | User account registration and JWT login verification | `USER_REGISTER_SUCCESS`, `USER_LOGIN_SUCCESS` |
| **`workspaces.py`** | `/api/v1/workspaces` | Multi-tenant brand workspace creation and listing | `WORKSPACE_CREATE_SUCCESS`, `WORKSPACE_LIST_SUCCESS` |
| **`agents.py`** | `/api/v1/agents` | Catalog browsing, employee hiring ($5/mo), active workforce | `AGENT_HIRE_SUCCESS`, `AGENT_CATALOG_SUCCESS` |
| **`data.py`** | `/api/v1/data` | File upload validation and document ingestion | `FILE_UPLOAD_SUCCESS`, `FILE_VALIDATE_ERROR` |
| **`nlp.py`** | `/api/v1/nlp` | Semantic vector search and grounded RAG question answering | `SEARCH_VECTOR_DB_SUCCESS`, `RAG_ANSWER_SUCCESS` |

### Pydantic Schemas (`backend/app/routes/schemas/`)

Requests and responses do not pass raw MongoDB documents to the client. Instead, they use typed DTOs:

* **`auth_schema.py`**:
  * `RegisterRequest`: Validates `email` format, `password` (minimum 8 characters), and `full_name`.
  * `LoginRequest`: Validates login credentials.
  * `AuthResponse`: Returns user identity, JWT access token, and standard response signal.
* **`workspace_schema.py`**:
  * `WorkspaceCreateRequest`: Validates company name (minimum 2 chars), industry, and optional ICP.
  * `WorkspaceResponse`: Clean public view of workspace without internal MongoDB metadata.
* **`agent_schema.py`**:
  * `HireAgentRequest`: Validates catalog agent reference, nickname, and custom company instructions.
  * `HiredAgentResponse`: Formats hired employee status, provisioning date, and active state.
* **`data_schema.py`**:
  * `FileUploadResponse`: Returns uploaded file size, sanitized filename, storage path, and processing status.
* **`nlp_schema.py`**:
  * `SearchRequest`: Validates semantic search query and top-k retrieval bounds (1 to 20).
  * `RAGQueryRequest`: Captures natural language question and temperature/limit parameters.
  * `RAGQueryResponse`: Formats generated answer, cited source documents, and confidence metadata.

---

## 7. RAG Engine: Architecture & Advanced Features (`backend/app/rag/`)

The platform integrates a production-ready, hybrid **Retrieval-Augmented Generation (RAG)** engine located in `backend/app/rag/`:

```text
[ User / Agent Query ]
         │
         ├───► Sparse Lexical Search (BM25: Exact keywords, acronyms, SKUs)
         │
         └───► Dense Semantic Search (HuggingFace MiniLM: 384-d ChromaDB vectors)
                      │
                      ▼
         [ Reciprocal Rank Fusion & Reranking ]
         (Cross-Encoder: ms-marco-MiniLM-L-6-v2)
                      │
                      ▼
         [ Maximum Marginal Relevance (MMR) ] -> Eliminate duplicate content
                      │
                      ▼
         [ Context-Constrained Prompt Assembly ] -> Source citation tags
                      │
                      ▼
         [ LLM Generation (Groq / OpenAI) ] -> Grounded Answer + Evidence
```

### Key Technical Features:
1. **Multi-Format Ingestion (`ingestion/`)**:
   * Text loaders for `.pdf`, `.md`, and `.txt` with automatic encoding detection.
   * Chunker with configurable overlap ensuring sentences are not truncated mid-thought.
2. **Hybrid Search Retrieval (`retrieval/`)**:
   * Combines **Dense Vectors** (for conceptual semantic similarity) and **BM25 Sparse Search** (for exact term matching).
   * Dense embeddings utilize `sentence-transformers/all-MiniLM-L6-v2`.
3. **Cross-Encoder Re-Ranking (`retrieval/retriver.py`)**:
   * Initial search gathers `initial_k=15` candidate chunks.
   * `cross-encoder/ms-marco-MiniLM-L-6-v2` re-ranks candidate pairs to return top `k=5` high-precision passages.
4. **Transparent Evidence & Anti-Hallucination (`application/rag_service.py`)**:
   * LLM responses strictly format citations: `[Source N: Document Title | Section Name]`.
   * If retrieved context is insufficient, the prompt mandates returning: *"No relevant documentation found in this workspace."*
5. **Multi-Tenant ChromaDB Collections**:
   * Each brand workspace has its own collection, guaranteeing that Workspace A cannot access Workspace B's intellectual property.

---

## 8. REST API Endpoints Specification

All endpoints are prefixed with `/api/v1` and return standardized JSON payloads:

### 1. Authentication (`/api/v1/auth`)
* `POST /api/v1/auth/register` — Register a new founder account.
  * Request: `{ "email": "founder@brand.com", "password": "...", "full_name": "..." }`
  * Response: `{ "user_id": "...", "email": "..." }`
* `POST /api/v1/auth/login` — Authenticate and receive JWT token.
  * Request: `OAuth2PasswordRequestForm` (username/password)
  * Response: `{ "access_token": "...", "token_type": "bearer" }`
* `GET /api/v1/auth/me` — Return current authenticated profile.

### 2. Workspaces (`/api/v1/workspaces`)
* `GET /api/v1/workspaces/` — List all brand workspaces owned by user.
* `POST /api/v1/workspaces/` — Create new workspace.
  * Request: `{ "name": "Daz Apparel", "industry": "Fashion", "brand_description": "..." }`
* `GET /api/v1/workspaces/{id}` — Fetch workspace details, settings, and strategic goals.
* `POST /api/v1/workspaces/{id}/switch` — Set workspace as active in session.

### 3. Agent Marketplace & Hiring (`/api/v1/agents`)
* `GET /api/v1/agents/catalog` — List all 6 AI employees with skills, bios, and ratings.
* `POST /api/v1/agents/hire` — Hire an employee into active workspace.
  * Request: `{ "catalog_id": "...", "custom_instructions": "..." }`
  * Response: `{ "hired_agent_id": "...", "status": "active" }`
* `GET /api/v1/agents/my-workforce` — List active employees provisioned in current workspace.
* `DELETE /api/v1/agents/{hired_id}` — Decommission employee and adjust subscription.

### 4. Workspace Chat & Deliverables (`/api/v1/chats` & `/api/v1/deliverables`)
* `GET /api/v1/chats/conversations?hired_agent_id={id}` — List conversations with agent.
* `POST /api/v1/chats/{conversation_id}/messages` — Post user message and receive agent response.
  * Request: `{ "content": "Create a 30-day marketing plan for Daz." }`
* `GET /api/v1/deliverables/` — List deliverables for workspace.
* `POST /api/v1/deliverables/{id}/feedback` — Submit feedback (`Needs Work` or `Approved`).
* `POST /api/v1/deliverables/{id}/sync` — Export deliverable directly to Notion or Drive.

### 5. Knowledge Base & RAG (`/api/v1/rag`)
* `POST /api/v1/rag/upload` — Upload and index documents (`multipart/form-data`).
* `POST /api/v1/rag/query` — Execute semantic search or ask questions over indexed brand docs.
  * Request: `{ "question": "What is our refund policy on outerwear?" }`
  * Response: `{ "answer": "...", "sources": [...] }`

### 6. Integrations (`/api/v1/integrations`)
* `GET /api/v1/integrations/status` — Get status of Notion, Drive, WhatsApp connectors.
* `POST /api/v1/integrations/{provider}/connect` — Store API credentials/OAuth tokens.

### 7. Subscriptions (`/api/v1/billing`)
* `GET /api/v1/billing/summary` — Return active plan, hired agent count, and monthly run rate.
* `POST /api/v1/billing/plan` — Update plan tier (`free`, `pay_as_you_hire`, `scale`).

---

## 9. Developer Setup & Execution Guide

### Option A: Running with Docker (Recommended)
Docker Compose provisions MongoDB, ChromaDB, FastAPI, and Streamlit in isolated containers.

1. **Configure Environment:**
   Ensure `.env` exists in the project root:
   ```bash
   copy .env.example .env
   ```
   Add your `GROQ_API_KEY` or `OPENAI_API_KEY` in `.env`.

2. **Build and Launch Stack:**
   ```bash
   docker compose up --build -d
   ```

3. **Check Service Status:**
   ```bash
   docker compose ps
   ```

4. **Access Applications:**
   * **Streamlit UI:** [http://localhost:8501](http://localhost:8501)
   * **FastAPI Docs:** [http://localhost:8001/docs](http://localhost:8001/docs)
   * **Health Check:** [http://localhost:8001/health](http://localhost:8001/health)

---

### Option B: Local Development Setup (Manual)

1. **Python Environment Setup:**
   Ensure Python 3.11+ is installed.
   ```bash
   python -m venv .venv
   .venv\Scripts\activate          # On Windows
   # source .venv/bin/activate     # On Linux / macOS
   ```

2. **Install Backend Dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Seed Initial Agent Catalog:**
   Populate MongoDB with the 6 core AI employees (Alex, Nora, Karim, Tarek, Salma, Youssef):
   ```bash
   python -m backend.app.db.seed_catalog
   ```

4. **Start the FastAPI Backend:**
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

5. **Start the Streamlit Frontend (in a separate terminal):**
   ```bash
   pip install -r frontend/requirements.txt
   streamlit run frontend/app.py --server.port 8501
   ```

---

## 10. Running Automated Tests

The test suite verifies the RAG ingestion, vector storage, hybrid retrieval, and LLM generation pipelines:

```bash
cd backend
pytest tests/rag -v
```

All test cases are configured in `backend/pytest.ini` and execute against test datasets in `backend/app/rag/data/`.
