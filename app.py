import streamlit as st

st.title("🔐 Protocol → Tamarin Rule Generator")

st.write("Enter protocol steps (one per line):")
st.write("Example: User -> Server: Login")

protocol_text = st.text_area("Protocol Input", height=200)


def parse_protocol(text):
    steps = []
    lines = text.strip().split("\n")

    for i, line in enumerate(lines):
        if "->" in line and ":" in line:
            parts = line.split(":")
            actors = parts[0].split("->")
            message = parts[1].strip()

            steps.append({
                "step": i + 1,
                "from": actors[0].strip(),
                "to": actors[1].strip(),
                "message": message
            })

    return steps


def generate_tamarin_rules(protocol):
    rules = []

    for step in protocol:
        sender = step["from"]
        receiver = step["to"]
        message = step["message"]
        step_no = step["step"]

        send_rule = f"""
rule Step_{step_no}_{sender}_to_{receiver}:
  [ Fr(~{message}) ]
  -->
  [ Out({message}), State({sender},{receiver},{message}) ]
"""

        receive_rule = f"""
rule Step_{step_no}_{receiver}_receives:
  [ In({message}), State({sender},{receiver},{message}) ]
  -->
  [ ]
"""

        rules.append(send_rule)
        rules.append(receive_rule)

    return "\n".join(rules)


if st.button("Generate Tamarin Rules"):
    if protocol_text.strip() == "":
        st.warning("Please enter protocol!")
    else:
        parsed = parse_protocol(protocol_text)
        output = generate_tamarin_rules(parsed)
        

        st.markdown("---")
        st.markdown("### 📜 Tamarin Rules Output")

        st.code(output)

        st.success("Rules generated successfully!")

        st.text_area("Copy Rules", output, height=200)

        st.download_button(
            label="Download .spthy file",
            data=output,
            file_name="protocol.spthy",
            mime="text/plain"
        )