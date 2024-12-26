from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

# Fungsi untuk membaca data CSV
def load_data():
    try:
        print("Memulai proses membaca file CSV...")  # Debug log
        csv_path = 'jumlah_capaian_penanganan_sampah.csv'  # Path relatif
        print(f"Path file CSV yang digunakan: {csv_path}")  # Debug log
        df = pd.read_csv(csv_path)  # Membaca file CSV
        print("File CSV berhasil dimuat:")
        print(df.head())  # Debug log
        return df
    except FileNotFoundError as fnf_error:
        print(f"File tidak ditemukan: {fnf_error}")
    except Exception as e:
        print(f"Error saat membaca file CSV: {e}")
    return pd.DataFrame()  # DataFrame kosong jika ada error

# Fungsi untuk simulasi Monte Carlo
def monte_carlo_prediction(df, year, num_simulations=1000):
    try:
        print("DataFrame diterima untuk prediksi:")
        print(df.head())  # Debug log
        data = df['jumlah_sampah'].values  # Ambil data dari kolom jumlah_sampah
        mean = np.mean(data)
        std_dev = np.std(data)
        simulated_data = np.random.normal(mean, std_dev, num_simulations)
        prediction = simulated_data.mean()
        return prediction
    except Exception as e:
        print(f"Error di monte_carlo_prediction: {e}")
        return 0

@app.route('/')
def index_page():
    try:
        print("Route / dipanggil")  # Debug log
        df = load_data()
        if df.empty:
            return "<h1>Data CSV kosong atau tidak ditemukan.</h1>"
        table_html = df.to_html(classes='table table-striped', index=False)
        return render_template('index.html', table_html=table_html)
    except Exception as e:
        print(f"Error di route /: {e}")
        return f"Error: {e}"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        year = int(request.form['year'])
        df = load_data()
        prediction = monte_carlo_prediction(df, year)
        return render_template('prediction.html', year=year, prediction=prediction)
    except Exception as e:
        print(f"Error di route /predict: {e}")
        return f"Error: {e}"

@app.route('/debug_csv')
def debug_csv():
    try:
        df = load_data()
        if df.empty:
            return "File CSV kosong atau tidak terbaca."
        return f"<h1>Data CSV berhasil dimuat:</h1><br>{df.to_html()}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

