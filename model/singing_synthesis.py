# model/singing_synthesis.py

import os
import sys
import torch
import numpy as np
import soundfile as sf
import json
import traceback
import torch.nn.functional as F

# Add root path for relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infer.utils.hparams import set_hparams, hparams
from infer.modules.hifigan.hifigan import HifiGanGenerator as HiFiGAN
from infer.modules.fastspeech.fs2 import FastSpeech2, build_mel2ph

# Load hyperparameters
set_hparams(config="configs/base.yaml")

# Dummy phoneme dictionary (used in model initialization)
import string

class DummyDictionary:
    def __init__(self):
        self.symbols = ["<pad>"] + list(string.ascii_lowercase) + [f"num_{i}" for i in range(10)] + ["sym"]
        self.pad_token = 0

    def pad(self):
        return self.pad_token

    def __len__(self):
        return len(self.symbols)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.symbols.index(item) if item in self.symbols else 0
        return self.symbols[item]

# Global flags and models
MODEL_LOADED = False
acoustic_model = None
vocoder_model = None

# Phoneme to ID mapping
phoneme_to_id = {s: i for i, s in enumerate(["<pad>"] + list(string.ascii_lowercase) + [f"num_{i}" for i in range(10)] + ["sym"])}


def load_diffsinger_model():
    global acoustic_model, vocoder_model, MODEL_LOADED
    try:
        dictionary = DummyDictionary()
        acoustic_model = FastSpeech2(dictionary=dictionary, out_dims=hparams['audio_num_mel_bins'])
        acoustic_model.eval()

        with open("assets/vocoder/hifigan_config.json") as f:
            h = json.load(f)

        vocoder_model = HiFiGAN(h)
        ckpt = torch.load("checkpoints/vocoder/model_ckpt_steps_2076000.ckpt", map_location="cpu")
        vocoder_model.load_state_dict(ckpt["state_dict"]["model_gen"])
        vocoder_model.eval()

        MODEL_LOADED = True
        print("✅ DiffSinger and HiFi-GAN loaded successfully")
        return True
        
    except Exception as e:
        print("❌ Error loading models:")
        traceback.print_exc()
        return False

def build_mel2ph(ph_dur):
    # ph_dur: list of durations (frames) for each phoneme
    mel2ph = []
    for i, d in enumerate(ph_dur):
        mel2ph += [i + 1] * int(d)  # +1 because 0 is usually padding
    return torch.tensor([mel2ph], dtype=torch.long)  # shape [1, total_frames]

def generate_singing_audio(diffsinger_input, output_path="lullaby.wav"):
    if not MODEL_LOADED:
        raise RuntimeError("Model not loaded")

    ph_seq = diffsinger_input["ph_seq"]
    ph_dur = diffsinger_input["ph_dur"]
    note_seq = diffsinger_input["note_seq"]
    note_dur = diffsinger_input["note_dur"]

    print(f"Phoneme Sequence: {ph_seq}")
    print(f"Note Sequence: {note_seq}")

    if len(ph_seq) == 0 or len(note_seq) == 0:
        raise ValueError("Empty input sequence: ph_seq or note_seq is empty.")

    ph_ids = [phoneme_to_id.get(p, 0) for p in ph_seq]
    ph_ids = torch.LongTensor(ph_ids).unsqueeze(0)
    ph_dur = torch.FloatTensor(ph_dur).unsqueeze(0)
    note_seq = torch.FloatTensor(note_seq).unsqueeze(0)
    note_dur = torch.FloatTensor(note_dur).unsqueeze(0)

    print(f"ph_ids: {ph_ids}, shape: {ph_ids.shape}")
    print(f"ph_dur: {ph_dur}, shape: {ph_dur.shape}")
    print(f"note_seq: {note_seq}, shape: {note_seq.shape}")
    print(f"note_dur: {note_dur}, shape: {note_dur.shape}")
    
    with torch.no_grad():
        print(f"ph_dur (before mel2ph): {ph_dur[0].tolist()}")
        mel2ph = build_mel2ph(ph_dur[0].tolist())
        print(f"mel2ph shape: {mel2ph.shape}, total frames: {mel2ph.shape[1]}")
        print(f"mel2ph: {mel2ph}")
        output_dict = acoustic_model(
            txt_tokens=ph_ids,
            mel2ph=mel2ph,
            note_pitches=note_seq,
            note_durs=note_dur,
            infer=False,         # <--- Try infer=False
            use_gt_dur=True
        )

    print(f"📦 Output dict keys: {output_dict.keys()}")
    
    mel_output = output_dict['mel_out']
    print(f"🔍 mel_output.shape: {mel_output.shape}")
    if mel_output.shape[1] == 0:
        print("❌ Model returned empty mel. Likely due to invalid phoneme/token input.")
        return

    if mel_output.shape[1] == 0:
        print("❌ Error: mel_output is empty. Returning silence.")
        mel_output = torch.zeros((1, 50, 80))

    mel_input = mel_output.transpose(1, 2)
    hhmel_input = torch.tanh(mel_input) * 4.0  # Normalize gently to [-4, 4]


    if mel_input.shape[2] < 30:
        mel_input = F.interpolate(mel_input, size=100, mode='linear')
        print(f"⚠️ Mel too short: {mel_output.shape[1]} frames, interpolating to 100.")

    # Denormalize mel spectrogram if needed
    # mel_input = FastSpeech2.mel_denorm(mel_input)

    print("mel_input shape:", mel_input.shape)
    print("mel_input min/max:", mel_input.min().item(), mel_input.max().item())
    print("mel_input mean:", mel_input.mean().item())

    with torch.no_grad():
        
        audio = vocoder_model(mel_input)

    audio_np = audio.detach().squeeze().cpu().numpy()
    sf.write(output_path, audio_np, samplerate=22050)
    print(f"🔉 audio tensor shape: {audio.shape}, min: {audio.min()}, max: {audio.max()}")

    if os.path.exists(output_path):
        print(f"✅ File written: {output_path}")
    else:
        print(f"❌ File write failed: {output_path} not found.")

    return output_path
