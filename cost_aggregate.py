import json

VISION_PROMPT_RATE = 0.01  # $0.01 / 1K tokens（例）
COMPLETION_RATE = 0.03     # $0.03 / 1K tokens（例）
result_file = "batch_result.jsonl"

total_cost = 0
with open(result_file, 'r') as f:
    for line in f:
        data = json.loads(line)
        usage = data.get('response', {}).get('usage', {})
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)

        cost = (prompt_tokens / 1000) * VISION_PROMPT_RATE + (completion_tokens / 1000) * COMPLETION_RATE
        total_cost += cost

print(f"\n💰 総推定コスト: ${total_cost:.4f}")