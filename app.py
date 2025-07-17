import streamlit as st
import requests

st.title("📰 Simple News App")

country = st.text_input("🌍 Country code (e.g. us, fr, de):")
keyword = st.text_input("🔍 Keyword (e.g. economy, sport):")

if st.button("Get News"):
    st.write(f"Searching news in **{country}** about **{keyword}**...")


    url = ('https://newsapi.org/v2/top-headlines?'
        f'country={country}&'
        'apiKey=7e872eb0f300406ea18c12ca35b2f041')

    response = requests.get(url)
    st.write(response)
    if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            if len(articles) == 0:
                st.info("No news articles found for this query.")
            else:
                for article in articles:
                    st.subheader(article.get("title", "No Title"))
                    st.write(article.get("description", ""))
                    st.markdown(f"[Read more]({article.get('url')})")
                    st.write("---")
    else:
            st.error(f"Failed to fetch news: {response.status_code}")



