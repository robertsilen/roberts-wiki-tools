# roberts-wiki-tools

Python tools created and used as Wikipedian in Residence for Projekt Fredrika ([projektfredrika.fi](https://projektfredrika.fi/)). I have edited over 10000 articles in Swedish Wikipedia and over 50000 Wikidata objects. These scripts were created effectively thanks to the _help_ of Generative AI. 

### In this repo
* stats\_wikipedia\_multi_lang.py - used to compile statistics for Wikipedia article views over multiple languages, taking as input a Wikidata Q-code and fetching data from Wikipedia APIs

### In [projekt-fredrika](https://github.com/projekt-fredrika)'s repo

* [finsvetekniker.ipynb](https://github.com/projekt-fredrika/Fredrikas-Lupp/blob/master/scripts/finsvetekniker.ipynb) early AI-test for final project described at [projektfredrika.fi/ai-sauna](https://projektfredrika.fi/ai-sauna/) - Script that applies Generative AI to improve Wikipedia by analyzing sources (books), finding relevant Wikipedia articles to improve (with NER), and making improvement suggestions - using NER and LLM (OpenAI & Anthropic API)
* [kotus-fo](https://github.com/projekt-fredrika/kotus-fo) - Script to parse wordlist (XML) of Finland Swedish dialects published by Institute for the Languages of Finland (Kotus), and to transform it to be uploadable to Wikidata where possible (according to rules developed together with Kotus-experts)
* [commons-statistik.py](https://github.com/projekt-fredrika/Fredrikas-Lupp/blob/master/scripts/commons-statistik.py) - used to compile view statistics for Wikimedia Commons images, fetching data from Commons' API