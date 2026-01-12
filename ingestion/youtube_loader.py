# this import is use for parsing url,urlparse breaks URL into components(scheme,hostname....) and parse_qs converts query string(key=value & key2=value2) into dictionary
from urllib.parse import urlparse,parse_qs
# from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled,NoTranscriptFound,CouldNotRetrieveTranscript
import yt_dlp
import xml.etree.ElementTree as ET
from ingestion.manual_input import get_manual_transcript

def extract_video_id(youtube_url:str) -> str:
    parsed_url=urlparse(youtube_url)


    #if hostname matches given names we try to get only v part of the query...bcoz video id is stored in v
    if parsed_url.hostname in ['www.youtube.com','youtube.com']:
        return parse_qs(parsed_url.query).get('v',[None])[0]
    

    #if we have shortened url
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    
    else:
        raise ValueError("Invalid Youtube URL")
    

def get_video_metadata(youtube_url:str)->dict:
    # yt=YouTube(youtube_url)

    # return {
    #     # "title":yt.title,
    #     "duration_seconds":yt.length,
    #     "author":yt.author
    # }

    ydl_opts={'quiet':True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info=ydl.extract_info(youtube_url,download=False)

        return {
            'title':info.get('title'),
            'duration':info.get('duration'),
            'channel':info.get('uploader')
        }

# def get_video_transcript(video_id:str)->str:
#     transcript=YouTubeTranscriptApi.get_transcript(video_id,languages=['en','en-US'])


#     #here in transcripts we get 3 items in dictionary text,start,duration...from that we only need text...we run a loop on every text in dictionary join by seprating with a space
#     full_text=" ".join([item['text'] for item in transcript])
#     return full_text



def get_video_transcript_safe(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["en", "en-US"]
        )
        return " ".join(item["text"] for item in transcript)

    except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript):
        return None

    except Exception:
        return None

def load_youtube_video(youtube_url:str | None=None)->dict:

    if youtube_url:
        video_id=extract_video_id(youtube_url)
        metadata=get_video_metadata(youtube_url)
        transcript=get_video_transcript_safe(video_id)

        if transcript:
            return{
                "context_text":transcript,
                "content_source":"youtube_transcript",
                            "metadata":metadata            }
        
    manual_text=get_manual_transcript()

    return{
            'content_text':manual_text,
            'content_source':'manual_input',
            'metadata':None
        }