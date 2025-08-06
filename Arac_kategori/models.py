from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Kullanici(Base):
    __tablename__ = "kullanicilar"

    id = Column(Integer, primary_key=True, index=True)
    kullanici_adi = Column(String(50), unique=True, index=True, nullable=False)
    parola = Column(String(100), nullable=False)
    admin = Column(Boolean, default=False)


class Arac(Base):
    __tablename__ = "araclar"

    id = Column(Integer, primary_key=True, index=True)
    isim = Column(String(100), index=True, nullable=False)
    kategori = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    yil = Column(Integer, nullable=False)
    favori = Column(Boolean, default=False)


def seed_data(session):
    # Kullanıcı verilerini ekle
    if not session.query(Kullanici).first():
        session.add_all([
            Kullanici(
                kullanici_adi="admin",
                parola="admin123",
                admin=True
            ),
            Kullanici(
                kullanici_adi="user",
                parola="user123",
                admin=False
            ),
        ])
        session.commit()
    
    # Araç verilerini ekle
    if not session.query(Arac).first():
        session.add_all([
            Arac(
                isim="Kar Küreme Aracı",
                kategori="Yol Bakım",
                model="KKA-2022",
                yil=2022,
                favori=False
            ),
            Arac(
                isim="Tuzlama Aracı",
                kategori="Yol Bakım",
                model="TA-2021",
                yil=2021,
                favori=False
            ),
            Arac(
                isim="Çöp Kamyonu",
                kategori="Temizlik",
                model="CK-2020",
                yil=2020,
                favori=False
            ),
        ])
        session.commit()
