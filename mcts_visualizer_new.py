import re
import networkx as nx
import matplotlib.pyplot as plt

def parse_log(log_file):
    """解析日志文件，提取 MCTS 树信息."""
    nodes = {}
    edges = []
    root_nodes = []
    current_root = None
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 匹配根节点
            root_match = re.search(r"Step \d+, choose next step:(.*)", line)
            if root_match:
                text = root_match.group(1).strip()
                if text not in nodes:
                    nodes[text] = {'type': 'root', 'ucb': 'N/A', 'value': 'N/A', 'prior': 'N/A'}
                if current_root:
                    edges.append((current_root, text))
                current_root = text
                root_nodes.append(text)
                continue
            
            # 匹配选择的子节点
            choose_match = re.search(r"Choose child: (.*)", line)
            if choose_match:
                text = choose_match.group(1).strip()
                if text not in nodes:
                    nodes[text] = {'type': 'choose', 'ucb': 'N/A', 'value': 'N/A', 'prior': 'N/A'}
                if current_root:
                    edges.append((current_root, text))
                current_root = text
                continue
            
            # 匹配候选动作
            candidate_match = re.search(r"Candidate action \d+: (.*)", line)
            if candidate_match:
                text = candidate_match.group(1).strip()
                if text not in nodes:
                    nodes[text] = {'type': 'candidate', 'ucb': 'N/A', 'value': 'N/A', 'prior': 'N/A'}
                if current_root:
                    edges.append((current_root, text))
                continue
            
            # 匹配 ucb_score, value, prior
            ucb_match = re.search(r"ucb_score: ([\d.]+), action: (.*), value: ([\d.]+), prior: ([\d.]+)", line)
            if ucb_match:
                ucb, action, value, prior = ucb_match.groups()
                action = action.strip()
                if action in nodes:
                    nodes[action]['ucb'] = ucb
                    nodes[action]['value'] = value
                    nodes[action]['prior'] = prior
    return nodes, edges, root_nodes

def create_graph(nodes, edges, root_nodes):
    """创建图形."""
    G = nx.DiGraph()
    for node, data in nodes.items():
        label = f"{node}\n(ucb: {data['ucb']}, value: {data['value']}, prior: {data['prior']})"
        G.add_node(node, label=label, type=data['type'])
    G.add_edges_from(edges)
    return G

def draw_graph(G, root_nodes):
    """绘制图形."""
    pos = nx.spring_layout(G, seed=42)
    
    node_colors = []
    for node in G.nodes(data=True):
        if node[1]['type'] == 'root':
            node_colors.append('lightblue')
        elif node[1]['type'] == 'choose':
            node_colors.append('lightgreen')
        else:
            node_colors.append('white')
    
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000, node_color=node_colors,
            font_size=8, font_weight='bold', arrowsize=10)
    
    plt.savefig('mcts_visualization.png')

if __name__ == "__main__":
    log_file = 'logs_terminal/debug.log'  # 替换为你的日志文件路径
    nodes, edges, root_nodes = parse_log(log_file)
    G = create_graph(nodes, edges, root_nodes)
    draw_graph(G, root_nodes)