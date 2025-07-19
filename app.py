import streamlit as st
import requests
import cohere

co = cohere.Client("WwkNe2VnB6hgVuV8K3o81evfD7SzEemDVmkox3Ng")



news_api_key = "7e872eb0f300406ea18c12ca35b2f041"

def summarize_text(text):
    if not text or len(text.split()) < 20:
        return "Not enough content to summarize."
    try:
        response = co.summarize(text=text, length='medium', format='paragraph')
        return response.summary
    except Exception as e:
        return f"Error: {e}"


st.title("📰 Simple News App")


country = st.text_input("🌍 Country code (e.g. us, fr, de):")
keyword = st.text_input("🔍 Keyword (e.g. economy, sport):")

if st.button("Get News"):
    if not country and not keyword:
        st.warning("Please enter either a country code or a keyword.")
    else:
        st.write(f"🔎 Searching news in **{country or 'all countries'}** about **{keyword or 'any topic'}**...")

        
        if country and keyword:
            url = f"https://newsapi.org/v2/everything?q={keyword}&language=en&sortBy=publishedAt&apiKey={news_api_key}"
        elif country:
            url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={news_api_key}"
        else:
            url = f"https://newsapi.org/v2/everything?q={keyword}&sortBy=publishedAt&apiKey={news_api_key}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                st.info("No news articles found.")
            else:
                for article in articles:
                    st.subheader(article.get("title", "No Title"))
                    st.write(article.get("description", "No description."))

                    
                    content = article.get("content") or article.get("description") or ""
                    summary = summarize_text(content)
                    
                    st.write("📝 Summary:")
                    st.success(summary)
                    st.markdown(f"[Read full article]({article.get('url')})")
                    st.write("---")
        else:
            st.error(f"❌ Failed to fetch news: {response.status_code}")
