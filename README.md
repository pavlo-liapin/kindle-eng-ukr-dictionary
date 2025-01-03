<img src="https://github.com/user-attachments/assets/8b2ffba5-74f9-4308-b455-57068e2e0c1c">

## About

This repository provides a Kindle-compatible format of the English-Ukrainian
dictionary (*Англо-український словник М.І. Балла*), a comprehensive resource
originally sourced from [bakustarver/ukr-dictionaries-list-opensource](https://github.com/bakustarver/ukr-dictionaries-list-opensource).

The dictionary has been optimized for use on Kindle devices,
enabling seamless access to translations and definitions directly within your
e-reader.

## Installation

1. Download [the latest version of the dictionary file](https://github.com/pavlo-liapin/kindle-eng-ukr-dictionary/releases/download/1.0/en-ua-dictionary-1.0.mobi) in MOBI format.
2. Install [Calibre](https://calibre-ebook.com) on your computer.
3. Connect your Kindle to your computer using a USB cable.
4. In Calibre, go to *Device* > *Add Books from a single folder*, and select
   the downloaded MOBI file.
5. Once the transfer is complete, go to *Device* > *Eject* to safely remove
   your Kindle.
6. On your Kindle, set the newly added dictionary as the default dictionary.

## Development

### Prerequisites

The scripts have been tested with **Python 3.10.16**, and the following dependencies are required:

```bash
pip install pyinflect
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```

> [!NOTE]
> On macOS ARM (e.g., M1/M2), use `spacy[apple]` instead of `spacy` for compatibility.
> For more details, refer to the [SpaCy installation guide](https://spacy.io/usage#installation).

## Acknowledgments

Thanks to these great resources that helped in preparing this dictionary:

- [Ukrainian offline dictionaries in open formats](https://github.com/bakustarver/ukr-dictionaries-list-opensource)
  for providing the source of this dictionary.

- **Jake McCrary**'s article
  [Creating a custom Kindle dictionary](https://jakemccrary.com/blog/2020/11/11/creating-a-custom-kindle-dictionary/)
  for explaining the basics of the Kindle dictionary format.

- **Hossein Yazdani**'s open-source
  [English-Persian Dictionary](https://github.com/hossein1376/English-Persian-Kindle-Custom-Dictionary)
  and
  [Kindle Custom Dictionary Scripts](https://github.com/hossein1376/Kindle-Custom-Dictionary-Scripts)
  for providing basic scripts that actually work.

- **Kevin Atkinson** and **Benjamin Titze** for the
  [**VarCon dataset**](src/varcon.zip) (Variant Conversion Info),
  which provides information to convert between American, British, Canadian,
  and Australian spellings and vocabulary.

### VarCon Licensing

The VarCon dataset is Copyright 2000-2020 by Kevin Atkinson and Benjamin Titze
and is used under the terms of its license, which permits use, modification,
and redistribution with proper attribution.

The VarCon dataset was derived from numerous sources, including the Ispell
distribution, and is provided "as is" without warranty.

For more details, visit the official VarCon page: [http://wordlist.aspell.net/](http://wordlist.aspell.net/).

Special thanks to Kevin Atkinson and Benjamin Titze for their work on VarCon.
