import pandas as pd
import requests
import streamlit as st


class CardGetter:
    def __init__(self):
        self.root = 'https://api.scryfall.com/cards'

    def build_url(self, string):
        print(f'{self.root}/{string}')

        return f'{self.root}/{string}'

    def check_field(self, api_result, field_name):
        """Check if a field exists in the returned API request."""
        try:
            api_result[field_name]
            return True
        except KeyError: 
            return False

    def get_random_card(self):
        url = self.build_url('random')
        result = self.query_api(url)
        card = self.format_result(result)

        return card
    
    def get_card_image(self, result, size='normal'):
        return result['image_uris'][size]


    def format_result(self, result):

        formatted = {
            'card_name': result['name'],
            'mana_cost': result['mana_cost'],
            'type_line': result['type_line'],            
            'keywords': result['keywords'],
            'rarity': result['rarity'],
            'prices': result['prices'],
            'image_uri': result['image_uris']['normal'],
        }

        # Only need to check once since if a card doesn't have power
        # it won't have toughness
        if self.check_field(result, 'power'):
            formatted.update({
                'power':     result['power'],
                'toughness': result['toughness']
            })

        # Lands don't have mana costs
        if self.check_field(result, 'mana_cost'):
            formatted.update({
                'mana_cost': result['mana_cost']
            })

        # Basic lands might not have oracle text?
        if self.check_field(result, 'oracle_text'):
            formatted.update({
                'description': result['oracle_text']
            })

        if self.check_field(result, 'flavor_text'):
            formatted.update({
                'flavor_text': result['flavor_text']
            })

        return formatted
    
    def query_api(self, url):
        try:
            result = requests.get(url).json()
        except:
            st.error('Something went wrong')

        return result

    def search_card(self, card_to_search):
        """Use the search API to look for a card."""
        url = self.build_url(f'named/?fuzzy={card_to_search}')
        result = self.query_api(url)
        # st.write(result)  # for debug
        if result['object'] != 'card':
            st.error(result)
            st.stop()
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
        with st.form('search_card'):
            card_to_search = st.text_input('Search for a Card by Name')
            submitted = st.form_submit_button('Search')
            if submitted:
                getter = CardGetter()
                searched_card = getter.search_card(card_to_search)
                image_uri = searched_card['image_uri']
                prices = searched_card['prices']
                self.render_image(image_uri)
                self.render_price(prices)
    
    def random_card(self):
        with st.form('get_random_card'):
            st.text('Get a Random Card')
            submitted = st.form_submit_button('Random')
            if submitted:
                getter = CardGetter()
                random_card = getter.get_random_card()
                image_uri = random_card['image_uri']
                prices = random_card['prices']
                self.render_image(image_uri)
                self.render_price(prices)
    
    def _json_to_table(self, data):
        return pd.DataFrame.from_dict(
            data, 
            orient='index'
        )
                

def main():
    # Render web contents
    page = PageView()
    page.render_page()


if __name__ == '__main__':
    main()