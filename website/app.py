import pandas as pd
import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None
    if request.method == 'POST':
        route = request.form.get('route')
        flight_code = request.form.get('flight_code')
        departure_hour = request.form.get('departure_hour')

        if route:
            route = route.strip().upper()
        if flight_code:
            flight_code = flight_code.strip().upper()
        if departure_hour:
            departure_hour = int(departure_hour)

        print("Route:", route, "Flight Code:", flight_code, "Departure Hour:", departure_hour)

        # CSV dosyasının yolu
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'temizlenmis_veriler.csv')

        try:
            df = pd.read_csv(csv_path)
            print("CSV loaded:", df.head())

            # Uçuşu bul
            matched_flights = df[
                (df['Flight'].str.upper() == flight_code) & 
                (df['Route'].str.upper() == route) & 
                (df['Departure_Hour'] == departure_hour)
            ]

            if not matched_flights.empty:
                # En yüksek probability'ye sahip satırı bul
                row = matched_flights.loc[matched_flights['Probability'].idxmax()]
                probability = round(row['Probability'], 2)
                result = row['Result']

                # Açıklama metinleri
                explanation = ""
                if result == "LESS_THAN_30_MINUTES":
                    explanation = "Uçuşunuzun 30 dakikadan az gecikmesi tahmin ediliyor."
                elif result == "BETWEEN_30_AND_60_MINUTES":
                    explanation = "Uçuşunuzun 30 ile 60 dakika arasında gecikmesi tahmin ediliyor."
                elif result == "BETWEEN_60_AND_120_MINUTES":
                    explanation = "Uçuşunuzun 60 ile 120 dakika arasında gecikmesi tahmin ediliyor."
                elif result == "OVER_120_MINUTES_OR_CANCELLED":
                    explanation = "Uçuşunuzun 120 dakikadan fazla gecikmesi veya iptal edilmesi tahmin ediliyor."

                # Dictionary olarak prediction oluştur - probability'yi hem float hem string olarak gönder
                prediction = {
                    'probability': probability,
                    'probability_str': str(probability),  # String versiyonu
                    'result': result,
                    'explanation': explanation,
                    'flight_code': flight_code,
                    'route': route
                }
            else:
                prediction = {'error': 'Belirtilen kriterlere uygun uçuş bulunamadı.'}
        except FileNotFoundError:
            prediction = {'error': 'CSV dosyası bulunamadı. Dosya yolunu kontrol edin.'}
        except Exception as e:
            prediction = {'error': f'Hata oluştu: {str(e)}'}

    print("Prediction:", prediction)
    return render_template("predict.html", prediction=prediction)

@app.route('/analysis')
def analysis():
    return render_template("analysis.html")

@app.route('/sql_queries')
def sql_queries():
    # CSV dosyasından veri oku
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'temizlenmis_veriler.csv')
    
    try:
        df = pd.read_csv(csv_path)
        
        # SQL sorgularını simüle et
        queries = [
            {
                'id': 1,
                'title': 'En Çok Geciken Rotalar',
                'description': 'Hangi rotalarda uçuşlar ortalama olarak daha fazla gecikiyor? Bu analiz, rota bazında gecikme olasılıklarının ortalamasını gösterir.',
                'query': '''SELECT Route, AVG(Probability) AS avg_delay
FROM cloud_delay_bucket
GROUP BY Route
ORDER BY avg_delay DESC
LIMIT 10''',
                'result': df.groupby('Route')['Probability'].mean().round(10).sort_values(ascending=False).head(10).reset_index().values.tolist(),
                'columns': ['Rota', 'Ortalama Gecikme Olasılığı (%)']
            },
            {
                'id': 2,
                'title': 'Saatlere Göre Gecikme Dağılımı',
                'description': 'Günün hangi saatlerinde uçuşların gecikme olasılığı daha yüksek? 24 saatlik dilim boyunca gecikme eğilimlerini analiz eder.',
                'query': '''SELECT Departure_Hour, AVG(Probability) AS avg_delay
FROM cloud_delay_bucket
GROUP BY Departure_Hour
ORDER BY Departure_Hour ASC''',
                'result': df.groupby('Departure_Hour')['Probability'].mean().round(10).reset_index().values.tolist(),
                'columns': ['Kalkış Saati', 'Ortalama Gecikme Olasılığı (%)']
            },
            {
                'id': 3,
                'title': 'En Çok Geciken Uçuş Kodları',
                'description': 'Hangi spesifik uçuş kodları (flight number) en yüksek gecikme olasılığına sahip? Bu, belirli uçuş rotalarının performansını değerlendirir.',
                'query': '''SELECT Flight, AVG(Probability) AS avg_delay
FROM cloud_delay_bucket
GROUP BY Flight
ORDER BY avg_delay DESC
LIMIT 10''',
                'result': df.groupby('Flight')['Probability'].mean().round(10).sort_values(ascending=False).head(10).reset_index().values.tolist(),
                'columns': ['Uçuş Kodu', 'Ortalama Gecikme Olasılığı (%)']
            },
            {
                'id': 4,
                'title': 'Hafta Günlerine Göre Gecikme Analizi',
                'description': 'Haftanın hangi günlerinde gecikmeler daha fazla? 0=Pazartesi, 6=Pazar olmak üzere haftalık gecikme paternlerini gösterir.',
                'query': '''SELECT Departure_DayOfWeek, AVG(Probability) AS avg_delay
FROM cloud_delay_bucket
WHERE Departure_DayOfWeek IS NOT NULL
GROUP BY Departure_DayOfWeek
ORDER BY Departure_DayOfWeek''',
                'result': df[df['Departure_DayOfWeek'].notna()].groupby('Departure_DayOfWeek')['Probability'].mean().round(10).reset_index().values.tolist(),
                'columns': ['Haftanın Günü', 'Ortalama Gecikme Olasılığı (%)']
            },
            {
                'id': 5,
                'title': 'Uçak Tiplerine Göre Gecikme Performansı',
                'description': 'Hangi uçak modelleri daha az gecikiyor? Farklı uçak tiplerinin operasyonel performanslarını karşılaştırır.',
                'query': '''SELECT 
  Aircraft, 
  AVG(Probability) AS avg_delay
FROM 
  cloud_delay_bucket
GROUP BY 
  Aircraft
ORDER BY 
  avg_delay DESC''',
                'result': df.groupby('Aircraft')['Probability'].mean().round(10).sort_values(ascending=False).reset_index().values.tolist(),
                'columns': ['Uçak Tipi', 'Ortalama Gecikme Olasılığı (%)']
            },
            {
                'id': 6,
                'title': 'En Az Geciken Uçuşlar',
                'description': 'Gecikme olasılığı %10\'dan düşük olan en güvenilir uçuşlar hangileri? Zamanında kalkış konusunda en başarılı uçuşları listeler.',
                'query': '''SELECT 
  Flight, Route, Probability
FROM 
  cloud_delay_bucket
WHERE 
  Probability < 10
ORDER BY 
  Probability DESC
LIMIT 20''',
                'result': df[df['Probability'] < 10].nlargest(20, 'Probability')[['Flight', 'Route', 'Probability']].round(10).values.tolist(),
                'columns': ['Uçuş Kodu', 'Rota', 'Gecikme Olasılığı (%)']
            }
        ]
        
        return render_template("sql_queries.html", queries=queries)
        
    except Exception as e:
        # Hata durumunda örnek veri göster
        queries = [
            {
                'id': 1,
                'title': 'Veri Yükleme Hatası',
                'description': f'CSV dosyası yüklenirken hata oluştu: {str(e)}',
                'query': 'SELECT * FROM cloud_delay_bucket LIMIT 1',
                'result': [['Veri bulunamadı', 'Hata', 0]],
                'columns': ['Hata', 'Açıklama', 'Değer']
            }
        ]
        return render_template("sql_queries.html", queries=queries)

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)