import pandas as pd
import requests
import streamlit as st


class CardGetter:
    def __init__(self):
        self.root = "https://api.scryfall.com/cards"

    def build_url(self, string):
        print(f"{self.root}/{string}")

        return f"{self.root}/{string}"

    def check_field(self, api_result, field_name):
        """Check if a field exists in the returned API request."""
        try:
            api_result[field_name]
            return True
        except KeyError:
            return False

    def get_random_card(self):
        url = self.build_url("random")
        result = self.query_api(url)

        return result

    def get_card_image(self, result, size="normal"):
        return result["image_uris"][size]

    # TODO: Handle fields nested under "card_faces"
    def format_result(self, result):

        if self.check_field(result, "card_faces"):
            formatted = {
                "image_uris": [
                    result["card_faces"][0]["image_uris"]["normal"],
                    result["card_faces"][1]["image_uris"]["normal"],
                ]
            }
        else:
            formatted = {
                "image_uris": [result["image_uris"]["normal"]],
            }

        formatted.update({"prices": result["prices"]})

        return formatted

    def query_api(self, url):
        try:
            result = requests.get(url).json()
        except:
            st.error("Something went wrong")

        return result

    def search_card(self, card_to_search):
        """Use the search API to look for a card."""
        url = self.build_url(f"named/?fuzzy={card_to_search}")
        result = self.query_api(url)
        # st.write(result)  # for debug
        return result

    def handle_result(self, result):
        if result["object"] != "card":
            page = PageView()
            page.render_error(result)
            return
        else:
            formatted = self.format_result(result)
            return formatted


class PageView:
    def create_elements(self, image=None):
        container = st.container()

        with container:
            self.search_bar()
            self.random_card()
            if image is not None:
                self.render_image(image)

    def render_error(self, result):
        st.write(result["details"])

    def render_image(self, image_uri):
        st.image(image_uri)

    def render_page(self):
        """Render a page with conditional elements."""
        self.create_elements()

    def render_price(self, prices):
        df = self._json_to_table(prices)
        with st.sidebar:
            st.table(df)

    def search_bar(self):
        with st.form("search_card"):
            card_to_search = st.text_input("Search for a Card by Name")
            submitted = st.form_submit_button("Search")
            if submitted:
                getter = CardGetter()
                searched_card = getter.handle_result(getter.search_card(card_to_search))
                if searched_card is not None:
                    image_uri = searched_card["image_uris"]
                    prices = searched_card["prices"]
                    self.render_image(image_uri)
                    self.render_price(prices)

    def random_card(self):
        with st.form("get_random_card"):
            st.text("Get a Random Card")
            submitted = st.form_submit_button("Random")
            if submitted:
                getter = CardGetter()
                random_card = getter.handle_result(getter.get_random_card())
                if random_card is not None:
                    image_uri = random_card["image_uris"]
                    prices = random_card["prices"]
                    self.render_image(image_uri)
                    self.render_price(prices)

    def _json_to_table(self, data):
        return pd.DataFrame.from_dict(data, orient="index")


def main():
    # Render web contents
    page = PageView()
    page.render_page()


if __name__ == "__main__":
    main()
