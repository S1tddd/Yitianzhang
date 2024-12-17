"""Class: CS230--Section 1
Name: Yitian Zhang
Description: Boston Airbnb Data Explorer with enhanced Streamlit features, visualizations, and Python capabilities.
I pledge that I have completed the programming assignment independently.
I have not copied the code from a student
or any source.
I have not given my code to any student."""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk


def filter_listings(df, neighbourhood, room_type=None):
    if room_type:
        filtered = df[(df['neighbourhood'] == neighbourhood) & (df['room_type'] == room_type)]
    else:
        filtered = df[df['neighbourhood'] == neighbourhood]
    return filtered, len(filtered)


def calculate_summary(df):
    return {
        'Number of Listings': len(df),
        'Average Price': df['price'].mean(),
        'Lowest Price': df['price'].min(),
        'Highest Price': df['price'].max()
    }


def clean_data(df):
    df['price'] = df['price'].fillna(0)
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
    return df


def get_unique_neighbourhoods(df, default_neighbourhood="All"):
    neighbourhoods = sorted(df['neighbourhood'].unique())
    return [default_neighbourhood] + neighbourhoods


listings_path = 'Final project/listings.csv'
neighbourhoods_path = 'Final project/neighbourhoods.csv'

listings_df = pd.read_csv(listings_path)
listings_df = clean_data(listings_df)

# ----- Sidebar Navigation -----
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Home", "Average Prices", "Top Neighborhoods", "Room Type Distribution", "Listings Map", "Price Summary","Survey"
])

# ----- Home Page -----
if page == "Home":
    st.title("Boston Airbnb Data Explorer")
    st.write("Use the sidebar to explore various visualizations and insights about Boston's Airbnb listings.")
    st.image("Final project/Boston_view_with_Airbnb_logo.jpg", caption="Explore Boston's Airbnb Listings", use_container_width=True)

# ----- Page 1: Average Prices -----
elif page == "Average Prices":
    st.title("Average Prices by Neighbourhood")
    avg_price = listings_df.groupby('neighbourhood')['price'].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    avg_price.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Average Prices by Neighbourhood')
    ax.set_ylabel('Average Price')
    st.pyplot(fig)

# ----- Page 2: Top Neighborhoods -----
elif page == "Top Neighborhoods":
    st.title("Top 5 Neighborhoods by Availability")
    availability = listings_df.groupby('neighbourhood')['availability_365'].mean().nlargest(5)

    fig, ax = plt.subplots(figsize=(8, 5))
    availability.plot(kind='bar', ax=ax, color='lightgreen')
    ax.set_title('Top 5 Neighborhoods by Availability')
    ax.set_ylabel('Average Availability (Days)')
    st.pyplot(fig)

# ----- Page 3: Room Type Distribution -----
elif page == "Room Type Distribution":
    st.title("Room Type Distribution")
    neighbourhoods = get_unique_neighbourhoods(listings_df)
    selected_neighbourhood = st.selectbox("Select a Neighbourhood", neighbourhoods)

    if selected_neighbourhood == "All":
        room_type_dist = listings_df['room_type'].value_counts()
    else:
        room_type_dist = listings_df[listings_df['neighbourhood'] == selected_neighbourhood]['room_type'].value_counts()

    fig, ax = plt.subplots()
    room_type_dist.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
    ax.set_ylabel('')
    st.pyplot(fig)

# ----- Page 4: Listings Map -----
elif page == "Listings Map":
    st.title("Map of Listings")
    neighbourhoods = get_unique_neighbourhoods(listings_df)
    selected_neighbourhood = st.selectbox("Select a Neighbourhood for Map", neighbourhoods)

    if selected_neighbourhood == "All":
        filtered_data = listings_df
    else:
        filtered_data, count = filter_listings(listings_df, selected_neighbourhood)
        st.write(f"Number of Listings: {count}")

    st.pydeck_chart(
        pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=filtered_data['latitude'].mean(),
                longitude=filtered_data['longitude'].mean(),
                zoom=11,
                pitch=50
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=filtered_data,
                    get_position='[longitude, latitude]',
                    get_radius=100,
                    get_color='[200, 30, 0, 160]',
                    pickable=True,
                    tooltip=True
                )
            ]
        )
    )

# ----- Page 5: Price Summary -----
elif page == "Price Summary":
    st.title("Price Summary")

    neighbourhoods = get_unique_neighbourhoods(listings_df)
    room_types = listings_df['room_type'].unique()
    selected_neighbourhood = st.selectbox("Select a Neighbourhood", neighbourhoods)
    selected_room_type = st.selectbox("Select a Room Type", room_types)

    if selected_neighbourhood == "All":
        filtered_data = listings_df[listings_df['room_type'] == selected_room_type]
    else:
        filtered_data, _ = filter_listings(listings_df, selected_neighbourhood, selected_room_type)

    summary = calculate_summary(filtered_data)

    st.write(f"**Price Summary for {selected_room_type} in {selected_neighbourhood}:**")
    for key, value in summary.items():
        if key == 'Number of Listings':  # No $ for Number of Listings
            st.write(f"- **{key}:** {value}")
        else:
            st.write(f"- **{key}:** ${value:.2f}")

# ----- Page 6: Price Survey -----
elif page == "Survey":
    st.title("Share Your Feedback!")
    st.write("We'd love to hear your thoughts on Boston Airbnb Data Explorer.")

    name = st.text_input("Your Name:")
    email = st.text_input("Your Email:")
    rating = st.slider("How would you rate this app? (1 = Poor, 5 = Excellent)", 1, 5, 3)
    comments = st.text_area("Additional Comments:")

    if st.button("Submit Feedback"):
        if name.strip() == "" or email.strip() == "":
            st.warning("Please fill in all the required fields (Name and Email).")
        else:
            subject = f"Survey Feedback from {name}"
            body = f"""
            Name: {name}
            Email: {email}
            Rating: {rating}/5
            Comments: {comments}
            """

            st.success("Thank you for your feedback! Your response has been submitted.")
            st.write("Feedback Summary:")
            st.write(body)

st.sidebar.info("Developed by Yitian Zhang | CS230 Section 1")
