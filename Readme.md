# ⚡ AI-Powered Electricity Theft Prevention System

An intelligent decision-support platform for power utilities to detect and prevent electricity theft using machine learning and explainable AI.

## 📋 Overview

This Streamlit-based application combines:
- **Strategic Dashboard**: Real-time monitoring of high-risk consumers
- **Live Prediction**: ML-based theft detection for new consumer data
- **Explainable AI**: Understanding why specific consumers are flagged

## 🛠 Technologies & Tools Used

### Core Libraries
- **Streamlit** (v1.0+): Interactive web framework for data apps
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning models (via joblib)
- **Joblib**: Model serialization and loading

### Machine Learning
- **Trained Model**: `electricity_theft_model (1).pkl`
  - Classification model for binary prediction (theft/normal)
  - Predicts probability of electricity theft
  
- **Feature Scaler**: `scaler (1).pkl`
  - StandardScaler for feature normalization
  - Ensures consistent model input preprocessing

### Data Source
- **Dashboard Data**: `dashboard_data.csv`
  - Contains historical consumer data with columns:
    - `CONS_NO`: Consumer ID
    - `AREA_ID`: Geographic area identifier
    - `risk_score`: ML-generated risk score (0-1)
    - `risk_level`: Risk category (Low/Medium/High)
    - `estimated_loss`: Estimated financial loss (₹)
    - `theft_reason`: Explanation for flagging

## 📊 Features

### Tab 1: Strategic Dashboard
1. **Control Panel** - Filter by Area and Risk Level
2. **KPIs** - High-level metrics:
   - Total Consumers
   - High Risk Cases
   - Total Estimated Loss
   - Areas Monitored

3. **Area-Wise Risk Overview** - Bar chart analysis
4. **High Priority Consumers** - Sortable table of flagged cases
5. **Inspection Priority List** - Top 10 consumers by risk × loss
6. **Explainable AI** - Reason explanations for each consumer

### Tab 2: Live Prediction
- Upload new consumer usage CSV file
- Automated feature engineering (7 derived features)
- Real-time prediction with confidence score
- Visual feedback (error/success messages)

## 🎯 Feature Engineering

Extracted from time-series usage data:
- `mean_usage`: Average consumption
- `std_usage`: Usage variability
- `min_usage`: Minimum recorded usage
- `max_usage`: Maximum recorded usage
- `usage_drop`: Average change in usage
- `zero_ratio`: Proportion of zero readings
- `AREA_USAGE_RATIO`: Normalized area baseline

## 📁 Project Structure

```
d:\Desktop\Theft Predictiion\
├── app.py                                    # Main Streamlit application
├── electricity_theft_model (1).pkl           # Trained ML model
├── scaler (1).pkl                            # Feature scaler
├── dashboard_data.csv                        # Historical consumer data
└── README.md                                 # This file
```

## 🚀 How to Run

### Prerequisites
```bash
pip install streamlit pandas numpy scikit-learn joblib
```

### Launch Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📥 Input Data Format

For live predictions, upload CSV with:
- Column 1: Consumer ID
- Column 2: Area ID
- Columns 3+: Hourly/daily usage readings (numeric)

Example:
```
CONS_NO,AREA_ID,Hour_0,Hour_1,Hour_2,...,Hour_23
C00001,Area_A,45,50,48,...,52
C00002,Area_B,120,118,125,...,130
```

## 🧠 Model Performance

- **Type**: Classification (Binary - Theft/Normal)
- **Input Features**: 7 engineered features
- **Output**: Probability score (0-1)
- **Confidence**: Displayed alongside predictions

## ⚙️ Configuration

Edit `st.set_page_config()` in app.py to customize:
- Page title
- Layout (wide/centered)
- Favicon
- Initial sidebar state

## 🔧 Troubleshooting

| Error | Solution |
|-------|----------|
| `FileNotFoundError: dashboard_data.csv` | Ensure CSV exists in same directory |
| `Model loading failed` | Verify `.pkl` files are not corrupted |
| `Feature mismatch error` | Check uploaded CSV has numeric columns from index 2+ |
| `Empty dataframe` | Verify data in CSV file and filters applied |

## 📈 Future Enhancements

- [ ] Real-time database integration
- [ ] Advanced visualization dashboards
- [ ] Model retraining pipeline
- [ ] Multi-language support
- [ ] Export reports (PDF/Excel)

## 📝 License

Internal use for power utilities only.

## 👨‍💼 Support

For issues or questions, contact your data engineering team.

---
**Built for Smart Utilities | AI + Decision Intelligence**