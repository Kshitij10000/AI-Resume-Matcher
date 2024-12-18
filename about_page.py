import streamlit as st 

def about_page_content():
    st.markdown("""
    <style>
        /* Main content container styling */
        .main-container {
            width: 70%; /* Set width to 70% of the viewport width */
            margin: auto; /* Center the container */
            padding: 20px; /* Add some padding */
            box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Subtle shadow for depth */
            border-radius: 10px; /* Rounded corners */
            background-color: #ffffff; /* White background for readability */
        }

        /* Header styling */
        h1 {
            font-size: 36px; /* Large, clear font size */
            color: #4a69bd; /* Deep blue for the heading */
            margin-bottom: 20px; /* Space below the heading */
            text-align: center; /* Center align the heading */
        }

        /* Paragraph styling */
        p, li {
            color: #333; /* Dark gray for text, enhances readability */
            font-size: 18px; /* Slightly larger font for ease of reading */
            line-height: 1.6; /* Improved line spacing */
        }

        /* List item styling */
        li {
            margin-bottom: 10px; /* Spacing after each list item */
        }

        /* Strong (bold) text styling within paragraphs */
        strong {
            color: #2c3e50; /* Even darker shade for emphasis */
        }
    </style>

    <div class='main-container'>
        <h1>Build Your Dream Team. Effortlessly.</h1>
        <p>Nirmaan.HR harnesses the power of AI to find the perfect match for your open positions. Say goodbye to endless resumes and hello to a streamlined recruitment process with:</p>
        <ul>
            <li>AI-driven candidate matching - Focus on top talent, not a talent pool.</li>
            <li>Customizable skill assessments - Evaluate what truly matters.</li>
            <li>Effortless platform - More time building your team, less time screening.</li>
            <li>Send direct emails - Notify selected candidates directly from the application, ensuring a seamless communication process.</li>
            <li>Interactive chat with historical data - Engage in conversations with previous data without needing to search manually, making your recruitment process as efficient as possible.</li>
        </ul>
        <p><strong>Nirmaan.HR: Recruit smarter, not harder.</strong></p>
    </div>
    """, unsafe_allow_html=True)
