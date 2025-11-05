import streamlit as st
import asyncio
from debate import team_config, debate

st.title(":blue[Debating Agents]")

topic = st.text_input("Give a topic:", value="Shall the US government ban TikTok?")

clicked = st.button("Start", type='primary')

chat = st.container()

if clicked:
    chat.empty()
    async def main():
        team = await team_config(topic)
        current_speaker = None
        content_placeholder = None
        buffer = ""
        
        with chat:
            async for msg in debate(team):
                if ": " not in msg:
                    continue  # Skip invalid messages
                
                source, content_chunk = msg.split(": ", 1)
                # Do NOT strip the chunk - preserve original spacing and newlines from the model
                if not content_chunk:  # Skip truly empty chunks
                    continue
                
                if source != current_speaker:
                    # Finish previous message if any (buffer is already in placeholder)
                    
                    # Start new message for this speaker
                    if source == "Jane":
                        message_container = st.chat_message(name="Jane", avatar="assistant")
                    elif source == "John":
                        message_container = st.chat_message(name="John", avatar="👍")
                    elif source == "Alice":
                        message_container = st.chat_message(name="Alice", avatar="👎")
                    else:
                        continue
                    
                    content_placeholder = message_container.empty()
                    buffer = ""
                    current_speaker = source
                
                # Simply append the raw chunk - trust the model's tokenization for spacing, punctuation, and line breaks
                buffer += content_chunk
                
                # Update the placeholder with the current buffer using markdown to respect \n for line breaks and paragraphs
                if content_placeholder is not None:
                    content_placeholder.markdown(buffer, unsafe_allow_html=False)
    
    asyncio.run(main())