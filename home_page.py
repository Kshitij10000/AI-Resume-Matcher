import streamlit as st 

def home_content():
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
        h1, h2 {
            font-size: 32px; /* Adjusted size for better visibility */
            color: #4a69bd; /* Deep blue for the headings */
            margin-bottom: 20px; /* Space below the headings */
            text-align: center; /* Center align the headings */
        }

        /* Subheader styling */
        h3 {
            font-size: 24px;
            color: #333;
            margin-top: 10px; /* Spacing before subheader */
            margin-bottom: 10px; /* Spacing after subheader */
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
        <h1>Welcome to Nirmaan.HR: Where Talent Meets Opportunity</h1>
        <p>Imagine a world where recruitment isn't a battlefield, but an elegant dance. You, the visionary leader, outlining the role you need to build your dream team. And Nirmaan.HR, your AI-powered partner, waltzing across the vast talent landscape, handpicking the perfect candidates who move in perfect rhythm with your vision.</p>
        <p>We believe in the power of human potential, and the alchemy that occurs when the right person meets the right opportunity. That's why we've meticulously crafted Nirmaan.HR, an online platform that goes beyond resumes. We leverage the brilliance of artificial intelligence to understand your needs, translating your job descriptions into a symphony of qualifications.</p>
        <h2>Here at Nirmaan.HR, you don't just fill roles, you cultivate a symphony of talent.</h2>
        <h3>Ready to craft your masterpiece?</h3>
        <ul>
            <li><strong>Explore our AI-powered matching:</strong> Let our algorithms become your personal headhunter, identifying candidates who resonate with your vision.</li>
            <li><strong>Craft bespoke skill assessments:</strong> Go beyond the resume and delve deeper. Design customized tests that truly evaluate the potential of each candidate.</li>
            <li><strong>Experience effortless recruitment:</strong> Spend less time wading through resumes and more time building a team that inspires you.</li>
            <li><strong>Send direct emails:</strong> Notify selected candidates directly from the application, ensuring a seamless communication process.</li>
            <li><strong>Interactive chat with historical data:</strong> Engage in conversations with previous data without needing to search manually, making your recruitment process as efficient as possible.</li>
        </ul>
        <p><strong>Nirmaan.HR. Where recruitment becomes an art form, and your dream team becomes a reality.</strong></p>
        <h2>Let the symphony begin.</h2>
    </div>
    """, unsafe_allow_html=True)
