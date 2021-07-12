import streamlit as st

class AppPage:

    def __init__(self) -> None:
        self.pages = []

    def define_page(self, page_name, page_handler) -> None:
        """
        Adds a new page to the pages list.
        :param page_name: The name of the page to add.
        :param page_handler: The handler of the page to add.
        :return: None
        """
        self.pages.append({
            'pageName': page_name,
            'pageHandler': page_handler,
        })

    def build_page(self) -> None:
        """
        Builds a page by executing the build_page
        function of each page in the pages folder as it's selected.
        :return: None
        """

        st.sidebar.image('./assets/Obj1.png', width=300)
        page = st.sidebar.radio('Please select from the following:', self.pages, format_func=lambda page_instance: page_instance['pageName'])

        # run the app function
        page['pageHandler']()
