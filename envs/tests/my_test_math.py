import sys
import os

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取项目根目录的路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)

from envs.MATH import (
    Env,
    get_train_test_dataset,
    extract_groundtruth,
    judge_correct,
    extract_answer,
)

if __name__ == "__main__":
    from transformers import AutoTokenizer
    from reason.evaluation.evaluator import MathEvaluator, Task
    from reason.inference.lm_call import VLLMRemoteCaller
    from reason.inference.rm_call import DummyRewardModelCaller,RMRemoteCaller
    from reason.inference.rm_call import RewardModelBaseConfig,RemoteRewardModelConfig
 
    from reason.evaluation.methods import cot
    import jsonlines
    import tree
    import numpy as np
    from tqdm import tqdm
    _, ds = get_train_test_dataset()
    print(len(ds))
    print(ds[0])
    problem = ds[0]
    env = Env(
        config={
            "max_actions": 10,
            "max_length": 10,
            "stop_str": "The answer is ",
            "generation_config": {
                "max_new_tokens": 512,
                "temperature": 0.3,
                "top_p": 1.0,
                "top_k": 50,
            },
        },
        math_problems=[
            {
                "question": problem["question"],
                "answer": extract_groundtruth(problem["answer"]),
            }
        ],
        # llm_gen_fn=VLLMRemoteCaller("Qwen2.5-Math-1.5B-Instruct", "http://0.0.0.0:28777"),
        llm_gen_fn=VLLMRemoteCaller("mistral-7b-sft", "http://0.0.0.0:28777"),
        reset=False,
    )

    env.reset(update_legal_action=True)
    print('*************************')
    print("env.legal_actions: ", env.legal_actions)
    print('*************************')
    env.step(action=env.legal_actions[0]["action"])
    print("env.get_state():", env.get_state())
    print('*************************')
    print("env.question: ", env.question)
    print('*************************')
    print("env.answer:", env.answer)
    print('*************************')

    task = Task("MATH")

    # rm_config = RewardModelBaseConfig(
    #     step_tag='prm_step_tag', format_str='prm_format_str'
    # )  
    rm_config = RewardModelBaseConfig(
        step_tag="ки\n",
        format_str="{question} {answer}",
        model_name='math-shepherd-mistral-7b-prm',
        controller_addr='http://0.0.0.0:30011',
    )
    rm_call = RMRemoteCaller(rm_config)    
    evaluator = MathEvaluator("MATH",
                              VLLMRemoteCaller("mistral-7b-sft", 'http://0.0.0.0:28777'),
                              rm_call)
    
    # res = env.step(action=f"The answer is: {problem['answer']} ки", update_legal_action=False)
    # print(res)
    print(env.get_state())

    a = "Step 1: To convert from rectangular coordinates to polar coordinates, we can use the formulas:\n$r = \\sqrt{x^2 + y^2}$ and $\\theta = \\arctan\\left(\\frac{y}{x}\\right)$. ки\nStep 2: In this case, $x = 0$ and $y = 3$. ки\nStep 3: Plugging these values into the formulas, we get:\n$r = \\sqrt{0^2 + 3^2} = 3$ and $\\theta = \\arctan\\left(\\frac{3}{0}\\right)$. ки\nStep 4: Since $\\frac{3}{0}$ is undefined, we need to find an alternative way to find $\\theta$. ки\nStep 5: We know that the point $(0,3)$ lies on the positive y-axis, so $\\theta = \\frac{\\pi}{2}$. ки\nStep 6: Therefore, the polar coordinates of the point $(0,3)$ are $\\boxed{(3,\\frac{\\pi}{2})}$. The answer is: (3,\\frac{\\pi}{2}) ки"
    g = "\\left( 3, \\frac{\\pi}{2} \\right)"
