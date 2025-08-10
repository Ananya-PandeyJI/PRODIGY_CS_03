from PIL import Image
import numpy as np
import random

def xor_encrypt_decrypt(img: Image.Image, key: int) -> Image.Image:
    arr = np.array(img)
    encrypted = arr ^ key
    return Image.fromarray(encrypted)

def shuffle_encrypt(img: Image.Image, seed: int) -> (Image.Image, list):
    arr = np.array(img)
    h, w, c = arr.shape
    flat = arr.reshape(-1, c)
    indices = list(range(flat.shape[0]))
    random.seed(seed)
    random.shuffle(indices)
    shuffled = flat[indices]
    return Image.fromarray(shuffled.reshape((h, w, c))), indices

def shuffle_decrypt(encrypted_img: Image.Image, indices: list) -> Image.Image:
    arr = np.array(encrypted_img)
    h, w, c = arr.shape
    flat = arr.reshape(-1, c)
    inv = [0] * len(indices)
    for i, orig_idx in enumerate(indices):
        inv[orig_idx] = i
    restored = flat[inv]
    return Image.fromarray(restored.reshape((h, w, c)))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple image encrypt/decrypt tool")
    parser.add_argument("mode", choices=["xor", "shuffle"], help="Method")
    parser.add_argument("operation", choices=["encrypt", "decrypt"], help="Encrypt or decrypt")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--key", type=int, default=0, help="Key for XOR or shuffle seed")
    parser.add_argument("--indices", help="Indices file for shuffle decrypt")
    args = parser.parse_args()

    img = Image.open(args.input).convert("RGB")

    if args.mode == "xor":
        if args.operation in ("encrypt", "decrypt"):
            out = xor_encrypt_decrypt(img, args.key)
            out.save(args.output)

    elif args.mode == "shuffle":
        if args.operation == "encrypt":
            out, indices = shuffle_encrypt(img, args.key)
            out.save(args.output)
            # Save indices for decryption
            with open(f"{args.output}.indices", "w") as f:
                f.write(",".join(map(str, indices)))
        else:
            with open(args.indices) as f:
                indices = list(map(int, f.read().split(",")))
            out = shuffle_decrypt(img, indices)
            out.save(args.output)
