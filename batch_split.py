import os

max_chunk_size = 200 * 1024 * 1024  # 200MB
input_file = 'vision_batch_job.jsonl'
output_dir = 'batch_splits'
os.makedirs(output_dir, exist_ok=True)

chunk_num = 1
current_chunk_size = 0
chunk_lines = []

with open(input_file, 'rb') as f:
    for line in f:
        if current_chunk_size + len(line) > max_chunk_size:
            output_path = os.path.join(output_dir, f'vision_batch_part_{chunk_num}.jsonl')
            with open(output_path, 'wb') as chunk_file:
                chunk_file.writelines(chunk_lines)
            print(f'✅ 分割完了: {output_path}')
            chunk_num += 1
            chunk_lines = []
            current_chunk_size = 0
        chunk_lines.append(line)
        current_chunk_size += len(line)

# 最後の残りを書き出し
if chunk_lines:
    output_path = os.path.join(output_dir, f'vision_batch_part_{chunk_num}.jsonl')
    with open(output_path, 'wb') as chunk_file:
        chunk_file.writelines(chunk_lines)
    print(f'✅ 分割完了: {output_path}')