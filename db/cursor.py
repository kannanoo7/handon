
from serializer import deserialize_row, ROW_SIZE
from pager import PAGE_SIZE

ROWS_PER_PAGE = PAGE_SIZE // ROW_SIZE


class Cursor:

    def __init__(self, table):

        self.table = table
        self.row_num = 0
        self.end_of_table = False

        if table.num_rows == 0:
            self.end_of_table = True
    
    def advance(self):

        self.row_num += 1

        if self.row_num >= self.table.num_rows:
            self.end_of_table = True

    
    def value(self):

        page_num = (self.row_num // ROWS_PER_PAGE) + 1
        row_offset = self.row_num % ROWS_PER_PAGE

        page = self.table.pager.get_page(page_num)

        start = row_offset * ROW_SIZE
        end = start + ROW_SIZE

        data = page[start:end]

        return deserialize_row(data)