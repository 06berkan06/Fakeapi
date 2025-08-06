from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
from models import Arac, Kullanici
from schemas import (
    AracCreate, AracUpdate, AracResponse, MessageResponse,
    KullaniciLogin, LoginResponse
)

app = FastAPI(
    title="Araç Yönetim API",
    description="Yol bakım araçları için profesyonel yönetim sistemi",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static dosyaları serve et
app.mount("/static", StaticFiles(directory="."), name="static")

# Analytics verilerini saklamak için basit bir in-memory storage
analytics_data = {
    "vehicle_views": {},
    "favorite_clicks": {},
    "detail_views": {},
    "admin_actions": {},
    "daily_stats": {}
}


def get_current_user():
    """Basit kullanıcı kontrolü - client-side session kullanıyoruz"""
    return None


def require_admin():
    """Admin kontrolü - client-side'da yapılıyor"""
    return None

@app.on_event("startup")
async def startup_event():
    """Uygulama başladığında veritabanını oluştur ve örnek veriler ekle"""
    from database import engine
    from models import Base
    
    Base.metadata.create_all(bind=engine)
    
    # Örnek veriler ekle
    db = next(get_db())
    
    # Kullanıcılar
    admin_user = db.query(Kullanici).filter(Kullanici.kullanici_adi == "admin").first()
    if not admin_user:
        admin_user = Kullanici(kullanici_adi="admin", parola="admin123", admin=True)
        db.add(admin_user)
    
    normal_user = db.query(Kullanici).filter(Kullanici.kullanici_adi == "user").first()
    if not normal_user:
        normal_user = Kullanici(kullanici_adi="user", parola="user123", admin=False)
        db.add(normal_user)
    
            # Araçlar - Daha fazla örnek araç ekleyelim
        if db.query(Arac).count() == 0:
            araclar = [
                Arac(isim="BMW X5", model="X5", yil=2023, kategori="SUV", favori=True),
                Arac(isim="Mercedes C-Class", model="C-Class", yil=2022, kategori="Sedan", favori=False),
                Arac(isim="Audi A3", model="A3", yil=2023, kategori="Hatchback", favori=True),
                Arac(isim="Volkswagen Golf", model="Golf", yil=2021, kategori="Hatchback", favori=False),
                Arac(isim="Toyota RAV4", model="RAV4", yil=2023, kategori="SUV", favori=True),
                Arac(isim="Honda Civic", model="Civic", yil=2022, kategori="Sedan", favori=False),
                Arac(isim="Ford F-150", model="F-150", yil=2023, kategori="Pickup", favori=True),
                Arac(isim="Nissan Qashqai", model="Qashqai", yil=2022, kategori="SUV", favori=False),
                Arac(isim="Hyundai i30", model="i30", yil=2023, kategori="Hatchback", favori=True),
                Arac(isim="Kia Sportage", model="Sportage", yil=2023, kategori="SUV", favori=False),
                Arac(isim="Mazda CX-5", model="CX-5", yil=2022, kategori="SUV", favori=True),
                Arac(isim="Subaru Impreza", model="Impreza", yil=2023, kategori="Sedan", favori=False),
                Arac(isim="Volvo XC60", model="XC60", yil=2023, kategori="SUV", favori=True),
                Arac(isim="Lexus RX", model="RX", yil=2022, kategori="SUV", favori=False),
                Arac(isim="Porsche Cayenne", model="Cayenne", yil=2023, kategori="SUV", favori=True),
                Arac(isim="Tesla Model 3", model="Model 3", yil=2023, kategori="Sedan", favori=True),
                Arac(isim="Range Rover Sport", model="Sport", yil=2023, kategori="SUV", favori=False),
                Arac(isim="Bentley Continental", model="Continental", yil=2022, kategori="Sedan", favori=True),
                Arac(isim="Ferrari F8", model="F8", yil=2023, kategori="Sports", favori=True),
                Arac(isim="Lamborghini Huracan", model="Huracan", yil=2023, kategori="Sports", favori=False),
                Arac(isim="McLaren 720S", model="720S", yil=2022, kategori="Sports", favori=True),
                Arac(isim="Bugatti Chiron", model="Chiron", yil=2023, kategori="Sports", favori=True),
                Arac(isim="Rolls Royce Phantom", model="Phantom", yil=2023, kategori="Sedan", favori=False),
                Arac(isim="Aston Martin DB11", model="DB11", yil=2022, kategori="Sports", favori=True),
            ]
            db.add_all(araclar)
    
    db.commit()
    db.close()

@app.get("/", response_class=HTMLResponse)
async def root():
    """Ana sayfa"""
    return FileResponse("index.html")

@app.get("/login")
async def login_page():
    """Login sayfası"""
    return FileResponse("Fakeapi/Arac_kategori/login.html")

@app.get("/docs")
async def docs():
    """API dokümantasyonu"""
    return FileResponse("Fakeapi/Arac_kategori/docs.html")

# Analytics endpoints
@app.post("/analytics/view/{vehicle_id}")
async def track_vehicle_view(vehicle_id: int):
    """Araç görüntüleme sayısını takip et"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if vehicle_id not in analytics_data["vehicle_views"]:
        analytics_data["vehicle_views"][vehicle_id] = 0
    analytics_data["vehicle_views"][vehicle_id] += 1
    
    # Günlük istatistikleri güncelle
    if today not in analytics_data["daily_stats"]:
        analytics_data["daily_stats"][today] = {"views": 0, "favorites": 0, "details": 0}
    analytics_data["daily_stats"][today]["views"] += 1
    
    return {"message": "View tracked"}

@app.post("/analytics/favorite/{vehicle_id}")
async def track_favorite_click(vehicle_id: int):
    """Favori tıklama sayısını takip et"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if vehicle_id not in analytics_data["favorite_clicks"]:
        analytics_data["favorite_clicks"][vehicle_id] = 0
    analytics_data["favorite_clicks"][vehicle_id] += 1
    
    # Günlük istatistikleri güncelle
    if today not in analytics_data["daily_stats"]:
        analytics_data["daily_stats"][today] = {"views": 0, "favorites": 0, "details": 0}
    analytics_data["daily_stats"][today]["favorites"] += 1
    
    return {"message": "Favorite click tracked"}

@app.post("/analytics/detail/{vehicle_id}")
async def track_detail_view(vehicle_id: int):
    """Detay görüntüleme sayısını takip et"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if vehicle_id not in analytics_data["detail_views"]:
        analytics_data["detail_views"][vehicle_id] = 0
    analytics_data["detail_views"][vehicle_id] += 1
    
    # Günlük istatistikleri güncelle
    if today not in analytics_data["daily_stats"]:
        analytics_data["daily_stats"][today] = {"views": 0, "favorites": 0, "details": 0}
    analytics_data["daily_stats"][today]["details"] += 1
    
    return {"message": "Detail view tracked"}

@app.post("/analytics/admin-action")
async def track_admin_action(action: str, vehicle_id: Optional[int] = None):
    """Admin işlemlerini takip et"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in analytics_data["admin_actions"]:
        analytics_data["admin_actions"][today] = {}
    
    if action not in analytics_data["admin_actions"][today]:
        analytics_data["admin_actions"][today][action] = 0
    analytics_data["admin_actions"][today][action] += 1
    
    return {"message": "Admin action tracked"}

@app.get("/analytics/vehicle/{vehicle_id}")
async def get_vehicle_analytics(vehicle_id: int):
    """Belirli bir aracın analytics verilerini getir"""
    views = analytics_data["vehicle_views"].get(vehicle_id, 0)
    favorites = analytics_data["favorite_clicks"].get(vehicle_id, 0)
    details = analytics_data["detail_views"].get(vehicle_id, 0)
    
    return {
        "vehicle_id": vehicle_id,
        "views": views,
        "favorite_clicks": favorites,
        "detail_views": details,
        "total_interactions": views + favorites + details
    }

@app.get("/analytics/dashboard")
async def get_analytics_dashboard():
    """Analytics dashboard verilerini getir"""
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Toplam istatistikler
    total_views = sum(analytics_data["vehicle_views"].values())
    total_favorites = sum(analytics_data["favorite_clicks"].values())
    total_details = sum(analytics_data["detail_views"].values())
    
    # Günlük istatistikler
    today_stats = analytics_data["daily_stats"].get(today, {"views": 0, "favorites": 0, "details": 0})
    yesterday_stats = analytics_data["daily_stats"].get(yesterday, {"views": 0, "favorites": 0, "details": 0})
    
    # En popüler araçlar
    popular_vehicles = []
    for vehicle_id in analytics_data["vehicle_views"]:
        views = analytics_data["vehicle_views"][vehicle_id]
        favorites = analytics_data["favorite_clicks"].get(vehicle_id, 0)
        details = analytics_data["detail_views"].get(vehicle_id, 0)
        total = views + favorites + details
        
        popular_vehicles.append({
            "vehicle_id": vehicle_id,
            "views": views,
            "favorites": favorites,
            "details": details,
            "total_interactions": total
        })
    
    # En popüler 5 araç
    popular_vehicles.sort(key=lambda x: x["total_interactions"], reverse=True)
    top_vehicles = popular_vehicles[:5]
    
    return {
        "overview": {
            "total_views": total_views,
            "total_favorites": total_favorites,
            "total_details": total_details,
            "total_interactions": total_views + total_favorites + total_details
        },
        "daily_stats": {
            "today": today_stats,
            "yesterday": yesterday_stats
        },
        "popular_vehicles": top_vehicles,
        "admin_actions": analytics_data["admin_actions"].get(today, {})
    }

@app.get("/analytics/trends")
async def get_analytics_trends(days: int = 7):
    """Son N günün trend verilerini getir"""
    trends = []
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        stats = analytics_data["daily_stats"].get(date, {"views": 0, "favorites": 0, "details": 0})
        
        trends.append({
            "date": date,
            "views": stats["views"],
            "favorites": stats["favorites"],
            "details": stats["details"],
            "total": stats["views"] + stats["favorites"] + stats["details"]
        })
    
    return {"trends": list(reversed(trends))}

# Mevcut endpoints
@app.get("/araclar", response_model=List[AracResponse])
async def araclari_listele(favori: Optional[bool] = None, db: Session = Depends(get_db)):
    """Tüm araçları listele"""
    query = db.query(Arac)
    
    if favori is not None:
        query = query.filter(Arac.favori == favori)
    
    araclar = query.all()
    return araclar

@app.get("/araclar/{arac_id}", response_model=AracResponse)
async def arac_detay(arac_id: int, db: Session = Depends(get_db)):
    """Belirli bir aracın detaylarını getir"""
    arac = db.query(Arac).filter(Arac.id == arac_id).first()
    if not arac:
        raise HTTPException(status_code=404, detail="Araç bulunamadı")
    
    # Analytics: Detay görüntüleme takibi
    await track_detail_view(arac_id)
    
    return arac

@app.post("/araclar", response_model=AracResponse)
async def arac_ekle(arac: AracCreate, db: Session = Depends(get_db)):
    """Yeni araç ekle"""
    db_arac = Arac(**arac.dict())
    db.add(db_arac)
    db.commit()
    db.refresh(db_arac)
    
    # Analytics: Admin işlemi takibi
    await track_admin_action("vehicle_added", db_arac.id)
    
    return db_arac

@app.delete("/araclar/{arac_id}", response_model=MessageResponse)
async def arac_sil(arac_id: int, db: Session = Depends(get_db)):
    """Aracı sil"""
    arac = db.query(Arac).filter(Arac.id == arac_id).first()
    if not arac:
        raise HTTPException(status_code=404, detail="Araç bulunamadı")
    
    db.delete(arac)
    db.commit()
    
    # Analytics: Admin işlemi takibi
    await track_admin_action("vehicle_deleted", arac_id)
    
    return {"message": "Araç başarıyla silindi"}

@app.patch("/araclar/{arac_id}/favori", response_model=AracResponse)
async def favori_degistir(arac_id: int, db: Session = Depends(get_db)):
    """Favori durumunu değiştir"""
    arac = db.query(Arac).filter(Arac.id == arac_id).first()
    if not arac:
        raise HTTPException(status_code=404, detail="Araç bulunamadı")
    
    arac.favori = not arac.favori
    db.commit()
    db.refresh(arac)
    
    # Analytics: Favori tıklama takibi
    await track_favorite_click(arac_id)
    
    return arac

@app.put("/araclar/{arac_id}", response_model=AracResponse)
async def arac_guncelle(arac_id: int, arac_update: AracUpdate, db: Session = Depends(get_db)):
    """Aracı güncelle"""
    arac = db.query(Arac).filter(Arac.id == arac_id).first()
    if not arac:
        raise HTTPException(status_code=404, detail="Araç bulunamadı")
    
    for field, value in arac_update.dict(exclude_unset=True).items():
        setattr(arac, field, value)
    
    db.commit()
    db.refresh(arac)
    
    # Analytics: Admin işlemi takibi
    await track_admin_action("vehicle_updated", arac_id)
    
    return arac

@app.post("/login", response_model=LoginResponse)
async def login(kullanici: KullaniciLogin, db: Session = Depends(get_db)):
    """Kullanıcı girişi"""
    user = db.query(Kullanici).filter(
        Kullanici.kullanici_adi == kullanici.kullanici_adi,
        Kullanici.parola == kullanici.parola
    ).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre")
    
    return {
        "success": True,
        "message": "Giriş başarılı",
        "kullanici": {
            "id": user.id,
            "kullanici_adi": user.kullanici_adi,
            "admin": user.admin
        }
    }

@app.post("/logout", response_model=MessageResponse)
async def logout():
    """Kullanıcı çıkışı"""
    return {"message": "Çıkış başarılı"}
