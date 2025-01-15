import re
from graphviz import Digraph
from dataclasses import dataclass
from typing import Dict, Optional, List
import random
import textwrap
import copy

@dataclass
class Node:
    action: str
    value: float = 0.0
    prior: float = 0.0
    ucb_score: float = 0.0
    children: Dict[str, 'Node'] = None
    is_final_choice: bool = False
    
    def __post_init__(self):
        if self.children is None:
            self.children = {}

def parse_log(log_content: str) -> Node:
    # 创建根节点
    root = Node(action="Root")
    
    # 用于跟踪当前路径
    current_path = [root]
    
    # 更新正则表达式以匹配实际的日志格式
    candidate_pattern = re.compile(r"Candidate action \d+: (.+)")
    # candidate_pattern = re.compile(r"Candidate action \d+: \{'action': '([^']+)', 'prob': ([\d.]+)")
    # node_pattern = re.compile(r"ucb_score, child_tmp: ([\d.]+), action: (.+?), value: ([\d.]+), prior: ([\d.]+)")
    node_pattern = re.compile(
    r"ucb_score: ([\d.]+), action: ([\s\S]*?), value: ([\d.]+), prior: ([\d.]+)"  # 使 `.` 匹配换行符
)
    choose_pattern = re.compile(r"Choose child: (.+)")
    step_pattern = re.compile(r"Step ([\d.]+), choose next step:(.+)")
    simulate_pattern = re.compile(r"Simulate \d+")
    
    # 用于跟踪每一轮模拟
    current_simulation = 0
    current_parent = root
    previous_parent = current_parent
    real_parent = root
    
    for line in log_content.split('\n'):
        # 处理模拟开始
        simulate_match = simulate_pattern.search(line)
        if simulate_match:
            current_simulation += 1
            current_parent = previous_parent
            print(f"\nStarting simulation {current_simulation}...")
            continue
        
        # 处理最终选择的步骤
        step_match = step_pattern.search(line)
        if step_match:
            step, chosen_step = step_match.groups()
            chosen_step = chosen_step.strip().replace('\n', ' ')
            node_id = str(hash(chosen_step))
            current_parent = real_parent
            
            # 如果这个节点还不存在，创建它
            if node_id not in current_parent.children:
                print("error in step_match")
                # exit(-1)
            
            # 更新当前父节点为选择的节点
            current_parent = current_parent.children[node_id]
            previous_parent = current_parent
            real_parent = current_parent
            current_path.append(current_parent)
            print(f"\nChose final step: {chosen_step[:50]}...")
            continue
            
        # 处理候选动作
        candidate_match = candidate_pattern.search(line)
        if candidate_match:
            action = candidate_match.groups()[0]
            # action, prob = candidate_match.groups()
            action = action.strip().replace('\n', ' ')
            short_action = action[:100] + "..." if len(action) > 100 else action
            
            node_id = str(hash(action))
            
            if node_id not in current_parent.children:
                node = Node(
                    action=action,
                    # action=short_action,
                    # prior=float(prob)
                )
                current_parent.children[node_id] = node
                print(f"Added candidate: {short_action[:100]}...")
                # print(f"Added candidate under {current_parent.action[:100]}: {short_action[:100]}...")
        
        # 更新节点的UCB值
        match = node_pattern.search(line)
        if match:
            ucb_score, action, value, prior = match.groups()
            action = action.strip().replace('\n', ' ')
            node_id = str(hash(action))
            
            if node_id in current_parent.children:
                node = current_parent.children[node_id]
                node.value = float(value)
                node.ucb_score = float(ucb_score)
                node.prior = float(prior)
                print(f"Updated UCB for: {action[:100]}...")
            else:
                print("error in node match")
                # exit(-1)
        
        # 处理模拟过程中的选择
        choose_match = choose_pattern.search(line)
        if choose_match:
            chosen_action = choose_match.groups()[0]
            chosen_action = chosen_action.strip().replace('\n', ' ')
            node_id = str(hash(chosen_action))
            
            if node_id in current_parent.children:
                previous_parent = current_parent
                current_parent = current_parent.children[node_id]
                print(f"Simulation chose: {chosen_action[:100]}...")
    
    return root

def visualize_mcts_tree(root: Node, filename: str = "mcts_tree"):
    dot = Digraph(comment='MCTS Tree')
    
    # 设置图形属性
    dot.attr(
        rankdir='TB',
        size='50,50',
        dpi='300'
    )
    
    # 设置节点默认属性
    dot.attr('node', 
        shape='box',
        style='rounded,filled',
        fillcolor='lightgray',
        fontname='Arial',
        fontsize='10',
        margin='0.3'
    )
    
    def add_node(node: Node, parent_id: Optional[str] = None) -> str:
        nonlocal node_count
        node_id = f"node_{node_count}"
        node_count += 1
        
        # 创建节点标签
        if node.action == "Root":
            label = "Root"
            dot.attr('node', fillcolor='lightblue')
        else:
            # 限制文本长度并添加换行
            action_text = node.action[:100] + "..." if len(node.action) > 100 else node.action
            wrapped_action = textwrap.fill(action_text, width=40)
            
            label = f"{wrapped_action}\n"
            if hasattr(node, 'value') and node.value != 0.0:
                label += f"value: {node.value:.3f}\n"
                label += f"prior: {node.prior:.3f}\n"
                label += f"ucb: {node.ucb_score:.3f}"
            
            # 根据节点类型设置不同的颜色
            if node.is_final_choice:  # 突出显示最终选择的节点
                dot.attr('node', fillcolor='lightgreen', penwidth='2')
            elif node.ucb_score > 0:
                color = f"{0.3 + min(node.ucb_score * 0.7, 0.7):.2f} 0.3 1.0"
                dot.attr('node', fillcolor=color)
            else:
                dot.attr('node', fillcolor='lightgray')
        
        # 添加节点和边
        dot.node(node_id, label)
        if parent_id is not None:
            dot.edge(parent_id, node_id)
        
        # 递归处理子节点
        for child in sorted(node.children.values(), key=lambda x: getattr(x, 'ucb_score', 0), reverse=True):
            add_node(child, node_id)
            
        return node_id
    
    # 从根节点开始构建树
    node_count = 0
    add_node(root)
    
    # 保存图形
    dot.render(filename, format='png', cleanup=True)

def main():
    # 读取日志文件
    with open('logs_terminal/debug.log', 'r') as f:
        log_content = f.read()
    
    # 解析日志并创建树
    root = parse_log(log_content)
    
    # 可视化树
    visualize_mcts_tree(root)
    
    print("MCTS树已生成，请查看 mcts_tree.png")

if __name__ == "__main__":
    main()