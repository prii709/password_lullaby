import torch

ckpt_path = "checkpoints/vocoder/model_ckpt_steps_2076000.ckpt"
checkpoint = torch.load(ckpt_path, map_location="cpu")

# Print top-level keys
print("\n🔍 Top-level keys in checkpoint:")
print(checkpoint.keys())

# Try going deeper if wrapped
if "state_dict" in checkpoint:
    print("\n📦 Keys inside checkpoint['state_dict']:")
    print(checkpoint["state_dict"].keys())

if "model_gen" in checkpoint:
    print("\n✅ model_gen exists — keys:")
    print(checkpoint["model_gen"].keys())

if "generator" in checkpoint:
    print("\n✅ generator exists — keys:")
    print(checkpoint["generator"].keys())
