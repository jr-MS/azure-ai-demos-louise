import os, time
from typing import Optional
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import DeepResearchTool, MessageRole, ThreadMessage


def fetch_and_print_new_agent_response(
    thread_id: str,
    agents_client: AgentsClient,
    last_message_id: Optional[str] = None,
) -> Optional[str]:
    response = agents_client.messages.get_last_message_by_role(
        thread_id=thread_id,
        role=MessageRole.AGENT,
    )
    if not response or response.id == last_message_id:
        return last_message_id, None  # No new content

    print("\nAgent response:")
    print("\n".join(t.text.value for t in response.text_messages))

    for ann in response.url_citation_annotations:
        print(f"URL Citation: [{ann.url_citation.title}]({ann.url_citation.url})")

    return response.id, response


def create_research_summary(
        message : ThreadMessage,
        filepath: str = "research_summary.md"
) -> None:
    if not message:
        print("No message content provided, cannot create research summary.")
        return

    with open(filepath, "w", encoding="utf-8") as fp:
        # Write text summary
        text_summary = "\n\n".join([t.text.value.strip() for t in message.text_messages])
        fp.write(text_summary)

        # Write unique URL citations, if present
        if message.url_citation_annotations:
            fp.write("\n\n## References\n")
            seen_urls = set()
            for ann in message.url_citation_annotations:
                url = ann.url_citation.url
                title = ann.url_citation.title or url
                if url not in seen_urls:
                    fp.write(f"- [{title}]({url})\n")
                    seen_urls.add(url)

    print(f"Research summary written to '{filepath}'.")


project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

conn_id = project_client.connections.get(name=os.environ["BING_RESOURCE_NAME"]).id


# Initialize a Deep Research tool with Bing Connection ID and Deep Research model deployment name
deep_research_tool = DeepResearchTool(
    bing_grounding_connection_id=conn_id,
    deep_research_model=os.environ["DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME"],
)

# Create Agent with the Deep Research tool and process Agent run
with project_client:

    with project_client.agents as agents_client:

        # Create a new agent that has the Deep Research tool attached.
        agent = agents_client.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="deep-research-agent",
            instructions="You are a helpful Agent that assists in researching scientific topics.",
            tools=deep_research_tool.definitions,
        )
        print(f"Created agent, ID: {agent.id}")

        # Create thread for communication
        thread = agents_client.threads.create()
        print(f"Created thread, ID: {thread.id}")

        user_content = "Research data regarding the investment in renewable energy, energy capacity, and energy consumption of countries in Sub-Saharan Africa"
        last_message_id = None
        while True:
            message = agents_client.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_content,
            )
            print(f"Created message, ID: {message.id}")

            print("Start processing the message... this may take a few minutes to finish. Be patient!")
            run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)
            agent_response = None
            while run.status in ("queued", "in_progress"):
                time.sleep(1)
                run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
                last_message_id, agent_response = fetch_and_print_new_agent_response(
                    thread_id=thread.id,
                    agents_client=agents_client,
                    last_message_id=last_message_id,
                )
                print(f"Run status: {run.status}")

            print(f"Run finished with status: {run.status}, ID: {run.id}")

            if run.status == "failed":
                print(f"Run failed: {run.last_error}")
                break

            # 让用户每次都决定是否继续补充或退出
            if agent_response:
                user_decision = input("是否需要补充说明？(y/n，输入n将写入总结并退出)：").strip().lower()
                if user_decision == "y":
                    user_content = input("请输入你的补充说明：")
                    continue
                else:
                    create_research_summary(agent_response)
                    break

        # Clean-up and delete the agent once the run is finished.
        # NOTE: Comment out this line if you plan to reuse the agent later.
        # agents_client.delete_agent(agent.id)
        # print("Deleted agent")