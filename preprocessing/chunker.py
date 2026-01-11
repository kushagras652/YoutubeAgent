# We will use token-aware fixed-size chunking with overlap.

from typing import List,Dict

def chunk_text(text:str,chunk_size:int =500,overlap:int = 100 )->List[Dict]:
    if overlap>=chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    
    chunks=[]
    start=0
    chunk_id=0
    text_length=len(text)

    while start<text_length:
        end=start+chunk_size
        chunk_text=text[start:end]

        chunks.append({
            "chunk_id":chunk_id,
            "text":chunk_text.strip(),
            "start_char":start,
            "end_char":min(end,text_length)
        })

        chunk_id+=1
        start+=chunk_size-overlap

    return chunks

