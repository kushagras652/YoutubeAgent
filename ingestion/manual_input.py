def get_manual_transcript()->str:
    print("\n Transcript not available")
    print("\n Paste the transcript below and when done type END on a new line")

    lines=[]

    while True:
        line=input()
        if line.strip()=='END':
            break
        lines.append(line)

    transcript=" ".join(lines).strip()

    if not transcript:
        raise ValueError("Empty transcript provided.")
    
    return transcript
