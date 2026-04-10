from serializer import ROW_SIZE

NODE_TYPE_SIZE = 1
NUM_CELLS_SIZE = 4

LEAF_NODE_HEADER_SIZE = NODE_TYPE_SIZE + NUM_CELLS_SIZE

LEAF_NODE_CELL_SIZE = 4 + ROW_SIZE


def initialize_leaf_node(page):

    page[0] = 1

    page[1:5] = (0).to_bytes(4, "little")


def leaf_node_num_cells(page):

    return int.from_bytes(page[1:5], "little")


def set_leaf_node_num_cells(page, num):

    page[1:5] = num.to_bytes(4, "little")


def leaf_node_insert(page, key, row_data):

    num_cells = leaf_node_num_cells(page)

    start = LEAF_NODE_HEADER_SIZE + num_cells * LEAF_NODE_CELL_SIZE

    page[start:start+4] = key.to_bytes(4, "little")

    page[start+4:start+4+len(row_data)] = row_data

    set_leaf_node_num_cells(page, num_cells + 1)


def leaf_node_cell(page, cell_num):

    start = LEAF_NODE_HEADER_SIZE + cell_num * LEAF_NODE_CELL_SIZE

    key = int.from_bytes(page[start:start+4], "little")

    row = page[start+4:start+4+ROW_SIZE]

    return key, row