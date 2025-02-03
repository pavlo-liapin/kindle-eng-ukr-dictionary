<img src="https://github.com/user-attachments/assets/8b2ffba5-74f9-4308-b455-57068e2e0c1c">

## About 🇬🇧🇺🇦

<img src="https://github.com/user-attachments/assets/1dee5c1e-1d68-4546-9fef-7971fbbd0806" align="right" width="250px">

**Welcome to the Kindle-Compatible English-Ukrainian Dictionary!**

This comprehensive, Kindle-native dictionary is designed to provide seamless translations while reading, making it the perfect companion for language learners, translators, and book lovers! 📚✨

If you’re a Ukrainian native speaker expanding your English vocabulary through reading, or an English speaker learning Ukrainian, this dictionary enables instant word lookups without disrupting your reading experience.

Compatible with all Kindle models and generations — including *Kindle Paperwhite*, *Oasis*, *Scribe* and others, it integrates directly into the Kindle lookup feature. It also works on any e-reader or app that supports MOBI dictionaries, ensuring a smooth and effortless bilingual reading experience.

### Features

- 🔍 **Optimized for Kindle**. Look up words instantly without leaving your book!<br/>
- ⚡ **Fast & Lightweight**. No lag, no hassle.<br/>
- 📚 **Massive Word Database**. Includes over 75,000 articles and 155,000+ words!<br/>
- 📖 **Based on the trusted dictionary**. *Англо-український словник М.І. Балла*, sourced from [bakustarver/ukr-dictionaries-list-opensource](https://github.com/bakustarver/ukr-dictionaries-list-opensource).<br/>
- 🌍 **British & American Spellings**. Whether it’s *color/colour* or *organize/organise*, this dictionary has you covered!
- 🔠 **Supports Different Word Forms**. Various verb conjugations, adjective forms, and plural nouns for accurate translations.

## Installation

1. Download [the dictionary](https://github.com/pavlo-liapin/kindle-eng-ukr-dictionary/releases/download/1.0/en-ua-dictionary-1.0.mobi) in MOBI format.
2. Install [Calibre](https://calibre-ebook.com) on your computer.
3. Connect your Kindle to your computer using a USB cable.
4. In Calibre, go to *Device* > *Add Books from a single folder*, and select
   the downloaded MOBI file.
5. Once the transfer is complete, go to *Device* > *Eject* to safely remove
   your Kindle.
6. On your Kindle, set it as the default dictionary.

## 📬 Contact & Support

Have questions or suggestions? Drop a message in the Issues tab or reach out on GitHub!

Happy reading! 📚✨

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

### Scripts

The following scripts are executed sequentially to process the original source dictionary:

| Script Name                                 | Purpose                                                                                   |
|---------------------------------------------|-------------------------------------------------------------------------------------------|
| [00.sanitize.py](scripts/00.sanitize.py)    | Removes metadata entries from the dictionary.                                             |
| [01.crosslinks.py](scripts/01.crosslinks.py)| Merges dictionary articles with simple links into a single consolidated entry.            |
| [02.varcon-csv.py](scripts/02.varcon-csv.py)| Converts the Variant Conversion (VarCon) dataset into a CSV of British and American variants. |
| [03.variants.py](scripts/03.variants.py)    | Applies the generated CSV to add synonyms and variants to the dictionary.                 |
| [04.irregular-nouns.py](scripts/04.irregular-nouns.py)| Extracts irregular noun inflections from the dictionary and saves them in a CSV.           |
| [05.filter-irregular-nouns.py](scripts/05.filter-irregular-nouns.py)| Merges dictionary articles for irregular nouns into their main entries.                    |
| [06.regular-nouns.py](scripts/06.regular-nouns.py)| Processes regular noun inflections, such as plural forms.                                  |
| [07.adjectives.py](scripts/07.adjectives.py)| Generates comparative and superlative forms of adjectives.                                |
| [08.filter-irregular-verbs.py](scripts/08.filter-irregular-verbs.py)| Merges dictionary articles for irregular verbs into their main entries.                    |
| [09.irregular-verbs.py](scripts/09.irregular-verbs.py)| Extracts irregular verb inflections and saves them in a CSV.                               |
| [10.regular-verbs.py](scripts/10.regular-verbs.py)| Processes regular verb inflections (e.g., past tense, participles, -ing form, singular forms). |
| [11.all-inflections.py](scripts/11.all-inflections.py)| Applies all previously extracted and processed inflections back into the dictionary.       |
| [12.clean-markup.py](scripts/12.clean-markup.py)| Cleans up redundant markup from the original source file.                                  |
| [13.convert-to-xhtml.py](scripts/13.convert-to-xhtml.py)| Converts the processed dictionary data into XHTML format for final output.                 |

Each script plays a critical role in transforming the source dictionary into its final structured and usable format.

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

## License

### Attribution for AI-Generated Content
Some parts of this project, including code and images, were generated with the
assistance of OpenAI's ChatGPT. OpenAI asserts no copyright over the outputs
you generate with ChatGPT, and you are free to use them in accordance with the
terms of the [OpenAI Usage Policies](https://openai.com/policies/usage-policies).

### VarCon Licensing

The VarCon dataset is Copyright 2000-2020 by Kevin Atkinson and Benjamin Titze
and is used under the terms of its license, which permits use, modification,
and redistribution with proper attribution.

The VarCon dataset was derived from numerous sources, including the Ispell
distribution, and is provided "as is" without warranty.

For more details, visit the official VarCon page: [http://wordlist.aspell.net/](http://wordlist.aspell.net/).
