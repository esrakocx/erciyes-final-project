import random
from datetime import datetime, timedelta
from amadeus import Client, ResponseError
import pandas as pd
import os

class FlightDelayPredictor:
    def __init__(self, client_id, client_secret):
        self.amadeus = Client(
            client_id=client_id,
            client_secret=client_secret
        )

    def predict_delay(self, flight_params):
        try:
            response = self.amadeus.travel.predictions.flight_delay.get(
                originLocationCode=flight_params['originLocationCode'],
                destinationLocationCode=flight_params['destinationLocationCode'],
                departureDate=flight_params['departureDate'],
                departureTime=flight_params['departureTime'],
                arrivalDate=flight_params['arrivalDate'],
                arrivalTime=flight_params['arrivalTime'],
                aircraftCode=flight_params['aircraftCode'],
                carrierCode=flight_params['carrierCode'],
                flightNumber=flight_params['flightNumber'],
                duration=flight_params['duration']
            )
            return response.data
        except ResponseError as error:
            print(f"Error occurred: {error}")
            return None

def create_flight_params(origin, destination, dep_date, dep_time, arr_date, arr_time, aircraft_code, carrier_code, flight_number, duration):
    return {
        'originLocationCode': origin,
        'destinationLocationCode': destination,
        'departureDate': dep_date,
        'departureTime': dep_time,
        'arrivalDate': arr_date,
        'arrivalTime': arr_time,
        'aircraftCode': aircraft_code,
        'carrierCode': carrier_code,
        'flightNumber': flight_number,
        'duration': duration
    }

def random_flight_time():
    date = datetime.today() + timedelta(days=random.randint(1, 30))
    dep_time = datetime.strptime(f"{random.randint(0, 23)}:{random.randint(0, 59)}:00", "%H:%M:%S").time()
    arr_time = (datetime.combine(date, dep_time) + timedelta(hours=random.randint(1, 16))).time()
    return date.strftime("%Y-%m-%d"), dep_time.strftime("%H:%M:%S"), date.strftime("%Y-%m-%d"), arr_time.strftime("%H:%M:%S")

def main():
    # API kimlik bilgilerini ayarla
    CLIENT_ID = 'kJKFKv7QftKWzWZ0DAMqET9IXKfbheG4'
    CLIENT_SECRET = '9SYSVJWzbkQR1iFp'

    predictor = FlightDelayPredictor(CLIENT_ID, CLIENT_SECRET)

    # Mevcut veri dosyasına göre yeni üretilecek veri miktarını belirle
    base_flights = 100
    csv_filename = "yeni_veriler.csv"
    if os.path.exists(csv_filename):
        df_existing = pd.read_csv(csv_filename)
        num_flights = base_flights + len(df_existing) // 2  # veri büyüdükçe daha fazla üret
    else:
        num_flights = base_flights
    print(f"\n{num_flights} adet yeni uçuş üretilecek.")

    # Rastgele seçilecek havaalanları
    airports = [
        'IST', 'ESB', 'ADB', 'SAW', 'GZT', 'TZX', 'AYT', 'ADA', 'BJV', 'DLM', 'ERZ', 
        'JFK', 'CDG', 'DXB', 'LAX', 'HND', 'SIN', 'SYD', 'FRA', 'ORD', 'MAD', 'MEX', 
        'HKG', 'YYZ', 'SFO', 'MIA', 'BOS', 'AMS', 'DEL', 'PEK', 'NRT', 'LHR', 'SIN', 
        'YYC', 'YVR', 'ICN', 'CGK', 'KIX', 'TLV', 'CPT', 'WAW', 'BRU', 'ZRH', 'LGW',
        'SFO', 'SEA', 'BNE', 'CMN', 'DUB', 'DUS', 'FCO', 'MXP', 'OST', 'YYJ', 'FLL',
        'MUC', 'BKK', 'KUL', 'MEL', 'HNL', 'SCL', 'MAD', 'OTP', 'VIE', 'CPH', 'ARN',
        'HEL', 'OSL', 'PMI', 'TLS', 'NCE', 'TPE', 'KHH'
    ]
    # Kullanılacak uçak modelleri (güncellenmiş)
    aircrafts = ['321', '777', '380', '787', '350', '747', '330', 'A220', 'A320', '737', '767']

    # Kullanılacak havayolu şirketleri
    carriers = ['TK', 'BA', 'EK', 'JL', 'SQ', 'LH', 'IB', 'CX', 'AC', 'DL', 'UA', 'AF', 'QF', 'NH', 'EY', 'AA', 'VX', 'VS', 'NZ', 'GA', 'KL', 'OA', 'SK', 'WY', 'CZ', 
    'CS', 'FI', 'AY', 'OS', 'RJ', '9W', 'AZ', 'MU', 'UA', 'TG', 'S7', 'OK', 
    'LX', 'SV', 'SN', 'NH', 'QR', 'AT', 'SC', 'VN', 'JL', 'SG', 'PK'
    ]

    # Uçuş listesini oluştur
    flights = []
    for _ in range(num_flights):
        origin, destination = random.sample(airports, 2)  # Aynı havaalanı seçilmemesi için
        dep_date, dep_time, arr_date, arr_time = random_flight_time()
        aircraft_code = random.choice(aircrafts)
        carrier_code = random.choice(carriers)
        flight_number = str(random.randint(100, 9999))
        duration = f"PT{random.randint(1, 16)}H{random.randint(10, 59)}M"

        flights.append(create_flight_params(origin, destination, dep_date, dep_time, arr_date, arr_time, aircraft_code, carrier_code, flight_number, duration))

    all_results = []

    for flight in flights:
        predictions = predictor.predict_delay(flight)

        if predictions:
            for pred in predictions:
                result = random.choices(
                    population=[
                        "LESS_THAN_30_MINUTES",
                        "BETWEEN_30_AND_60_MINUTES",
                        "BETWEEN_60_AND_120_MINUTES",
                        "OVER_120_MINUTES_OR_CANCELLED"
                    ],
                    weights=[0.5, 0.25, 0.15, 0.10],
                    k=1
                )[0]
                all_results.append({
                    'Flight': f"{flight['carrierCode']}{flight['flightNumber']}",
                    'Route': f"{flight['originLocationCode']}-{flight['destinationLocationCode']}",
                    'Departure': f"{flight['departureDate']} {flight['departureTime']}",
                    'Arrival': f"{flight['arrivalDate']} {flight['arrivalTime']}",
                    'Delay_Type': pred.get('subType', ''),
                    'Probability': pred.get('probability', 0),
                    'Result': result,
                    'Aircraft': flight['aircraftCode'],
                    'Duration': flight['duration']
                })

    # Eğer yeni veri varsa farklı bir CSV dosyasına kaydet
    if all_results:
        df_new = pd.DataFrame(all_results)

        # Eğer dosya varsa üstüne ekleyerek kaydet, yoksa yeni dosya oluştur
        if os.path.exists(csv_filename):
            df_old = pd.read_csv(csv_filename)
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            df_combined.to_csv(csv_filename, index=False)
        else:
            df_new.to_csv(csv_filename, index=False)

        print(f"\n {num_flights} yeni uçuş verisi {csv_filename} dosyasına kaydedildi!")
    else:
        print("\n⚠️ Hiçbir tahmin alınamadı!")

if __name__ == "__main__":
    main()