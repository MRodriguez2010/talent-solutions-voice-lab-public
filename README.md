# Voice Lab · Employee Sentiment Analysis

**Employee Sentiment Analysis project family:** [Project guide](https://github.com/MRodriguez2010/Revelio/blob/main/docs/employee-sentiment-analysis-projects.md) · [Revelio interactive demo](https://github.com/MRodriguez2010/Revelio)

A local analyst workbench for reviewing topic-level evidence and building a slide brief. Inspect the numerator and denominator for each comparison, approve the topics to include, and download an editable presentation. Approval choices persist locally in SQLite. Each exported slide corresponds to an approved topic.

```sh
python -m pip install -r requirements.txt
python lab.py
```

Open **http://127.0.0.1:8091**. The public edition uses a fictional survey summary. Its workbench, input schema and presentation layout are new public substitutes for the private client tooling. [Related repositories](https://github.com/search?q=user%3AMRodriguez2010+topic%3Aemployee-sentiment-analysis&type=repositories)

## Historical source examples

[Download the historical Caliber Collision benchmark](public-data/caliber-benchmark.pptx) or [inspect the underlying values](public-data/caliber-ratings.csv). The February 5, 2026 slide presents archived five-point ratings. The interactive fictional demo above uses favorable answer counts, a different measure.
