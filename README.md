# Project 2: Persuasive or Deceptive Visualization?

## Proposition

Gender equality in education is now mostly solved.

## Group Members

- Harshini Kanakala: hkanakala@ucsd.edu
- Jiya Sreejesh: jsreejesh@ucsd.edu
- Kala Nguyen: knn013@ucsd.edu
- Triton Stewart: trstewart@ucsd.edu

## Dataset

This project uses the World Bank Human Development Indicators dataset, specifically the `gender.csv` file from the gender category. The analysis focuses on:

- Girls' and boys' adjusted net enrollment rate in primary school
- Women's and men's gross tertiary enrollment rate

Dataset source: https://github.com/light-and-salt/World-Bank-Data-by-Indicators

## Project Structure

```text
.
├── data/
│   ├── raw/gender.csv
│   └── processed/
├── src/make_visualizations.py
├── visuals/
├── index.html
├── report/
└── README.md
```

## Reproduce the Visualizations

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Regenerate the processed data and chart images:

```bash
python3 src/make_visualizations.py
```

## Design Summary

The first visualization argues for the proposition by focusing on the latest available female-to-male primary enrollment ratios across regions and income groups. The second visualization argues against the proposition by shifting attention to tertiary education and income-group inequality.

The design rationale in `index.html` documents 3-5 design decisions for each visualization, assigns each decision a deception/earnestness score from -2 to 2, and reflects on the ethical boundary between persuasion and deception.
