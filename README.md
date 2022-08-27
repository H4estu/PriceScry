# PriceScry
An [extremely simple website](https://h4estu-pricescry-pricescry-0uc1b9.streamlitapp.com/) for tracking MTG card prices.

This is a [Streamlit Cloud](https://streamlit.io/cloud) app for looking up cards using the [Scryfall API](https://scryfall.com/docs/api). 


## How To Use
### Named Search
You can search for a card by name. The search by name feature does fuzzy matching, so you don't need to type the full name of the card in. For example, searching "Willowdusk" and "Willowdusk, Essence Seer" will return identical results. You will be prompted to change your search if the search text is too ambiguous (i.e. multiple cards were matched to the search string) or if no cards matched the search string.

### Pick a Random Card
Click the Random button for endless fun!

### Prices
Prices show up in the sidebar. The sidebar should open automatically on desktop, but on mobile you may have to click the right-facing chevron `>` in the upper left corner to see the card prices.
