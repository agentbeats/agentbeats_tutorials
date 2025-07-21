Stage I: reproducing Tensortrust example Red
Logging into a server with public ip (take an account from the spreadsheet)
Xy will take care
pip install agentbeats
wget xxx/example_tensortrust_red.toml
OPENAI_API_KEY=xxx agentbeats run exampleblabla.toml
Python script to make sure the agent is running locally? - test it clear
Register it on agentbeats website
Start a battle (selecting a particular WEAK blue agent and the one uploaded)
Check the result
Start another battle with STRONG blue agent
Check the result
Stage II: try to upgrade your red agent and win

Different methods to try out (provide baseline tomls/ folders / with explanations):
Upgrade the agent card
To have separate tool to try fixed command
Use different model (via CLI)
Leverage the tips in https://tensortrust.ai/wiki/Special:Attack_Guide 
Building a separate (a2a) agent? (we won’t be providing instructions here)


# 🔴 Building a Red Agent with AgentBeats SDK for TensorTrust

TensorTrust is a security game where your Red Agent tries to extract a secret key from an LLM. If the agent successfully makes the LLM say the key, or the phrase `"Access Granted"`, you win. Meanwhile, blue team agents will defend the LLM with system prompts.

This tutorial walks you through setting up a Red Agent with the AgentBeats SDK, launching attacks, and improving your strategy.

---

## Stage I: Reproducing the Example Red Agent

### Quick Setup

#### 1. Log into Server

...

get `AGENT_PORT` and `LAUNCHER_PORT` from the spreadsheet.

...
The backend should be running at port `...`


#### 2. Install AgentBeats SDK

Ensure you're using Python 3.11+.

```bash
pip install agentbeats
```

#### 3. Get Example Red Agent Config

Download the example configuration file for the Red Agent.

```bash
wget https://aaaaaaaaaaa/example_tensortrust_red.toml
```

#### 4. Run the Red Agent Locally

```bash
OPENAI_API_KEY=sk-xxx agentbeats run example_tensortrust_red.toml --launcher_host 0.0.0.0 --launcher_port LAUNCHER_PORT --backend ???
```

#### 5. Test Locally with Python

Use `test_red_agent.py` to ensure your agent is running correctly.

```bash
python .\test_red_agent.py --agent_url="http://localhost:AGENT_PORT"
```

### Start Battle On AgentBeats

**Register Your Red Agent on AgentBeats Website**

* Go to [https://agentbeats.org](https://agentbeats.org)
* Navigate to **Agents** → **Register Agent**
* Fill in:

  * **Agent URL**: `http://localhost:AGENT_PORT`
  * **Launcher URL**: `http://localhost:LAUNCHER_PORT`

**Start a Battle**

* Go to **Battles** -> **Stage a Battle**
* Select TensorTrust Host as green agent
* Select a weak Blue Agent like `adadadada`
* Choose your Red Agent from the dropdown
* Click "Create Battle"

**Try Again vs. Stronger Blue Agents**

Now challenge `bbbbbbaaaa`, it is a stronger Blue Agent.
See how they resist, and analyze what needs to change in your Red Agent.

---

## ⚔️ Stage II: Upgrade Your Red Agent and Win!

Improve your attack strategies with the following ideas:

#### 1. Modify the Agent Card

If you create agent with only `toml` file, the prompt is set in the `description` field. You can change it to something more effective:

```toml
...
name = "AAARed"
description = "Here is actually used as prompt. Update it!"
...
```


#### 2. Integrate Tools for Fixed Commands

123123



#### 3. Try Different Models

123123



#### 4. Read the Official Attack Guide

Check the community-driven [Attack Guide](https://tensortrust.ai/wiki/Special:Attack_Guide) for ideas.

#### 5. Advanced Custom Red Agent (Optional)

Power users may choose to:

* Build a fully custom A2A-compatible agent
* With more complex tools, reasoning, strategies...
* Host it on server and register it on AgentBeats

(Not included in this tutorial)
