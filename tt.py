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
    root = Node(action="Root")
    node_pattern = re.compile(r"Choose child:\s*([\s\S]*?)(?=\n\n)", re.DOTALL)
    
    lines = log_content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # print(f"Processing line: {line}")  # 调试信息
        
        # 检查是否是 ucb_score 行
        if "ucb_score" in line:
            # 处理当前行和下一行
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                combined_line = line + " " + next_line  # 合并行
                match = node_pattern.search(combined_line)
                if match:
                    ucb_score, action, value, prior = match.groups()
                    action = action.strip().replace('\n', ' ')
                    node_id = str(hash(action))
                    print("Get UCB line.")  # 确认匹配成功
                    # 处理匹配到的内容
                    # ...
            i += 2  # 跳过下一行
        else:
            i += 1  # 继续处理下一行

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
    # visualize_mcts_tree(root)
    
    # print("MCTS树已生成，请查看 mcts_tree.png")

if __name__ == "__main__":
    main()