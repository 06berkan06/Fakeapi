from sqlalchemy import Column, Integer, String, Boolean, Text
from database import Base


class Kullanici(Base):
    __tablename__ = "kullanicilar"
    
    id = Column(Integer, primary_key=True, index=True)
    kullanici_adi = Column(String, unique=True, index=True)
    parola = Column(String)
    admin = Column(Boolean, default=False)


class Arac(Base):
    __tablename__ = "araclar"

    id = Column(Integer, primary_key=True, index=True)
    isim = Column(String, index=True)
    model = Column(String)
    yil = Column(Integer)
    kategori = Column(String)
    fiyat = Column(Integer, default=0)
    aciklama = Column(Text, nullable=True)
    favori = Column(Boolean, default=False)
    resim_url = Column(String, nullable=True)


def seed_data():
    """Örnek veriler"""
    return {
        "kullanicilar": [
            {"kullanici_adi": "admin", "parola": "admin123", "admin": True},
            {"kullanici_adi": "user", "parola": "user123", "admin": False},
        ],
        "araclar": [
            {
                "isim": "BMW X5",
                "model": "X5",
                "yil": 2023,
                "kategori": "SUV",
                "fiyat": 850000,
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=300&fit=crop"
            },
            {
                "isim": "Mercedes C-Class",
                "model": "C-Class",
                "yil": 2022,
                "kategori": "Sedan",
                "favori": False,
                "resim_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=400&h=300&fit=crop"
            },
            {
                "isim": "Audi A3",
                "model": "A3",
                "yil": 2023,
                "kategori": "Hatchback",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=400&h=300&fit=crop"
            },
            {
                "isim": "Volkswagen Golf",
                "model": "Golf",
                "yil": 2021,
                "kategori": "Hatchback",
                "favori": False,
                "resim_url": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=400&h=300&fit=crop"
            },
            {
                "isim": "Toyota RAV4",
                "model": "RAV4",
                "yil": 2023,
                "kategori": "SUV",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1541899481282-d53bffe3c55d?w=400&h=300&fit=crop"
            },
            {
                "isim": "Honda Civic",
                "model": "Civic",
                "yil": 2022,
                "kategori": "Sedan",
                "favori": False,
                "resim_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop"
            },
            {
                "isim": "Ford F-150",
                "model": "F-150",
                "yil": 2023,
                "kategori": "Pickup",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop"
            },
            {
                "isim": "Nissan Qashqai",
                "model": "Qashqai",
                "yil": 2022,
                "kategori": "SUV",
                "favori": False,
                "resim_url": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=400&h=300&fit=crop"
            },
            {
                "isim": "Hyundai i30",
                "model": "i30",
                "yil": 2023,
                "kategori": "Hatchback",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=400&h=300&fit=crop"
            },
            {
                "isim": "Kia Sportage",
                "model": "Sportage",
                "yil": 2023,
                "kategori": "SUV",
                "favori": False,
                "resim_url": "https://images.unsplash.com/photo-1541899481282-d53bffe3c55d?w=400&h=300&fit=crop"
            },
            {
                "isim": "Mazda CX-5",
                "model": "CX-5",
                "yil": 2022,
                "kategori": "SUV",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=300&fit=crop"
            },
            {
                "isim": "Subaru Impreza",
                "model": "Impreza",
                "yil": 2023,
                "kategori": "Sedan",
                "favori": False,
                "resim_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop"
            },
            {
                "isim": "Volvo XC60",
                "model": "XC60",
                "yil": 2023,
                "kategori": "SUV",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1541899481282-d53bffe3c55d?w=400&h=300&fit=crop"
            },
            {
                "isim": "Lexus RX",
                "model": "RX",
                "yil": 2022,
                "kategori": "SUV",
                "favori": False,
                "resim_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=300&fit=crop"
            },
            {
                "isim": "Porsche Cayenne",
                "model": "Cayenne",
                "yil": 2023,
                "kategori": "SUV",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=300&fit=crop"
            },
            {
                "isim": "Tesla Model 3",
                "model": "Model 3",
                "yil": 2023,
                "kategori": "Sedan",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop"
            },
            {
                "isim": "Range Rover Sport",
                "model": "Sport",
                "yil": 2023,
                "kategori": "SUV",
                "favori": False,
                "resim_url": "https://images.unsplash.com/photo-1541899481282-d53bffe3c55d?w=400&h=300&fit=crop"
            },
            {
                "isim": "Bentley Continental",
                "model": "Continental",
                "yil": 2022,
                "kategori": "Sedan",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=400&h=300&fit=crop"
            },
            {
                "isim": "Ferrari F8",
                "model": "F8",
                "yil": 2023,
                "kategori": "Sports",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop"
            },
            {
                "isim": "Lamborghini Huracan",
                "model": "Huracan",
                "yil": 2023,
                "kategori": "Sports",
                "favori": False,
                "resim_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop"
            },
            {
                "isim": "McLaren 720S",
                "model": "720S",
                "yil": 2022,
                "kategori": "Sports",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop"
            },
            {
                "isim": "Bugatti Chiron",
                "model": "Chiron",
                "yil": 2023,
                "kategori": "Sports",
                "favori": True,
                "resim_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop"
            },
            {
                "isim": "Rolls Royce Phantom",
                "model": "Phantom",
                "yil": 2023,
                "kategori": "Sedan",
                "favori": False,
                "resim_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=400&h=300&fit=crop"
            }
        ]
    }
