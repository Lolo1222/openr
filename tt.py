import json
import re

def extract_actions(log_file, output_file):
    with open(log_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line_number, line in enumerate(infile, start=1):
            line = line.strip()
            if not line:
                continue
            if "Candidate action" in line:
                try:
                    # Use regex to extract the JSON part
                    match = re.search(r"\{.*\}", line)
                    if match:
                        json_str = match.group(0)
                        # Replace single quotes with double quotes for keys and values
                        json_str = json_str.replace("'", '"')
                        # Ensure that the keys are properly formatted
                        json_str = re.sub(r'(\w+):', r'"\1":', json_str)
                        data = json.loads(json_str)
                        if isinstance(data, dict) and 'action' in data:
                            outfile.write(data['action'] + '\n')
                        # else:
                        #     print(f"Line {line_number}: No 'action' key found or not a dict: {line}")
                    # else:
                    #     print(f"Line {line_number}: No JSON object found in line: {line}")
                except json.JSONDecodeError as e:
                    # print(f"Line {line_number}: JSONDecodeError: {e}, Line: {line}")
                    continue
            # else:
            #     print(f"Line {line_number}: Not a candidate action line: {line}")

if __name__ == "__main__":
    log_file = "logs_terminal/mathtrain6500_simple_mcts_qwen_mprm_width10.log"  # Replace with your log file path
    # log_file = "logs_terminal/beam_search_math500.log"  # Replace with your log file path
    output_file = "actions.txt"  # Replace with your desired output file path
    extract_actions(log_file, output_file)
    print(f"Actions extracted and saved to {output_file}")