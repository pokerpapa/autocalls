import os, logging, wave, time
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

MODEL_PATH = os.getenv("VOSK_MODEL")
SAMPLE_RATE = 16000

def mp3_to_wav(src: str, dst: str) -> None:
    logging.debug("Конвертация MP3 → WAV")
    AudioSegment.from_mp3(src) \
        .set_channels(1) \
        .set_frame_rate(SAMPLE_RATE) \
        .export(dst, format="wav")

def transcribe(wav_path: str) -> str:
    logging.debug("Загрузка модели Vosk...")
    t0 = time.time()
    model = Model(MODEL_PATH)
    logging.debug(f"Модель загружена за {time.time()-t0:.1f}s")

    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)

    with wave.open(wav_path, "rb") as wf:
        while data := wf.readframes(4000):
            rec.AcceptWaveform(data)

    return rec.FinalResult()
