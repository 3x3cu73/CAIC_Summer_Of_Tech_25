# Hidden in Plain Sight

**Category:** Steganography  
**Points:** 100
**Difficulty:** Medium

## Description

A seemingly innocent image contains a secret message.

## Files
- [miku.jpg](./miku.jpg) - Image containing hidden data

## Hints
<details>
  <summary>Hints</summary>
- [10] stegseek has some modes of running
- [40] you can run stegseek with rockyou.txt to bruteforce the passphrase
</details>

<details>
  <summary>Solution and Flag</summary>
## Solution
- Use stegseek on the image with rockyou.txt, it will find the key `hatsune` and give you the flag as a file.

## Flag
- dcCTF{h1d1ng_1n_y0ur_w1f1}
</details>
