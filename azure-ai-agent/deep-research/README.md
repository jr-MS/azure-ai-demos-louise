# Deep Research Agent Demo

This folder contains a demo for using the Azure AI Deep Research Agent. The script `deep_research.py` demonstrates how to use Azure AI's project, agent, and Bing grounding capabilities to perform scientific research and generate a summary with references.

## 🏃‍♂️ How to Run

1. **Clone this repo and navigate to this folder:**
   ```sh
   cd azure-ai-agent/deep-research
   ```

2. **Create and update your `.env` file:**
   Create a file named `.env` in this directory with the following content:
   ```ini
   PROJECT_ENDPOINT=your_project_endpoint
   BING_RESOURCE_NAME=your_bing_resource_name
   DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME=your_deep_research_model
   MODEL_DEPLOYMENT_NAME=your_model_deployment
   ```
   > Replace each value with your actual Azure resource/configuration.

3. **Install dependencies:**
   ```sh
   pip install azure-ai-projects azure-identity azure-ai-agents
   ```

4. **Run the script:**
   ```sh
   python deep_research.py
   ```

5. **Follow the prompts:**
   - The script will create an agent, start a research thread, and interactively ask if you want to add more information or finish and generate a summary.
   - The summary (with references) will be saved as `research_summary.md`.

## 🔑 Required Environment Variables
- `PROJECT_ENDPOINT`: Your Azure AI Project endpoint URL.
- `BING_RESOURCE_NAME`: The Bing resource name for grounding.
- `DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME`: The deployment name of your Deep Research model.
- `MODEL_DEPLOYMENT_NAME`: The deployment name of the main model for the agent.

## 📄 Output
- `research_summary.md`: The generated research summary with references.

## 👩‍💻 Author
Louise Han, Solution Engineer, Azure AI

---
Happy researching with Azure AI! 💡
