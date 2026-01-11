# this is use for regex
import re

FILLER_WORDS=[
    'uh','um','you know','okay','so','like','basically','actually','right','i mean'
]


# \b              → word boundary (ensures clean matching)
# \d{1,2}         → 1 or 2 digits (hours or minutes)
# :               → literal colon
# \d{2}           → exactly 2 digits (seconds)
# (:\d{2})?       → optional ":ss" (for HH:MM:SS format)
# \b              → word boundary
# re.sub(pattern,replacment,text)
def remove_timestamps(text:str)->str:
    return re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\b","",text)

def remove_filler_words(text:str)->str:
    for filler in FILLER_WORDS:
        pattern=r"\b" + re.escape(filler) + r"\b"
        text=re.sub(pattern,"",text,flags=re.IGNORECASE)
    return text

def normalize_whitespace(text:str)->str:
    text=re.sub(r"\s+"," ",text)
    return text.strip()

def basic_sentence_cleanup(text:str)->str:
    text=text.replace(" .",".")
    text=text.replace(" ,",",")
    text=text.replace(" ?","?")
    return text

def clean_transcript(text:str)->str:
    text=remove_timestamps(text)
    text=remove_filler_words(text)
    text=normalize_whitespace(text)
    text=basic_sentence_cleanup(text)
    return text

