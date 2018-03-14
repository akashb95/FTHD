class Pagination:
    def __init__(self, curr_page, max_page, left=2, right=2):
        """
        Initialise pagination
        :param curr_page: current page number
        :param max_page: maximum number of pages needed for results
        :param left: number of previous search pages whose links are to be displayed
        :param right: number of following search pages whose links are to be displayed
        """
        self.current_page = int(curr_page)
        self.max_page = int(max_page)
        self.num_previous_pages = int(left)
        self.num_next_pages = int(right)
        self.pages = []
        return

    def has_previous(self):
        return self.current_page > 1

    def has_next(self):
        return self.current_page < self.max_page

    def paginate(self):
        """
        :return: An array of page numbers to be shown.
        """
        if self.has_previous():
            self.pages.extend(list(range(max(self.current_page - self.num_previous_pages, 1),
                                         self.current_page)))

        self.pages.append(self.current_page)

        if self.has_next():
            self.pages.extend(list(range(self.current_page + 1,
                                         min(self.current_page + self.num_next_pages + 1, self.max_page + 1))))

        return self.pages

