from flask import Flask
from flask_restful import Api, Resource
from youtube_transcript_api import YouTubeTranscriptApi
import json
from transformers import T5ForConditionalGeneration, T5Tokenizer
from flask import request
from flask import jsonify

app = Flask(__name__)

class YouTubeTranscript(Resource):
    def get_yt_transcript(self,video_id):
        transcript = ""
        transcript_dict = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_json = json.dumps(transcript_dict)
        text_json = json.loads(transcript_json)
        for instance in text_json:
            transcript += instance['text'] + " "

        return transcript
    
class Text_Summarize:
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("t5-base")
        self.model = T5ForConditionalGeneration.from_pretrained("t5-base")

    def summarize(self,transcript):
        chunks = [transcript[i:i+1024] for i in range(0,len(transcript),1024)]
        summary=[]
        for chunk in chunks:
            inputs = self.tokenizer.encode("summarize: " + chunk, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
            chunk_summary = self.tokenizer.decode(outputs[0])
            summary.append(chunk_summary)
        transcript_summary = " ".join(summary)

        return transcript_summary
    
@app.route('/api/summarize',methods=['GET'])
def get_summarize_youtube():#video_id eg: 1iNyqomXQt8
    youtube_url = request.args.get('youtube_url')
    video_id = youtube_url.split('v=')[1]
    youtube_transcript = YouTubeTranscript()
    

    try:
        transcript = youtube_transcript.get_yt_transcript(video_id)
        text_summarize = Text_Summarize()
        summary = text_summarize.summarize(transcript)

        return jsonify({'Summary':summary},{'Transcript':transcript}), 200
        

    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == "__main__":
    app.run(debug = True,port=5000)