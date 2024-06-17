# audio cut
from pydub import AudioSegment
wav_path = "..."
output_path = '...'
start_msec = 0
end_msec = 15000 
audio = AudioSegment.from_file(wav_path, format="wav")

cut_seconds = audio[int(start_msec):int(end_msec)]  

cut_seconds.export(output_path, format="wav")
