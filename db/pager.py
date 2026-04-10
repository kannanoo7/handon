import os

PAGE_SIZE = 4096


class Pager:

    def __init__(self, filename):

        self.filename = filename
        self.pages = {}

        if not os.path.exists(filename):
            open(filename, "wb").close()

        self.file = open(filename, "r+b")

        self.file_length = os.path.getsize(filename)

    def get_page(self, page_num):

        if page_num in self.pages:
            return self.pages[page_num]

        page = bytearray(PAGE_SIZE)

        num_pages = self.file_length // PAGE_SIZE

        if page_num < num_pages:

            self.file.seek(page_num * PAGE_SIZE)
            page[:] = self.file.read(PAGE_SIZE)

        self.pages[page_num] = page

        return page

    def flush(self, page_num):

        if page_num not in self.pages:
            return

        self.file.seek(page_num * PAGE_SIZE)

        self.file.write(self.pages[page_num])

    def close(self):

        for page_num in self.pages:
            self.flush(page_num)

        self.file.close()