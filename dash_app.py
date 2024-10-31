from dashboard import create_dashboard

if __name__ == '__main__':
    app = create_dashboard("../data/processed/air_quality_cleaned.csv")
    app.run_server(debug=True)