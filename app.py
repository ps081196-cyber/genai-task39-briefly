import os
import streamlit as st
from core import SAMPLE, generate, preview, validate_text

st.set_page_config(page_title='Briefly | GenAI Summarizer', page_icon='📝', layout='centered')
st.title('📝 Briefly')
st.caption('Turn long text into clear summaries • Assignment 39 • Devendra Singh')

def secret(name, default=''):
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets.get(name, default)
    except FileNotFoundError:
        return default

with st.sidebar:
    st.header('Summary settings')
    mode = st.radio('Mode', ['Offline preview', 'Generative AI'])
    style = st.selectbox('AI output format', ['Bullet points', 'Short paragraph', 'Study notes with headings'])
    length = st.select_slider('AI summary length', ['Short (80 words)', 'Medium (150 words)', 'Detailed (250 words)'])
    language = st.selectbox('AI output language', ['English', 'Hindi'])
    model = st.text_input('Hugging Face chat model', value=secret('HF_MODEL', 'Qwen/Qwen2.5-7B-Instruct'))
    user_token = st.text_input('Your HF token (if no deployment secret)', type='password') if mode == 'Generative AI' else ''
    st.caption('Model availability and inference credits depend on your provider/account. No token is included in this project.')

st.info('Offline preview extracts existing sentences. Select Generative AI for model-generated summaries.')
st.caption('AI mode sends the submitted text to the selected inference provider. Avoid confidential data.')
if 'document' not in st.session_state:
    st.session_state.document = ''
if st.button('Load example'):
    st.session_state.document = SAMPLE
uploaded = st.file_uploader('Optional: upload a UTF-8 text file (up to 100 KB)', type=['txt'])
if uploaded is not None:
    if uploaded.size > 100000:
        st.error('File too large. Upload a text file below 100 KB.')
    else:
        try:
            content = uploaded.getvalue().decode('utf-8-sig')
            if st.session_state.get('last_upload') != content:
                st.session_state.document = content
                st.session_state.last_upload = content
        except UnicodeDecodeError:
            st.error('Please save the file as UTF-8 text.')
text = st.text_area('Paste your document', key='document', height=250, max_chars=16000)
st.caption(f'{len(text.split())} words • {len(text):,}/16,000 characters')
if st.button('Create summary', type='primary'):
    st.session_state.pop('result', None)
    try:
        validate_text(text)
        with st.spinner('Preparing your summary…'):
            result = preview(text) if mode == 'Offline preview' else generate(text, user_token or secret('HF_TOKEN'), model, style, length, language)
        st.session_state.result = result
        st.session_state.result_mode = mode
    except ValueError as error:
        st.error(str(error))
    except Exception:
        st.error('Inference failed. Check token permissions, credits, model/provider support and network access, then retry. No credentials are shown.')
if st.session_state.get('result'):
    st.subheader('Summary')
    st.caption('Created using: ' + st.session_state.result_mode)
    st.markdown(st.session_state.result)
    st.download_button('Download summary', st.session_state.result, file_name='summary.txt', mime='text/plain')
st.divider()
st.caption('Review AI output against the original. Source files are not saved by this app; current-session input/output stays in session memory.')
