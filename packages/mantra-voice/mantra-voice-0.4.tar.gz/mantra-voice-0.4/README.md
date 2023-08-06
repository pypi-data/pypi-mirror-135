# Mantra Voice
A speech to text library that builds on top of [gTTS](https://pypi.org/project/gTTS/) and [pyttsx3](https://pypi.org/project/pyttsx3/). This is specifically designed for [Mantra AI](https://github.com/bossauh/mantra-ai)

## Features
- Easily configurable voice with effects thanks to [SoX](http://sox.sourceforge.net/)
- Fallback to pyttsx3's offline text to speech when gTTS fails.

## Requirements
You'd have to install [SoX](http://sox.sourceforge.net/) after that make sure to add it to `PATH`

If you happen to receive an error related to sox when using the text to speech, copy the provided `libmad-0.dll` and `libmp3lame-0.dll` files to your sox's directory.

Thanks to [this post](https://stackoverflow.com/questions/3537155/sox-fail-util-unable-to-load-mad-decoder-library-libmad-function-mad-stream) for helping out.


### Install Package
```
pip install mantra-voice
```

## Usage
The main `say()` function is a coroutine because it is expected to be used in asynchronous programs.
```py
import asyncio
from mantra_voice import TextToSpeech

async def main() -> None:
    tts = TextToSpeech(
        "path/to/unprocessed.mp3",
        "path/to/processed.wav"
    )

    await tts.say("Hello World")


if __name__ == "__main__":
    asyncio.run(main())
```

You can initialize the `TextToSpeech` class with a `config=` in order to change certain settings like so.
```py
TextToSpeech(
    config={
        "engine": "gtts" # Either 'gtts' or 'pyttsx3'. Required,
        "gtts_params": {
            # Parameters to be passed to the gTTS class (only used if engine == "gtts")
            "lang": "en",
            "tld": "co.za"
        },
        "tfm_effects": {
            # SoX effects, check code for more info and also sox's documentation.
            "tempo": 1.3,
            "chorus": [0.8, 1, 3]
            ...
        },
        "pyttsx3_properties": {
            # Properties to be set in the pyttsx3 engine. Even if you have the gtts engine, you might still want to configure this since the say() coroutine will fallback to pyttsx3 if gtts didn't work. i.e, no internet connection
            "rate": 138
        }
    }
)
```

## API Referece
### `class TextToSpeech(raw_path: str, processed_path: str, config: dict = DEFAULT_CONFIG)`
- `raw_path: str` mp3 path that tells the engine where to save the unprocessed voice. i.e, no tfm effects.
- `processed_path: str` wav path that tells the engine where to save the processed voice. i.e, with tfm effects.
- `config: dict` Configuration, defaults to the constant `DEFAULT_CONFIG` variable inside `tts.py`
- `mixer: Mixer` Mantra voice supports the Mixer class from [mantra-mixer](https://github.com/bossauh/mantra-mixer). When this class is provided, the play_file coroutine from `Mixer` will be used instead

- ## Methods
    - ### `async def say(text: str, blocking: bool = False)`
        - Make the engine say the provided `text`
    - ### `update_config(config: dict)`
        - Updates the current config with the provided config. (So you wouldn't have to reinitialize)

## Exceptions
### `class TTSError(Exception)`
- Base class for all exception related to this library.
### `class InvalidEngine(TTSError)`
- Raised when the config detects an invalid engine name.
### `class InvalidEffect(TTSError)`
- Raised when an invalid tfm effect is detected in the config.

# LICENSE
MIT License
Copyright (c) 2021 Philippe Mathew
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
