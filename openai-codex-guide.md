# OpenAI Codex 使用指南

## 1. 简介
OpenAI Codex 是面向代码理解与生成的模型，可通过 OpenAI REST API 或官方 SDK（如 `openai` Python 包、JavaScript SDK）进行调用。本文档概述典型的使用流程，并提供可直接运行或用于自动化测试的示例代码，帮助你快速将 Codex 集成到现有项目中。

> ⚠️ 注意：当前主打的模型系列是 `gpt-3.5`/`gpt-4` 的代码能力，也兼容 Codex API。请在控制台确认你的账号仍然可以访问 `code-davinci-002` 等 Codex 部署，或换用具备代码补全能力的 GPT 模型。

## 2. 前提条件
- 拥有 OpenAI 账号，以及 Codex（或具备代码补全能力的 GPT 模型）的调用权限。
- 本地安装 Python 3.8+。
- 可访问互联网以调用 OpenAI API。
- 已在 [OpenAI 控制台](https://platform.openai.com/account/api-keys) 生成 API Key。

## 3. 环境配置
1. 创建隔离虚拟环境（可选）：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows 使用 .venv\\Scripts\\activate
   ```
2. 安装 OpenAI SDK：
   ```bash
   pip install openai>=1.11.0
   ```
3. 设置环境变量（推荐使用 `.env` 或 shell profile）：
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

## 4. 基础调用示例（Python）
下面的脚本演示了如何使用 GPT-4o Mini 兼容 Codex 能力的模型完成函数生成。若你仍在使用经典 Codex，可将模型名称改为 `code-davinci-002`。

```python
# file: codex_example.py
from openai import OpenAI

client = OpenAI()

prompt = """"""
编写一个 Python 函数 `fizz_buzz(n)`：
- 输入正整数 n
- 返回 1..n 列表，其中
  * 能被 3 整除 -> "Fizz"
  * 能被 5 整除 -> "Buzz"
  * 同时被 3 和 5 整除 -> "FizzBuzz"
  * 否则返回数字本身
""""""

response = client.responses.create(
    model="gpt-4o-mini",  # Codex: code-davinci-002
    input=[{"role": "user", "content": prompt}]
)

# 对于 responses API，代码结果通常位于 candidates[0].content
message = response.output[0].content[0].text
print("== Model Output ==")
print(message)
```

运行脚本：
```bash
python codex_example.py
```

## 5. 将生成代码写入文件
可把模型返回的代码保存为文件，方便后续执行或审阅：

```python
# file: save_code.py
from pathlib import Path
from openai import OpenAI

client = OpenAI()

prompt = "写一个可以解析 CSV 并转换为 JSON 的 Python 脚本。"

response = client.responses.create(
    model="gpt-4o-mini", 
    input=[{"role": "user", "content": prompt}]
)

code_snippet = response.output[0].content[0].text.strip()
Path("generated_script.py").write_text(code_snippet, encoding="utf-8")
print("代码已写入 generated_script.py")
```

## 6. 测试代码示例
调用真实 API 时通常无法在离线或 CI 中稳定运行测试，可通过模拟（mock）HTTP 请求来验证逻辑是否正确构造。

```python
# file: tests/test_codex_client.py
from types import SimpleNamespace
from unittest.mock import patch

from codex_example import client, prompt


def test_codex_request_payload():
    fake_leaf = SimpleNamespace(text="pass")
    fake_chunk = SimpleNamespace(content=[fake_leaf])
    fake_response = SimpleNamespace(output=[[fake_chunk]])

    with patch.object(client.responses, "create", return_value=fake_response) as mock_create:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[{"role": "user", "content": prompt}]
        )

    payload = mock_create.call_args.kwargs

    assert payload["model"] == "gpt-4o-mini"
    assert payload["input"][0]["content"] == prompt
    assert response.output[0][0].content[0].text == "pass"
```

运行测试：
```bash
pytest tests/test_codex_client.py
```

若希望集成经典 completions API（`client.completions.create`），可以采用类似的 Mock 技巧，重点验证 `model`、`prompt`、`max_tokens` 等核心参数。

## 7. 常见问题
- **提示词过长或响应超时**：适当缩短 prompt 或调整 `max_tokens`、`temperature`。
- **返回结果不是纯代码**：可在 prompt 中强调“只输出代码，不要解释”。
- **需要增量补全**：在编辑器场景下，将已有代码片段作为 prompt 的上下文即可。
- **速率限制**：遵循 OpenAI 提供的速率限制策略，必要时添加重试逻辑。

## 8. 后续扩展
- 使用 [Assistants API](https://platform.openai.com/docs/assistants/overview) 管理多轮对话与代码生成。
- 结合 Github Copilot 或 VS Code 插件获得更丰富的实时补全体验。
- 利用 OpenAI Functions/JSON mode 让 Codex 输出结构化数据以便二次处理。

---
如需进一步自定义，请根据自身项目结构调整模块与测试文件位置。例如将示例纳入现有 `tests/` 目录，并在 CI 中通过环境变量注入 Mock，从而避免真实请求。
