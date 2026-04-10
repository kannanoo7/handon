from pager import Pager
from serializer import serialize_row, deserialize_row
from btree import *


class Table:

    def __init__(self, filename):

        self.pager = Pager(filename)

        root_page = self.pager.get_page(1)

        if self.pager.file_length == 0:

            initialize_leaf_node(root_page)

        self.root_page_num = 1

    def insert(self, row):

        page = self.pager.get_page(self.root_page_num)

        serialized = serialize_row(row)

        leaf_node_insert(page, row.id, serialized)

    def select(self):

        page = self.pager.get_page(self.root_page_num)

        num_cells = leaf_node_num_cells(page)

        rows = []

        for i in range(num_cells):

            key, row_data = leaf_node_cell(page, i)

            id, username = deserialize_row(row_data)

            rows.append((id, username))

        return rows

    def close(self):

        self.pager.close()