import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.bug_analyzer import analyze_bug
from agents.code_fixer import fix_code
from agents.test_writer import write_tests
from agents.test_runner import run_tests
from db.database import get_all_runs, init_db
from dotenv import load_dotenv

load_dotenv()
init_db()

st.title("🤖 Bug-to-PR Agent")
st.subheader("Automatically fix bugs and create GitHub PRs!")

st.markdown("### 📝 Paste your buggy Python code:")
code = st.text_area("Enter your code here", height=200,
    placeholder="def calculate_average(numbers):\n    return sum(numbers) / len(numbers)",
    label_visibility="hidden")

if st.button("🔧 Fix My Bug!", type="primary"):
    if not code.strip():
        st.error("Please paste some code first!")
    else:
        with open("temp_input.py", "w") as f:
            f.write(code)

        with st.status("Running pipeline...", expanded=True) as status:
            st.write("🔍 Analyzing bug...")
            bug_report = analyze_bug(code)

            if not bug_report or "error" in bug_report:
                status.update(label="Pipeline failed!", state="error")
                st.error("❌ Could not analyze bug!")
            else:
                st.write("🔧 Fixing code...")
                fixed_code = fix_code(code, bug_report)

                if not fixed_code:
                    status.update(label="Pipeline failed!", state="error")
                    st.error("❌ Could not fix code!")
                else:
                    st.write("📝 Writing tests...")
                    test_code = write_tests(fixed_code)
                    os.makedirs("tests", exist_ok=True)
                    with open("tests/test_output.py", "w") as f:
                        f.write(test_code)

                    st.write("🧪 Running tests...")
                    result = run_tests()

                    if result["passed"]:
                        st.write("✅ Tests passed!")
                        status.update(label="Pipeline complete!", state="complete")

                        st.success("✅ Bug fixed successfully!")

                        st.markdown("### 🐛 Bug Found:")
                        st.info(bug_report.get('bug_description'))

                        st.markdown("### ✅ Fixed Code:")
                        st.code(fixed_code, language="python")

                        st.info("💡 PR creation works in local environment only.")

                        from db.database import save_run
                        save_run("temp_input.py", bug_report.get('bug_description'), True, "", "success")
                    else:
                        status.update(label="Pipeline failed!", state="error")
                        st.error("❌ Tests failed!")

st.markdown("---")
st.markdown("### 📊 Run History")

runs = get_all_runs()
if runs:
    import pandas as pd
    df = pd.DataFrame(runs, columns=["ID", "Timestamp", "File", "Bug Found", "Fixed", "PR URL", "Status"])
    df["Fixed"] = df["Fixed"].apply(lambda x: "✅" if x else "❌")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No runs yet!")