import streamlit as st
import time
import random

# --- 1. Game Configuration ---

# Define the three enigmas, their solutions, and hints
RIDDLES = [
    {
        "title": "🎩 Enigma 1: The Curse of the Confounding Hats",
        "subtitle": "D1 - The Logic of Survival",
        "story": "Your defense committee, disguised as a nefarious organization, has forced a group of ten researchers into a deadly statistics problem. To save them, you must find the loophole.",
        "riddle": """
            <div class="puzzle-container">
                <div class="puzzle-header">
                    <h3>🧠 The Scenario</h3>
                </div>
                <div class="puzzle-content">
                    <p>Ten prisoners (1-10, front to back) are lined up single-file. Each wears a black or white hat. They see all hats in front but not their own. Starting from the back (Prisoner 10), each must call out 'Black' or 'White'. A correct guess lives; a wrong guess dies. They can only communicate using their guess. They may plan a strategy <em>now</em>.</p>
                </div>
                <div class="puzzle-question">
                    <h4>🎯 Your Task</h4>
                    <p>What is the maximum number of prisoners who can guarantee their survival?</p>
                </div>
            </div>
        """,
        "answer": 9,
        "digit_index": 0,
        "hint": "Think about parity and how the first person can encode information for the rest.",
        "difficulty": "🧠 Advanced Logic"
    },
    {
        "title": "🔢 Enigma 2: The Hex of the High-Order Shift",
        "subtitle": "D2 - The Mathematical Mystery",
        "story": "Your data set has been corrupted! A malicious process has shifted the last element of a 6-digit number to the front, creating a new number exactly three times the original. Unravel this arithmetic mystery to find the original final digit.",
        "riddle": """
            <div class="puzzle-container">
                <div class="puzzle-header">
                    <h3>🔍 The Riddle</h3>
                </div>
                <div class="puzzle-content">
                    <p>A six-digit number is such that if you move its last digit to the front, you get a number that is exactly three times the original.</p>
                    <div class="math-example">
                        <p><strong>Example:</strong> If original = 123456, then shifted = 612345</p>
                        <p>But in our case: shifted = 3 × original</p>
                    </div>
                </div>
                <div class="puzzle-question">
                    <h4>🎯 Your Task</h4>
                    <p>What is the numerical value of the original number's last digit?</p>
                </div>
            </div>
        """,
        "answer": 7,
        "digit_index": 1,
        "hint": "Set up the equation: if the original number is ABCDEF, then FABCDE = 3 × ABCDEF.",
        "difficulty": "🔢 Mathematical Reasoning"
    },
    {
        "title": "💰 Enigma 3: The Division of Logs",
        "subtitle": "D3 - The Fair Share Dilemma",
        "story": "The Sage, being a fair and rational person, asks you to settle a financial dispute between three friends. Do not trust your first impulse; calculate the true value of their contributions.",
        "riddle": """
            <div class="puzzle-container">
                <div class="puzzle-header">
                    <h3>⚖️ The Riddle</h3>
                </div>
                <div class="puzzle-content">
                    <p>Three friends—Alice, Bob, and Carol—were making a fire. Alice put 3 logs into the fire, and Bob added 5 logs. Carol, who had no firewood, paid them $8 as her share.</p>
                    <div class="math-example">
                        <p><strong>Total logs:</strong> 3 + 5 = 8 logs</p>
                        <p><strong>Carol's share:</strong> $8 (for her equal 1/3 share of the fire)</p>
                    </div>
                </div>
                <div class="puzzle-question">
                    <h4>🎯 Your Task</h4>
                    <p>How much money (in whole dollars) must Bob receive?</p>
                </div>
            </div>
        """,
        "answer": 7,
        "digit_index": 2,
        "hint": "Since Carol paid $8 for her 1/3 share, the full fire cost $24. At $3 per log, Bob contributed $15 but only consumed $8 worth, so he should receive $7.",
        "difficulty": "💰 Fair Division Logic"
    }
]

# --- 2. Streamlit Setup and State Initialization ---

def initialize_state():
    """Initializes session state variables for the game."""
    if 'current_riddle_index' not in st.session_state:
        st.session_state.current_riddle_index = 0
    if 'collected_digits' not in st.session_state:
        st.session_state.collected_digits = [None, None, None]
    if 'game_finished' not in st.session_state:
        st.session_state.game_finished = False
    if 'show_hint' not in st.session_state:
        st.session_state.show_hint = False
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    if 'celebration_triggered' not in st.session_state:
        st.session_state.celebration_triggered = False

# Apply sophisticated styling with animations and modern design
st.set_page_config(
    layout="centered", 
    page_title="The PhD Enigmas", 
    page_icon="🎓",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    
    /* Animated Background */
    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.3) 0%, transparent 50%);
        animation: backgroundShift 20s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes backgroundShift {
        0%, 100% { transform: translateX(0) translateY(0); }
        25% { transform: translateX(-20px) translateY(-10px); }
        50% { transform: translateX(20px) translateY(10px); }
        75% { transform: translateX(-10px) translateY(20px); }
    }
    
    /* Main Header */
    .main-header {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease-in-out infinite;
        padding: 20px 0;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
        margin-bottom: 10px;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .subheader {
        text-align: center;
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 40px;
        font-weight: 500;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Puzzle Container */
    .puzzle-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: slideInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .puzzle-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .puzzle-header h3 {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .puzzle-content {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #4f46e5;
        position: relative;
    }
    
    .puzzle-content p {
        color: #4a5568;
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 0;
    }
    
    .math-example {
        background: rgba(79, 70, 229, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
        border: 1px solid rgba(79, 70, 229, 0.2);
    }
    
    .math-example p {
        margin: 5px 0;
        font-family: 'Courier New', monospace;
        color: #553c9a;
    }
    
    .puzzle-question {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .puzzle-question h4 {
        margin: 0 0 10px 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .puzzle-question p {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Code Display */
    .code-display-box {
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        border: 3px solid #4f46e5;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 40px 0;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .code-display-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(79, 70, 229, 0.1) 50%, transparent 70%);
        animation: codeGlow 2s ease-in-out infinite;
    }
    
    @keyframes codeGlow {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.8; }
    }
    
    .code-display {
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: 1rem;
        font-family: 'Courier New', monospace;
        position: relative;
        z-index: 1;
    }
    
    .digit-unsolved {
        color: #4a5568;
        text-shadow: 0 0 10px rgba(74, 85, 104, 0.5);
        animation: pulse 2s ease-in-out infinite;
    }
    
    .digit-solved {
        color: #48bb78;
        text-shadow: 0 0 20px rgba(72, 187, 120, 0.8);
        animation: solvedGlow 1s ease-out;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
    }
    
    @keyframes solvedGlow {
        0% { 
            transform: scale(1);
            text-shadow: 0 0 20px rgba(72, 187, 120, 0.8);
        }
        50% { 
            transform: scale(1.2);
            text-shadow: 0 0 30px rgba(72, 187, 120, 1);
        }
        100% { 
            transform: scale(1);
            text-shadow: 0 0 20px rgba(72, 187, 120, 0.8);
        }
    }
    
    /* Progress Indicators */
    .progress-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 30px 0;
    }
    
    .progress-dot {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.5);
        transition: all 0.3s ease;
    }
    
    .progress-dot.active {
        background: #4f46e5;
        border-color: #4f46e5;
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.6);
        animation: progressPulse 1.5s ease-in-out infinite;
    }
    
    .progress-dot.completed {
        background: #48bb78;
        border-color: #48bb78;
        box-shadow: 0 0 20px rgba(72, 187, 120, 0.6);
    }
    
    @keyframes progressPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input Styling */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(79, 70, 229, 0.3);
        border-radius: 15px;
        padding: 15px;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.3);
        outline: none;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        border-radius: 15px;
        border: none;
        color: white;
        font-weight: 600;
        animation: successSlide 0.5s ease-out;
    }
    
    .stError {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        border-radius: 15px;
        border: none;
        color: white;
        font-weight: 600;
        animation: errorShake 0.5s ease-out;
    }
    
    @keyframes successSlide {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes errorShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    /* Celebration Effects */
    .celebration {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1000;
    }
    
    .confetti {
        position: absolute;
        width: 10px;
        height: 10px;
        background: #ff6b6b;
        animation: confettiFall 3s linear infinite;
    }
    
    @keyframes confettiFall {
        0% {
            transform: translateY(-100vh) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }
    
    /* Hint System */
    .hint-container {
        background: linear-gradient(135deg, #fef5e7 0%, #fed7aa 100%);
        border: 2px solid #f6ad55;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        animation: hintSlide 0.5s ease-out;
    }
    
    @keyframes hintSlide {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hint-container h4 {
        color: #c05621;
        margin: 0 0 10px 0;
        font-size: 1.2rem;
    }
    
    .hint-container p {
        color: #744210;
        margin: 0;
        font-style: italic;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .code-display {
            font-size: 2.5rem;
            letter-spacing: 0.5rem;
        }
        
        .puzzle-container {
            padding: 20px;
        }
    }
    </style>
""", unsafe_allow_html=True)


# --- 3. Core Game Logic ---

def check_answer():
    """Checks the user's input against the current riddle's answer."""
    current_index = st.session_state.current_riddle_index

    # Check if the game is finished
    if current_index >= len(RIDDLES):
        return

    try:
        user_answer = int(st.session_state.user_input)
    except ValueError:
        st.error("Please enter a valid numerical answer.")
        return

    riddle = RIDDLES[current_index]
    st.session_state.attempts += 1

    if user_answer == riddle["answer"]:
        # Success animation and sound
        st.success(f"🎉 Brilliant! The digit D{current_index + 1} is {riddle['answer']}!")
        
        # Store the solved digit
        st.session_state.collected_digits[riddle["digit_index"]] = riddle["answer"]
        
        # Reset hint state for next puzzle
        st.session_state.show_hint = False

        # Advance the game state
        st.session_state.current_riddle_index += 1

        if st.session_state.current_riddle_index >= len(RIDDLES):
            st.session_state.game_finished = True
            st.session_state.celebration_triggered = True
    else:
        st.error(f"❌ Not quite right. Attempt #{st.session_state.attempts}. Think deeper about the logic!")
        st.session_state.show_hint = True


def display_game_interface():
    """Renders the current riddle and the interactive input form."""
    current_index = st.session_state.current_riddle_index

    if st.session_state.game_finished:
        display_celebration()
        return

    # Display current riddle
    riddle = RIDDLES[current_index]

    # Progress indicator
    display_progress_indicators()

    st.markdown(f"## {riddle['title']}")
    st.markdown(f"### {riddle['subtitle']}")
    st.markdown(f"<p style='color: rgba(255, 255, 255, 0.8); font-style: italic; margin-bottom: 20px; font-size: 1.1rem;'>\"{riddle['story']}\"</p>", unsafe_allow_html=True)
    
    # Difficulty indicator
    st.markdown(f"<div style='text-align: center; margin: 10px 0;'><span style='background: rgba(255, 255, 255, 0.2); padding: 5px 15px; border-radius: 20px; color: white; font-weight: 500;'>{riddle['difficulty']}</span></div>", unsafe_allow_html=True)
    
    st.markdown(riddle["riddle"], unsafe_allow_html=True)

    # Hint system
    if st.session_state.show_hint:
        st.markdown(f"""
            <div class="hint-container">
                <h4>💡 Hint</h4>
                <p>{riddle['hint']}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Interactive input and submission
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.number_input("Enter Your Solution:", key="user_input", step=1, min_value=0, max_value=99999, 
                       help="Think carefully about the logic and mathematics involved!")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        st.button(f"🎯 Submit D{current_index + 1}", on_click=check_answer, type="primary", use_container_width=True)
    
    # Show attempts counter
    if st.session_state.attempts > 0:
        st.markdown(f"<p style='text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;'>Attempts: {st.session_state.attempts}</p>", unsafe_allow_html=True)


def display_progress_indicators():
    """Displays animated progress dots for the current puzzle."""
    current_index = st.session_state.current_riddle_index
    digits = st.session_state.collected_digits
    
    progress_html = '<div class="progress-container">'
    for i in range(3):
        if i < current_index or digits[i] is not None:
            progress_html += '<div class="progress-dot completed"></div>'
        elif i == current_index:
            progress_html += '<div class="progress-dot active"></div>'
        else:
            progress_html += '<div class="progress-dot"></div>'
    progress_html += '</div>'
    
    st.markdown(progress_html, unsafe_allow_html=True)

def display_code_progress():
    """Renders the current state of the 3-digit code with enhanced visuals."""
    digits = st.session_state.collected_digits
    code_str = ""
    
    # Format the digits with appropriate color classes
    for i, digit in enumerate(digits):
        if digit is not None:
            code_str += f"<span class='digit-solved'>{digit}</span>"
        else:
            code_str += "<span class='digit-unsolved'>_</span>"
        if i < 2:  # Add space between digits
            code_str += " "

    # Calculate completion percentage
    solved_count = sum(1 for d in digits if d is not None)
    completion_percentage = (solved_count / 3) * 100

    st.markdown(f"""
        <div style='text-align: center; margin-top: 40px;'>
            <p style='font-size: 1.3rem; font-weight: 600; color: rgba(255, 255, 255, 0.9); margin-bottom: 10px;'>
                🔑 The Final Lock Combination
            </p>
            <p style='font-size: 1rem; color: rgba(255, 255, 255, 0.7); margin-bottom: 20px;'>
                Progress: {solved_count}/3 digits solved ({completion_percentage:.0f}%)
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class='code-display-box'>
            <div class='code-display'>
                {code_str}
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_celebration():
    """Displays the final celebration screen with confetti and statistics."""
    # Calculate completion time
    completion_time = time.time() - st.session_state.start_time
    minutes = int(completion_time // 60)
    seconds = int(completion_time % 60)
    
    # Confetti animation
    if st.session_state.celebration_triggered:
        confetti_html = '<div class="celebration">'
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff']
        for i in range(50):
            color = random.choice(colors)
            left = random.randint(0, 100)
            delay = random.uniform(0, 2)
            confetti_html += f'<div class="confetti" style="left: {left}%; background: {color}; animation-delay: {delay}s;"></div>'
        confetti_html += '</div>'
        st.markdown(confetti_html, unsafe_allow_html=True)
        st.session_state.celebration_triggered = False

    st.markdown("""
        <div style='text-align: center; padding: 40px 20px; background: rgba(255, 255, 255, 0.95); border-radius: 20px; margin: 20px 0;'>
            <h1 style='font-size: 3rem; color: #2d3748; margin-bottom: 20px;'>🎉 CONGRATULATIONS DR. MAHTA! 🎉</h1>
            <h2 style='font-size: 2rem; color: #6366f1; margin-bottom: 30px;'>From Kaiserslautern to SIXT Munich - Mission Accomplished!</h2>
            <p style='font-size: 1.3rem; color: #4a5568; margin-bottom: 20px;'>
                You have successfully solved all three enigmas and proven your intellectual prowess! 
                Your journey from the academic halls of Kaiserslautern to the innovation hub of SIXT Munich 
                has been nothing short of remarkable. Well done, Doctor!
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⏱️ Completion Time", f"{minutes}m {seconds}s")
    with col2:
        st.metric("🎯 Total Attempts", st.session_state.attempts)
    with col3:
        st.metric("🧠 Puzzles Solved", "3/3")

    # Final code reveal
    st.markdown("""
        <div style='text-align: center; margin: 30px 0;'>
            <h3 style='color: rgba(255, 255, 255, 0.9); font-size: 1.5rem; margin-bottom: 20px;'>
                🏆 The Sacred Code of Wisdom
            </h3>
        </div>
    """, unsafe_allow_html=True)

    final_code = "".join(str(d) for d in st.session_state.collected_digits)
    st.markdown(f"""
        <div class='code-display-box' style='border: 3px solid #48bb78; box-shadow: 0 0 30px rgba(72, 187, 120, 0.5);'>
            <div class='code-display' style='color: #48bb78; text-shadow: 0 0 30px rgba(72, 187, 120, 1);'>
                {final_code}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='text-align: center; margin: 30px 0;'>
            <p style='font-size: 1.2rem; color: rgba(255, 255, 255, 0.8); font-style: italic;'>
                "The code {final_code} shall forever be remembered as the key to Dr. Mahta's doctoral triumph! 
                From the research labs of Kaiserslautern to the tech innovation of SIXT Munich - 
                a journey of excellence and achievement!"
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Restart button
    if st.button("🔄 Play Again", type="secondary", use_container_width=True):
        # Reset all state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# --- 4. Main App Execution ---

def main():
    """Main function to run the Streamlit app."""
    initialize_state()

    # Main header with enhanced styling
    st.markdown("<p class='main-header'>🎓 Dr. Mahta's Doctoral Trials 🎓</p>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>🧠 From Kaiserslautern to SIXT Munich: Solve the Enigmas to Unlock Your Celebration Code 🧠</p>", unsafe_allow_html=True)

    # Add some atmospheric elements
    st.markdown("""
        <div style='text-align: center; margin: 20px 0;'>
            <p style='color: rgba(255, 255, 255, 0.7); font-style: italic; font-size: 1rem;'>
                "Congratulations Dr. Mahta! Your journey from the academic halls of Kaiserslautern 
                to the innovation hub of SIXT Munich has been remarkable. Now prove your intellectual prowess one final time!"
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Use columns to center the content
    col1, col2, col3 = st.columns([1, 6, 1])

    with col2:
        display_game_interface()
        if not st.session_state.game_finished:
            display_code_progress()

    # Footer
    st.markdown("""
        <div style='text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid rgba(255, 255, 255, 0.2);'>
            <p style='color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;'>
                🎓 Created for Dr. Mahta's Doctoral Celebration - Kaiserslautern to SIXT Munich 🎓
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
