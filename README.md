# Project 2: Persuasive or Deceptive Visualization?

## Proposition

Gender equality in education is now mostly solved.

## Dataset

This project uses the World Bank Human Development Indicators dataset, specifically the `gender.csv` file from the gender category. The analysis focuses on:

- Girls' and boys' adjusted net enrollment rate in primary school
- Women's and men's gross tertiary enrollment rate

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

## How To Reproduce

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Regenerate the processed data and chart images:

```bash
python3 src/make_visualizations.py
```

Open `index.html` in a browser or publish the repository with GitHub Pages.

## Final Submission

The final submission page is `index.html`. Before submitting, replace the group member placeholder in the header with each member's full name and UCSD email address.

## Design Summary

The first visualization argues for the proposition by focusing on the latest available female-to-male primary enrollment ratios across regions and income groups. The second visualization argues against the proposition by shifting attention to tertiary education and income-group inequality.
