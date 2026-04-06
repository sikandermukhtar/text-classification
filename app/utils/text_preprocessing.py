import re

def remove_url(text):
    pattern = re.compile(r'https?://\S+|www\.\S+')
    return pattern.sub(r'', text)

def remove_html_tags(text):
  pattern = re.compile(r'<.*?>')
  return pattern.sub(r'', text)

def clean_text(text):

    text = remove_html_tags(text)
    text = remove_url(text)

    return text