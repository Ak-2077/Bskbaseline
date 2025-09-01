# 🎓 School Performance Dashboard

A comprehensive multi-level school analysis system built with Streamlit that provides hierarchical drill-down analysis from school overview to individual student performance.

## 📊 Features

- **School Overview**: Performance comparison across 80+ schools with different types (Government, Private, International, Semi-Government)
- **Interactive Navigation**: Click-based drill-down from school → grade → section → student levels
- **Dynamic Visualizations**: Scatter plots, radar charts, bar charts, and box plots
- **Real Data Integration**: Supports CSV data files with automatic column mapping
- **Performance Metrics**: Tracks multiple assessment areas including Logical Reasoning, Critical Thinking, Creative Thinking, etc.

## 🚀 Quick Start

### Local Development

1. **Clone/Download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   streamlit run student_performance_analysis.py
   ```
4. **Open your browser** to `http://localhost:8501`

### Data Requirements

Place your CSV files in the `data/` directory. The app automatically detects and processes files with these column patterns:
- Student performance metrics (percentages)
- Grade and Section information
- Student names

## 🌐 Deployment on Streamlit Cloud

### **Step 1: GitHub Setup**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/school-dashboard.git
git push -u origin main
```

### **Step 2: Deploy**
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account
4. Select your repository
5. **Main file**: `student_performance_analysis.py`
6. Click "Deploy"

## 📁 Project Structure

```
Ai/
├── student_performance_analysis.py    # Main application
├── requirements.txt                   # Dependencies
├── data/                             # CSV data files
│   ├── DATA.csv
│   └── [other CSV files]
├── README.md                         # This file
├── .streamlit/
│   └── config.toml                   # App configuration
└── .gitignore                        # Git exclusions
```

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly Express/Graph Objects
- **Interactivity**: streamlit-plotly-events

## 📝 License

This project is for educational and analytical purposes.
