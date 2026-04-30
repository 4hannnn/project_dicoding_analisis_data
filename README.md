# Bike Sharing Analysis

This project analyzes the Bike Sharing Dataset (daily and hourly) and provides a Streamlit dashboard.

## Project Structure
- data/day.csv: daily dataset
- data/hour.csv: hourly dataset
- notebook.ipynb: analysis notebook (run all cells before submission)
- dashboard/dashboard.py: Streamlit app
- requirements.txt: project dependencies
- url.txt: Streamlit Cloud URL (fill after deployment)

## How to Run
1. Create and activate a Python environment.
2. Install dependencies:
   pip install -r requirements.txt
3. Run the dashboard:
   streamlit run dashboard/dashboard.py

## Notebook
- Open notebook.ipynb and run all cells so outputs are saved.
- The notebook covers: questions, data wrangling, EDA, visualization, and recommendations.

## Dashboard Features
- Filters: year and season
- Metrics: total rentals, average daily rentals, and peak day
- Charts: monthly trend, weather impact, working day vs holiday, and hourly demand pattern

## Submission Checklist
- [ ] All datasets included in data/
- [ ] notebook.ipynb executed and saved with outputs
- [ ] dashboard/dashboard.py runs locally
- [ ] requirements.txt included
- [ ] README.md included
- [ ] url.txt filled with Streamlit Cloud URL (after deployment)

## Notes
- If Streamlit is launched from the dashboard folder, the app still reads data from the project root.
- Deploy later and paste the URL into url.txt to complete the bonus requirement.
