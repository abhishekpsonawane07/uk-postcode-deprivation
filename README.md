# 🗺️ Does Your Postcode Decide Your Life?

An interactive data analysis of deprivation, education and health across 317 English Local Authorities.

**🔗 Live App:** https://abhishekpsonawane07-uk-postcode-deprivation.streamlit.app/

---

## What This Project Does

Type any UK postcode and instantly see:
- How deprived your area is ranked out of 317 Local Authorities
- Your area's income, education and health scores
- How you compare to the rest of England

---

## Key Findings

- **8x deprivation gap** between the most deprived (Blackpool, 45.9) and least deprived (Hart, 5.7) areas in England
- **London and Manchester beat the odds** — despite high deprivation, these cities significantly outperform on education
- **The North/South divide is real** — deprivation increases significantly north of Derbyshire

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python + Pandas | Data cleaning and analysis |
| Plotly | Interactive charts and choropleth map |
| Streamlit | Web dashboard |
| Postcodes.io API | Live postcode lookup |
| GitHub + Streamlit Cloud | Deployment |

---

## Data Sources

- [ONS Indices of Multiple Deprivation 2019](https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019)
- [Postcodes.io](https://postcodes.io) — free UK postcode API

---

## How to Run Locally

```bash
git clone https://github.com/abhishekpsonawane07/uk-postcode-deprivation
cd uk-postcode-deprivation
pip install -r requirements.txt
streamlit run app.py
```

---

## Project Structure

```
├── app.py                  # Streamlit dashboard
├── Postcode_project.ipynb  # Analysis notebook
├── deprivation_data.csv    # Cleaned dataset
├── requirements.txt        # Dependencies
└── *.html                  # Exported charts
```
---
Built by Abhishek Sonawane · MSc Data Science

