# Using a private, offline LLM for secure testing

When your test data, logs or code are confidential, use a model that runs on your own machine. With Ollama, nothing is sent to a cloud AI provider.

```bash
# 1. Install Ollama (Linux/WSL)
curl -fsSL https://ollama.com/install.sh | sh

# 2. Download a model
ollama pull llama3.2

# 3. Point this project at it (.env)
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2

# 4. Use any AI helper as usual
python -m ai.generate_test_cases docs/user-stories/checkout.md
```

**Good uses for a private LLM:** analyzing production logs, drafting bug reports that contain internal details, and reviewing proprietary test code.
**Trade-off:** small local models are faster to set up and private, but less accurate than large cloud models. Always review the output.
