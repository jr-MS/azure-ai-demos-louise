# Azure AI Agent Service · Browser Automation Demo

Use the Browser Automation tool to navigate websites, fill forms, click elements, and extract information—fully automated by an Azure AI Agent.

- Demo video: https://youtu.be/5mMgWdmig74
- Official docs: https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/browser-automation-samples

Please complete the prerequisites following the doc above.

## Query examples
Copy any of the prompts below into your agent thread. Tweak site URLs or criteria as needed.

### 1) Fill out a form
```text
Go to https://forms.cloud.microsoft/r/YfjkFtDcaJ and submit the following:
- Satisfaction: 5 stars
- Most frequently used feature: Model Deployment
- What you love: model catalog
- What you dislike: unknown system errors
```

### 2) Find dance classes
```text
From https://www.1milliondance.com/schedule/week show all available Master dance classes this weekend.
```

### 3) YouTube research
```text
Go to https://www.youtube.com, search for "AI Agent". Use filters to sort by most viewed.
Return the top 5 with: channel, title, short description, video length, link, views.
```

### 4) Blog aggregation (last 7 days)
```text
From https://devblogs.microsoft.com/foundry/ and https://techcommunity.microsoft.com/Blogs
find posts published in the last 7 days. Output: title, author, summary, publish date, views, likes, link.
Also save the results as a CSV file.
```

## Tips for better results
- Be explicit about the site, action, and the data fields you want back.
- Prefer one clear task per prompt. For multi-step tasks, list steps in order.
- When scraping tables or lists, specify output schema and format (e.g., CSV columns).



