import os
import networkx as nx

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from PIL import Image

from .file_manager import load_graph_files, prob_line_parser, find_prob_file_by_node
from .data_helper import get_node_name_from_pos_abs, get_node_pos_from_name_abs

def generate_pictures(root_dir="../"):
    map_info, _ = load_graph_files(env_path=root_dir, map_lookup="L")
    prob_prefix = "data/prob/"
    vis_save_path = "vis/"
    files = os.listdir(root_dir + prob_prefix)
    files_txt = [i for i in files if i.endswith('.txt')]
    for f in files_txt:
        file = open(root_dir + prob_prefix + f, 'r')
        lines = file.readlines()

        # predetermined colors
        col_lookup = ['grey', 'red', 'yellow', 'green', 'blue']
        col_norm = colors.BoundaryNorm(boundaries=[0, 1e-16, 0.1, 0.5, 0.95, 1.1], ncolors=len(col_lookup))
        col_idx = [0] * len(map_info.n_info)
        for line in lines:
            _, _, n_row, n_col, f_prob = prob_line_parser(line)
            n_idx = map_info.get_index_by_name(get_node_name_from_pos_abs((n_row, n_col)))
            col_idx[n_idx - 1] = col_norm(f_prob)
        col_map = [col_lookup[col_idx[i]] for i in range(len(col_idx))]
        nx.draw_networkx(map_info.g_acs, map_info.n_info, node_color=col_map, node_size=150, font_size=6, edge_color="grey", arrows=False)
        plt.savefig(root_dir + vis_save_path + f[:-4] + ".png", dpi=300)
    plt.close()


def generate_picture_by_index(root_dir="../", index_n=42, ext_col_lookup=None, ext_col_boundaries=None):
    map_info, _ = load_graph_files(env_path=root_dir, map_lookup="L")
    prob_prefix = "data/prob/"

    node_name = map_info.get_name_by_index(index_n)
    node_row, node_col = get_node_pos_from_name_abs(node_name)

    col_lookup = ['grey', 'red', 'yellow', 'green', 'cyan'] if ext_col_lookup is None else ext_col_lookup
    col_boundaries = [0, 1e-16, 0.1, 0.5, 0.99, 1.1] if ext_col_boundaries is None else ext_col_boundaries
    col_norm = colors.BoundaryNorm(boundaries=col_boundaries, ncolors=len(col_lookup))

    files = find_prob_file_by_node(root_dir + prob_prefix, node_row, node_col)
    for i, f in enumerate(files):
        file = open(root_dir + prob_prefix + f, 'r')
        lines = file.readlines()
        # predetermined colors
        
        col_idx = [0] * len(map_info.n_info)
        for line in lines:
            _, _, n_row, n_col, f_prob = prob_line_parser(line)
            n_idx = map_info.get_index_by_name(get_node_name_from_pos_abs((n_row, n_col)))
            col_idx[n_idx - 1] = col_norm(f_prob)
        col_map = [col_lookup[col_idx[i]] for i in range(len(col_idx))]
        nx.draw_networkx(map_info.g_acs, map_info.n_info, node_color=col_map, node_size=100, font_size=5, edge_color="grey", arrows=False)
        plt.savefig(f"{i}.png", dpi=200, transparent=True)
    plt.close()


def load_picture_by_row_col(node_row=6, node_col=3, root_dir="../"):
    vis_path = "vis/"
    files_png = find_prob_file_by_node(root_dir + vis_path, node_row, node_col, file_type="png")
    return files_png


def plotout(map_dir):
    fig = plt.figure(frameon=False, figsize=(12, 9), facecolor='none')
    plt.axis('off')
    map_info, _ = load_graph_files(env_path=map_dir, map_lookup="L")
    col_map = ["gold"] * len(map_info.n_info)
    nx.draw_networkx(map_info.g_acs, map_info.n_info, node_color=col_map, node_size=200, font_size=6, edge_color="grey", arrows=False)
    # plt.show()
    plt.savefig("map_act.png", dpi=200, transparent=True)
    # nx.draw_networkx(map_info.g_vis, map_info.n_info, node_color=col_map, node_size=300, edge_color="grey", arrows=False)
    # plt.savefig("map_vis.png", dpi=300)
    # map_info.save_plots_to_file("acs","vis")
    plt.close()

if __name__ == "__main__":
    root_dir = "../"
    plotout(root_dir)