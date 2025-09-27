# Azure OpenAI 模型速览

## 1. Azure OpenAI 是什么？
Azure OpenAI 服务将 OpenAI 的大语言模型部署到 Azure 的企业级基础设施上，提供与 OpenAI API 基本一致的体验，同时继承 Azure 的安全与合规特性。你可以通过 Azure Portal 管理模型部署，结合虚拟网络、私有终端和企业身份管理，满足内部应用对数据保护和可控性的要求。

主流模型系列包括：
- **GPT-4o / GPT-4.1**：多模态和较强推理能力，适合对话、代码生成、搜索等复杂任务。
- **GPT-4o mini / GPT-3.5 Turbo**：轻量、成本更低，适用于高并发、对延迟敏感的场景。
- **Embeddings（text-embedding-3 大系列）**：用于向量检索、语义搜索、语义分类等。
- **通用自定义模型（如 o3、Conversations、Deep Research 等）**：通过助手 API 提供特定能力，支持工具调用和工作流自动化。

## 2. 核心概念
| 名称 | 说明 |
|------|------|
| 资源（Resource） | 在某个 Azure 区域创建的 Azure OpenAI 服务实例。一个资源可以包含多个部署。 |
| 部署（Deployment） | 将特定模型版本挂载到资源上生成的 Endpoint。客户端使用部署名调用模型。 |
| 密钥（API Key）/Azure AD Token | 访问 Endpoint 的凭证。你可以使用密钥（key-based）或 Azure AD 应用（token-based）鉴权。 |
| API 版本（api-version） | 决定调用 API 时启用的功能。Azure OpenAI 通常以日期字符串表示，例如 `2024-06-01`. |

## 3. 初始化准备
1. 在 Azure Portal 注册并通过审批后创建 Azure OpenAI 资源。
2. 在 **Keys and Endpoint** 页面获取 `ENDPOINT` 与 `API_KEY`，或配置托管身份/Azure AD 应用。
3. 为目标模型创建部署，记录部署名称（如 `gpt-4o`、`gpt-4o-mini`）。
4. 安装 SDK（示例使用 Python 的 `azure-ai-openai` 或 OpenAI 官方 SDK）。

> 🎯 小贴士：在企业环境中推荐使用 Azure AD 鉴权并结合网络隔离（VNet + Private Endpoint），可以避免密钥外泄风险。

## 4. Python SDK 调用示例
以下示例展示了使用 Azure 官方 SDK（`azure-ai-openai>=1.0.0`）调用文本生成。

```python
# file: azure_openai_chat.py
import os
from azure.identity import DefaultAzureCredential
from azure.ai.openai import OpenAIClient

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
use_aad = os.getenv("USE_AAD", "false").lower() == "true"

if use_aad:
    token_credential = DefaultAzureCredential()
    client = OpenAIClient(endpoint=endpoint, credential=token_credential)
else:
    key = os.environ["AZURE_OPENAI_KEY"]
    client = OpenAIClient(endpoint=endpoint, credential=key)

response = client.get_chat_completions(
    deployment_id=deployment,
    messages=[
        {"role": "system", "content": "You are an Azure OpenAI assistant."},
        {"role": "user", "content": "Explain retrieval augmented generation in Chinese."},
    ],
    temperature=0.7,
    max_tokens=400,
)

for choice in response.choices:
    print("-- Response --")
    print(choice.message.content)
```

执行前需设置环境变量：
```bash
export AZURE_OPENAI_ENDPOINT="https://<your-resource-name>.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o"
export AZURE_OPENAI_KEY="<api-key>"  # 当使用 key-based 鉴权时
python azure_openai_chat.py
```

## 5. REST API 调用示例
借助 curl 也能快速验证部署是否工作。以下示例调用 `chat/completions` 接口：

```bash
curl https://$AZURE_OPENAI_ENDPOINT/openai/deployments/$AZURE_OPENAI_DEPLOYMENT/chat/completions?api-version=2024-06-01 \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_KEY" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "给我三条高效Prompt编写技巧"}
    ],
    "temperature": 0.2,
    "max_tokens": 256
  }'
```

若使用 Azure AD Token，只需将 `-H "api-key: ..."` 换成 `-H "Authorization: Bearer $ACCESS_TOKEN"`。

## 6. 生成式 AI 工作流最佳实践
- **提示工程（Prompt Engineering）**：分层结构、明确角色和输出格式，必要时结合 few-shot 示例。
- **检索增强生成（RAG）**：在回答前先从企业知识库检索相关文档，将结果拼接入 prompt，提高实时性和准确性。
- **上下文窗口管理**：控制对话轮数与文档长度，避免超过模型上下文限制；可利用 Token 计数工具（如 `tiktoken`）。
- **监控与审计**：启用 Azure Monitor/Log Analytics 跟踪使用量和异常，并通过内容过滤器管控输出。
- **缓存与并发**：对热点请求使用响应缓存，配置重试策略，确保在限流情况下依旧保证稳定性。

## 7. 常见问题 FAQ
1. **如何选择区域？** 先在 Azure OpenAI 申请页面确认资源可用性，一般建议就近部署以降低延迟。
2. **模型更新怎么办？** 当 OpenAI 发布新版本（如新版 GPT-4o），你可以创建新的部署平滑切换，或使用版本化部署（`deployment-capacity`）。
3. **是否支持多模态输入？** GPT-4o 支持文本、图像等多模态输入。SDK 中可通过 `content=[{"type": "text", ...}, {"type": "image_url", ...}]` 来上传图片 URL。
4. **如何节省成本？** 选择合适模型、控制 `max_tokens`、复用上下文、实施缓存策略，并监控用量预警。

## 8. 下一步
- 将 Azure OpenAI 与 Azure Functions、Logic Apps 等无服务器服务结合，快速构建应用。
- 使用 Azure AI Studio/Prompt Flow 进行可视化提示工程和评估。
- 集成 Azure AI Content Safety、Speech、Search 等服务，实现语音对话、语义搜索等复合场景。

---
如需更深入的企业级落地方案，可继续浏览本仓库的其它 Azure AI Demo 或参考官方文档：[Azure OpenAI Service 文档](https://learn.microsoft.com/azure/ai-services/openai/)。
