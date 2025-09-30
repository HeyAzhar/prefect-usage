# Prefect Usage

A compact, hands-on repository with small Prefect example flows showing basics, sync vs async patterns, retry & logging patterns, and simple deployment/parameterized-deployment examples. Use this as a learning playground to try out local runs, `prefect` deploys, and triggering deployments programmatically.

---

## Table of contents

- [What’s in this repo](#whats-in-this-repo)
- [Prerequisites](#prerequisites)
- [Install](#install)
- [Directory structure (quick)](#directory-structure-quick)
- [Quickstart — run examples locally](#quickstart---run-examples-locally)
- [Key concepts demonstrated](#key-concepts-demonstrated)
- [Deployments & parameterized runs](#deployments--parameterized-runs)
- [Troubleshooting & tips](#troubleshooting--tips)
- [Contributing / License / Contact](#contributing--license--contact)

---

# What’s in this repo

This repo collects short, focused examples that demonstrate common Prefect (flow/task) patterns:

- `a_basics/` — minimal flows and tasks to get started.
- `b_sync_async_concepts/` — synchronous, asynchronous (`.submit()`), and mixed execution examples.
- `c_retry_logic/` — retry behavior, logging, and combined sync/async retry examples.
- `d_deployments/` — a small flow and a deployment walkthrough (example CLI transcript is included).
- `e_parameterized_deployments_workers/` — parameterized deployments, `prefect.yaml`, and example scripts to trigger deployments via the Prefect API.

---

# Prerequisites

- Python 3.8+ (or whichever you prefer; test locally)
- `pip` available
- Network access for any remote Prefect server / UI you run
- `prefect` installed (the repo's `requirements.txt` contains `prefect`)

> Note: this repo intentionally leaves the Prefect version unspecified in `requirements.txt`. If you rely on a specific Prefect version in your environment, pin it (for example `prefect==2.x.x`) in a virtual environment.

---

# Install

Create a virtual environment and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows Powershell

pip install -r requirements.txt
```

You can also install a specific prefect version if you want (optional):

```bash
pip install "prefect>=2.0.0"
```

---

# Directory structure (quick)

```
heyazhar-prefect-usage/
├── requirements.txt
├── .prefectignore
├── a_basics/
│   ├── 01_basic_example_with_flows.py
│   └── 02_flows_and_tasks.py
├── b_sync_async_concepts/
│   ├── 03_sync_demo.py
│   ├── 04_async_demo_with_submit.py
│   └── 05_async_sync_mixed_demo.py
├── c_retry_logic/
│   ├── 06_retry_logic.py
│   ├── 07_retry_logger.py
│   └── 08_sync_async_retry_logger.py
├── d_deployments/
│   ├── readme.md
│   ├── user_flow.py
│   └── .prefectignore
└── e_parameterized_deployments_workers/
    ├── readme.md
    ├── 01_trigger_deploymnet_by_id.py
    ├── 02_get_deployment_id_by_name.py
    ├── 03_trigger_deploymnet_by_id_name_lookup.py
    ├── prefect.yaml
    ├── user_account_balance.py
    └── .prefectignore
```

---

# Quickstart — run examples locally

After cloning the repo:

1. **Install Prefect** (and other requirements):

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Prefect server** (UI + API) locally:

   ```bash
   prefect server start
   ```

   > This launches Prefect locally, and you can access the dashboard in your browser at `http://localhost:4200`.

3. **Run an example flow**:  
   From the `a_basics/` folder, run any Python file:

   ```bash
   python a_basics/01_basic_example_with_flows.py
   ```

   or

   ```bash
   python a_basics/02_flows_and_tasks.py
   ```

4. **Check the run in the dashboard**:

   - Open the Prefect UI → **Flows**.
   - Click on the flow you just ran.
   - You’ll see the **Run list**; click into a run.
   - Under the **Visualize** tab, you can see the flow graph with tasks and their statuses — _that’s the beauty of Prefect!_

5. **Try other examples**:

   - Sync demo: `python b_sync_async_concepts/03_sync_demo.py`
   - Async demo: `python b_sync_async_concepts/04_async_demo_with_submit.py`
   - Mixed pattern: `python b_sync_async_concepts/05_async_sync_mixed_demo.py`
   - Retry/logging demos: `python c_retry_logic/06_retry_logic.py`, `07_retry_logger.py`, `08_sync_async_retry_logger.py`
   - Local flow test: `python d_deployments/user_flow.py`
   - Parameterized flow test: `python e_parameterized_deployments_workers/user_account_balance.py`

6. **Deployments & workers (quick)**:
   - To create a deployment in a folder containing a flow:
     ```bash
     cd d_deployments
     prefect deploy
     ```
   - Start a worker/agent that pulls from a work pool (on the machine that will execute flows):
     ```bash
     prefect worker start --pool 'default'
     ```
   - Trigger deployment runs from the UI, CLI, or programmatically (see `e_parameterized_deployments_workers` scripts).

---

# Key concepts demonstrated

A quick summary of the learning points by folder:

### `a_basics/`

- How to define `@flow` and `@task`.
- Returning values from tasks and flows.

### `b_sync_async_concepts/`

- Synchronous execution: tasks run sequentially.
- Asynchronous execution using `.submit()` so tasks run concurrently.
- Mixed patterns: dependencies between tasks while other tasks run in parallel.

### `c_retry_logic/`

- Task-level retries via task arguments (`retries`, `retry_delay_seconds`).
- Using `get_run_logger()` to instrument tasks and flows.
- Simulated failures to see retry behavior and logs in action.

### `d_deployments/`

- Example `user_account_flow` and a recorded CLI session showing `prefect deploy` usage and `prefect` output.
- Notes on creating deployments, saving `prefect.yaml`, and starting workers that pull from a work pool.

### `e_parameterized_deployments_workers`

- `prefect.yaml` sample for configuring deployable flows with parameters and working directory.
- Example scripts to:
  - Trigger a deployment by hard-coded deployment id (`01_trigger_deploymnet_by_id.py`)
  - Get deployment id by flow+deployment name via the Prefect API (`02_get_deployment_id_by_name.py`)
  - Lookup and trigger deployment in one script (`03_trigger_deploymnet_by_id_name_lookup.py`)

---

# Deployments & parameterized runs (details)

This repo includes example files and a `prefect.yaml` showing how a deployment can be created and saved.

Basic flow:

1. Create a deployment (from the directory containing your flow):

   ```bash
   prefect deploy
   ```

   The repo contains a recorded CLI transcript in `d_deployments/readme.md` demonstrating an interactive deployment flow where a `prefect.yaml` gets generated.

2. Start a worker/agent on a machine that will run the flow (the transcript uses `prefect worker start --pool 'default'` — check your Prefect version & docs, the exact command for agents/workers may vary by Prefect release and chosen infrastructure).

3. Trigger runs:
   - From the Prefect UI or CLI (`prefect deployment run 'flow-name/deployment-name'`), or
   - Programmatically via the Prefect API — the scripts under `e_parameterized_deployments_workers/` show how to call local Prefect API endpoints to create flow runs and pass parameters:
     - Get deployment id by name: `02_get_deployment_id_by_name.py`
     - Trigger a run by id: `01_trigger_deploymnet_by_id.py`
     - Lookup+trigger: `03_trigger_deploymnet_by_id_name_lookup.py`

> Important: the example scripts assume the Prefect API/UI is reachable at `http://localhost:4200`. Adjust the base URL if your Prefect server/Orion UI is on another host (for example an internal host).

---

# Troubleshooting & tips

- If a deployment CLI complains about `prefect.yaml` missing, create one or answer `prefect deploy` prompts interactively (the repo contains generated and example `prefect.yaml` files).
- When tasks randomly fail in retry demos, watch logs for retry attempts. The retry behavior is controlled by `retries` and `retry_delay_seconds` set on the `@task` decorator.
- If your workers cannot load flow code, ensure:
  - Workers have access to the project directory (or configure `push/pull` in `prefect.yaml`), or
  - Workers are configured to pull from a remote repo/storage (docker image or git).
- The CLI names for starting server, agents, or workers vary between Prefect versions. If a `prefect` subcommand fails, consult the Prefect docs or `prefect --help` for your installed version.
- When triggering via the API, ensure your Prefect server's API URL is correct and reachable from where you run the script.
