import html
import streamlit as st
from calculator import safe_eval


st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --------------------------------
# Session state initialization
# --------------------------------
defaults = {
    "expression_widget": "",
    "current_result": "",
    "last_answer": "",
    "history": [],
    "angle_mode": "Radians",
    "theme_mode": "Dark",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------
# Helper functions
# --------------------------------
def format_result(value):
    """Format numeric output for cleaner display."""
    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.12g}"

    return str(value)


def append_value(value: str):
    """Append a value to the input expression."""
    st.session_state.expression_widget += value


def clear_expression():
    """Clear the expression and result."""
    st.session_state.expression_widget = ""
    st.session_state.current_result = ""


def delete_last():
    """Delete the last character."""
    st.session_state.expression_widget = st.session_state.expression_widget[:-1]


def insert_answer():
    """Insert the last answer into the expression."""
    if st.session_state.last_answer:
        st.session_state.expression_widget += str(st.session_state.last_answer)


def evaluate_expression():
    """Evaluate the current expression safely."""
    expression = st.session_state.expression_widget.strip()

    if not expression:
        st.session_state.current_result = "Please enter an expression."
        return

    try:
        result = safe_eval(expression, angle_mode=st.session_state.angle_mode)
        formatted = format_result(result)

        st.session_state.current_result = formatted
        st.session_state.last_answer = formatted
        st.session_state.history.insert(
            0,
            {"expression": expression, "result": formatted}
        )

        st.session_state.expression_widget = formatted

    except Exception as error:
        st.session_state.current_result = f"Error: {error}"


# --------------------------------
# Sidebar settings
# --------------------------------
st.sidebar.title("⚙️ Settings")

theme_mode = st.sidebar.radio(
    "Theme Mode",
    ["Dark", "Light"],
    index=0 if st.session_state.theme_mode == "Dark" else 1,
)

angle_mode = st.sidebar.radio(
    "Angle Mode",
    ["Radians", "Degrees"],
    index=0 if st.session_state.angle_mode == "Radians" else 1,
)

st.session_state.theme_mode = theme_mode
st.session_state.angle_mode = angle_mode

st.sidebar.markdown("---")
st.sidebar.markdown("### Supported Functions")
st.sidebar.markdown(
    """
- `sin(x)`
- `cos(x)`
- `tan(x)`
- `sqrt(x)`
- `log(x)`
- `ln(x)`
- `factorial(x)`
- `abs(x)`
- `exp(x)`
- `pi`
- `e`
"""
)

if st.sidebar.button("Clear History", use_container_width=True):
    st.session_state.history = []


# --------------------------------
# Dynamic theme colors
# --------------------------------
if st.session_state.theme_mode == "Dark":
    bg_main = """
        radial-gradient(circle at top left, rgba(93, 63, 211, 0.18), transparent 28%),
        radial-gradient(circle at top right, rgba(0, 194, 203, 0.14), transparent 25%),
        linear-gradient(135deg, #07111f 0%, #0b1220 45%, #111827 100%)
    """
    text_primary = "#f8fafc"
    text_secondary = "#cbd5e1"
    border_color = "rgba(255, 255, 255, 0.10)"
    hero_bg = "rgba(255, 255, 255, 0.06)"
    card_bg = "linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.88))"
    result_bg = "linear-gradient(135deg, rgba(16, 185, 129, 0.20), rgba(59, 130, 246, 0.20))"
    history_bg = "rgba(255, 255, 255, 0.05)"
    input_bg = "rgba(15, 23, 42, 0.92)"
    button_bg = "linear-gradient(180deg, rgba(17, 24, 39, 0.98), rgba(30, 41, 59, 0.96))"
    sidebar_bg = "linear-gradient(180deg, #0b1220 0%, #111827 100%)"
else:
    bg_main = """
        radial-gradient(circle at top left, rgba(59, 130, 246, 0.10), transparent 28%),
        radial-gradient(circle at top right, rgba(16, 185, 129, 0.10), transparent 25%),
        linear-gradient(135deg, #f8fafc 0%, #eef2ff 45%, #e2e8f0 100%)
    """
    text_primary = "#0f172a"
    text_secondary = "#334155"
    border_color = "rgba(15, 23, 42, 0.10)"
    hero_bg = "rgba(255, 255, 255, 0.75)"
    card_bg = "linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(241, 245, 249, 0.95))"
    result_bg = "linear-gradient(135deg, rgba(187, 247, 208, 0.75), rgba(191, 219, 254, 0.75))"
    history_bg = "rgba(255, 255, 255, 0.72)"
    input_bg = "rgba(255, 255, 255, 0.92)"
    button_bg = "linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(226, 232, 240, 0.98))"
    sidebar_bg = "linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%)"

# --------------------------------
# Premium CSS
# --------------------------------
st.markdown(
    f"""
    <style>
        .stApp {{
            background: {bg_main};
            color: {text_primary};
        }}

        .block-container {{
            max-width: 920px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        section[data-testid="stSidebar"] {{
            background: {sidebar_bg};
            border-right: 1px solid {border_color};
        }}

        .hero-card {{
            background: {hero_bg};
            border: 1px solid {border_color};
            border-radius: 26px;
            padding: 30px 26px 22px 26px;
            backdrop-filter: blur(16px);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.16);
            margin-bottom: 18px;
        }}

        .title-text {{
            font-size: 2.6rem;
            font-weight: 800;
            line-height: 1.1;
            color: {text_primary};
            margin-bottom: 0.4rem;
        }}

        .subtitle-text {{
            color: {text_secondary};
            font-size: 1rem;
            margin-bottom: 0;
        }}

        .display-card {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 20px;
            padding: 16px 18px;
            margin-top: 8px;
            margin-bottom: 14px;
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.12);
        }}

        .result-card {{
            background: {result_bg};
            border: 1px solid {border_color};
            border-radius: 20px;
            padding: 16px 18px;
            margin-bottom: 18px;
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.10);
        }}

        .label-text {{
            font-size: 0.85rem;
            color: {text_secondary};
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
        }}

        .value-text {{
            font-size: 1.6rem;
            font-weight: 700;
            color: {text_primary};
            word-wrap: break-word;
        }}

        .history-card {{
            background: {history_bg};
            border: 1px solid {border_color};
            border-radius: 18px;
            padding: 14px 16px;
            margin-bottom: 10px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
        }}

        .history-line {{
            color: {text_primary};
            font-size: 0.98rem;
            margin: 0;
        }}

        div[data-testid="stTextInput"] input {{
            background: {input_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 16px !important;
            color: {text_primary} !important;
            padding: 14px 16px !important;
            font-size: 1.05rem !important;
        }}

        div[data-testid="stTextInput"] label {{
            color: {text_secondary} !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stButton"] > button {{
            width: 100%;
            border-radius: 16px;
            border: 1px solid {border_color};
            background: {button_bg};
            color: {text_primary};
            font-size: 1rem;
            font-weight: 700;
            min-height: 54px;
            transition: all 0.18s ease-in-out;
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.12);
        }}

        div[data-testid="stButton"] > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 14px 28px rgba(0, 0, 0, 0.16);
            border-color: rgba(59, 130, 246, 0.45);
        }}

        .small-note {{
            color: {text_secondary};
            font-size: 0.95rem;
            margin-top: 8px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------
# Header
# --------------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="title-text">🧮 Scientific Calculator</div>
        <p class="subtitle-text">
            Premium Python calculator with theme switching, angle modes, safe expression evaluation, and history tracking.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------
# Input
# --------------------------------
st.text_input(
    "Enter Expression",
    key="expression_widget",
    placeholder="Example: sin(pi/2) + sqrt(49) + 5^2",
)

expression_to_show = html.escape(
    st.session_state.expression_widget if st.session_state.expression_widget else "0"
)
result_to_show = html.escape(
    st.session_state.current_result if st.session_state.current_result else "No result yet"
)

st.markdown(
    f"""
    <div class="display-card">
        <div class="label-text">Expression</div>
        <div class="value-text">{expression_to_show}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="result-card">
        <div class="label-text">Result</div>
        <div class="value-text">{result_to_show}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------
# Calculator buttons
# --------------------------------
button_rows = [
    [("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/"), ("sin", "sin("), ("cos", "cos(")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("×", "*"), ("tan", "tan("), ("sqrt", "sqrt(")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("-", "-"), ("log", "log("), ("ln", "ln(")],
    [("0", "0"), (".", "."), ("(", "("), (")", ")"), ("+", "+"), ("^", "^")],
    [("pi", "pi"), ("e", "e"), ("mod", "%"), ("abs", "abs("), ("fact", "factorial("), ("ANS", "ANS")],
]

for row_index, row in enumerate(button_rows):
    cols = st.columns(6, gap="small")
    for col_index, (label, value) in enumerate(row):
        with cols[col_index]:
            if label == "ANS":
                st.button(
                    label,
                    key=f"btn_{row_index}_{col_index}",
                    use_container_width=True,
                    on_click=insert_answer,
                )
            else:
                st.button(
                    label,
                    key=f"btn_{row_index}_{col_index}",
                    use_container_width=True,
                    on_click=append_value,
                    args=(value,),
                )

action_cols = st.columns(3, gap="small")

with action_cols[0]:
    st.button(
        "AC",
        key="clear_all",
        use_container_width=True,
        on_click=clear_expression,
    )

with action_cols[1]:
    st.button(
        "DEL",
        key="delete_one",
        use_container_width=True,
        on_click=delete_last,
    )

with action_cols[2]:
    st.button(
        "=",
        key="evaluate",
        use_container_width=True,
        on_click=evaluate_expression,
    )

# --------------------------------
# Examples
# --------------------------------
st.markdown("### Quick Examples")
st.code(
    "2 + 3 * 4\n"
    "sqrt(81)\n"
    "sin(pi/2)\n"
    "cos(60)\n"
    "factorial(5)\n"
    "log(100)\n"
    "ln(e)\n"
    "5^3\n"
    "10 % 3",
    language="python",
)

st.markdown(
    f"""
    <p class="small-note">
        Current theme: <strong>{st.session_state.theme_mode}</strong> |
        Current angle mode: <strong>{st.session_state.angle_mode}</strong>
    </p>
    """,
    unsafe_allow_html=True,
)

# --------------------------------
# History
# --------------------------------
st.markdown("### History")

if st.session_state.history:
    for item in st.session_state.history[:10]:
        history_expression = html.escape(item["expression"])
        history_result = html.escape(item["result"])
        st.markdown(
            f"""
            <div class="history-card">
                <p class="history-line"><strong>{history_expression}</strong> = {history_result}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("No calculations yet.")