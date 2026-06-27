import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator import run_pipeline
from db.database import get_all_runs, init_db
from dotenv import load_dotenv

load_dotenv()
init_db()

st.title("🤖 Bug-to-PR Agent")
st.subheader("Automatically fix bugs and create GitHub PRs!")

# Code input
st.markdown("### 📝 Paste your buggy Python code:")
code = st.text_area("Enter your code here", height=200, 
    placeholder="def calculate_average(numbers):\n    return sum(numbers) / len(numbers)",
    label_visibility="hidden")

# Fix button
if st.button("🔧 Fix My Bug!", type="primary"):
    if not code.strip():
        st.error("Please paste some code first!")
    else:
        with open("temp_input.py", "w") as f:
            f.write(code)
        
        with st.status("Running pipeline...", expanded=True) as status:
            st.write("🔍 Analyzing bug...")
            result = run_pipeline("temp_input.py")
            
            if result:
                st.write("🔧 Code fixed!")
                st.write("📝 Tests written!")
                st.write("🧪 Tests passed!")
                st.write("🚀 PR created!")
                status.update(label="Pipeline complete!", state="complete")
                
                st.success("✅ Bug fixed successfully!")
                
                st.markdown("### 🐛 Bug Found:")
                st.info(result['bug_report'].get('bug_description'))
                
                st.markdown("### ✅ Fixed Code:")
                st.code(result['fixed_code'], language="python")
                
                if result.get('pr_url'):
                    st.markdown("### 🔗 Pull Request:")
                    st.success(f"PR created: {result['pr_url']}")
            else:
                status.update(label="Pipeline failed!", state="error")
                st.error("❌ Could not fix the bug!")

# Run history
st.markdown("---")
st.markdown("### 📊 Run History")

runs = get_all_runs()
if runs:
    import pandas as pd
    df = pd.DataFrame(runs, columns=["ID", "Timestamp", "File", "Bug Found", "Fixed", "PR URL", "Status"])
    df["Fixed"] = df["Fixed"].apply(lambda x: "✅" if x else "❌")
    st.dataframe(df, width="stretch")
else:
    st.info("No runs yet!")