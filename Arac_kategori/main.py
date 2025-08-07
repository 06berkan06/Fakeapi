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
    KullaniciLogin, LoginResponse, KullaniciCreate, KullaniciResponse
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
            Arac(isim="BMW X5", model="X5", yil=2023, kategori="SUV", fiyat=850000, favori=True, resim_url="https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=300&fit=crop"),
            Arac(isim="Mercedes C-Class", model="C-Class", yil=2022, kategori="Sedan", fiyat=650000, favori=False, resim_url="https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=400&h=300&fit=crop"),
            Arac(isim="Audi A3", model="A3", yil=2023, kategori="Hatchback", fiyat=450000, favori=True, resim_url="https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=400&h=300&fit=crop"),
            Arac(isim="Volkswagen Golf", model="Golf", yil=2021, kategori="Hatchback", fiyat=350000, favori=False, resim_url="https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=400&h=300&fit=crop"),
            Arac(isim="Toyota RAV4", model="RAV4", yil=2023, kategori="SUV", favori=True, resim_url="https://images.unsplash.com/photo-1541899481282-d53bffe3c55d?w=400&h=300&fit=crop"),
            Arac(isim="Honda Civic", model="Civic", yil=2022, kategori="Sedan", favori=False, resim_url="https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop"),
            Arac(isim="Ford F-150", model="F-150", yil=2023, kategori="Pickup", favori=True, resim_url="https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop"),
            Arac(isim="Nissan Qashqai", model="Qashqai", yil=2022, kategori="SUV", favori=False, resim_url="https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=400&h=300&fit=crop"),
            Arac(isim="Hyundai i30", model="i30", yil=2023, kategori="Hatchback", favori=True, resim_url="https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=400&h=300&fit=crop"),
            Arac(isim="Kia Sportage", model="Sportage", yil=2023, kategori="SUV", favori=False, resim_url="https://images.unsplash.com/photo-1541899481282-d53bffe3c55d?w=400&h=300&fit=crop"),
            Arac(isim="Mazda CX-5", model="CX-5", yil=2022, kategori="SUV", favori=True, resim_url="https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=300&fit=crop"),
            Arac(isim="Subaru Impreza", model="Impreza", yil=2023, kategori="Sedan", favori=False, resim_url="https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop"),
            Arac(isim="Volvo XC60", model="XC60", yil=2023, kategori="SUV", favori=True, resim_url="https://images.unsplash.com/photo-1541899481282-d53bffe3c55d?w=400&h=300&fit=crop"),
            Arac(isim="Lexus RX", model="RX", yil=2022, kategori="SUV", favori=False, resim_url="https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=300&fit=crop"),
            Arac(isim="Porsche Cayenne", model="Cayenne", yil=2023, kategori="SUV", favori=True, resim_url="https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=300&fit=crop"),
            Arac(isim="Tesla Model 3", model="Model 3", yil=2023, kategori="Sedan", favori=True, resim_url="https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop"),
            Arac(isim="Range Rover Sport", model="Sport", yil=2023, kategori="SUV", favori=False, resim_url="https://images.unsplash.com/photo-1541899481282-d53bffe3c55d?w=400&h=300&fit=crop"),
            Arac(isim="Bentley Continental", model="Continental", yil=2022, kategori="Sedan", favori=True, resim_url="https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=400&h=300&fit=crop"),
            Arac(isim="Ferrari F8", model="F8", yil=2023, kategori="Sports", favori=True, resim_url="https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop"),
            Arac(isim="Lamborghini Huracan", model="Huracan", yil=2023, kategori="Sports", favori=False, resim_url="https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop"),
            Arac(isim="McLaren 720S", model="720S", yil=2022, kategori="Sports", favori=True, resim_url="https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop"),
            Arac(isim="Bugatti Chiron", model="Chiron", yil=2023, kategori="Sports", favori=True, resim_url="https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop"),
            Arac(isim="Rolls Royce Phantom", model="Phantom", yil=2023, kategori="Sedan", favori=False, resim_url="https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=400&h=300&fit=crop"),
        ]
        
        for arac in araclar:
            db.add(arac)
    
    db.commit()
    db.close()

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("index.html")

@app.get("/login")
async def login_page():
    return FileResponse("login.html")

@app.get("/docs")
async def docs():
    return FileResponse("index.html")

# Analytics endpoints
@app.post("/analytics/view/{vehicle_id}")
async def track_vehicle_view(vehicle_id: int):
    """Araç görüntüleme sayısını takip et"""
    if vehicle_id not in analytics_data["vehicle_views"]:
        analytics_data["vehicle_views"][vehicle_id] = 0
    analytics_data["vehicle_views"][vehicle_id] += 1
    
    # Günlük istatistikleri güncelle
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in analytics_data["daily_stats"]:
        analytics_data["daily_stats"][today] = {"views": 0, "favorites": 0, "details": 0}
    analytics_data["daily_stats"][today]["views"] += 1
    
    return {"message": "View tracked"}

@app.post("/analytics/favorite/{vehicle_id}")
async def track_favorite_click(vehicle_id: int):
    """Favori tıklama sayısını takip et"""
    if vehicle_id not in analytics_data["favorite_clicks"]:
        analytics_data["favorite_clicks"][vehicle_id] = 0
    analytics_data["favorite_clicks"][vehicle_id] += 1
    
    # Günlük istatistikleri güncelle
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in analytics_data["daily_stats"]:
        analytics_data["daily_stats"][today] = {"views": 0, "favorites": 0, "details": 0}
    analytics_data["daily_stats"][today]["favorites"] += 1
    
    return {"message": "Favorite click tracked"}

@app.post("/analytics/detail/{vehicle_id}")
async def track_detail_view(vehicle_id: int):
    """Detay görüntüleme sayısını takip et"""
    if vehicle_id not in analytics_data["detail_views"]:
        analytics_data["detail_views"][vehicle_id] = 0
    analytics_data["detail_views"][vehicle_id] += 1
    
    # Günlük istatistikleri güncelle
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in analytics_data["daily_stats"]:
        analytics_data["daily_stats"][today] = {"views": 0, "favorites": 0, "details": 0}
    analytics_data["daily_stats"][today]["details"] += 1
    
    return {"message": "Detail view tracked"}

@app.post("/analytics/admin-action")
async def track_admin_action(action: str, vehicle_id: Optional[int] = None):
    """Admin işlemlerini takip et"""
    if action not in analytics_data["admin_actions"]:
        analytics_data["admin_actions"][action] = 0
    analytics_data["admin_actions"][action] += 1
    
    return {"message": "Admin action tracked"}

@app.get("/analytics/vehicle/{vehicle_id}")
async def get_vehicle_analytics(vehicle_id: int):
    """Belirli bir aracın analitik verilerini getir"""
    views = analytics_data["vehicle_views"].get(vehicle_id, 0)
    favorites = analytics_data["favorite_clicks"].get(vehicle_id, 0)
    details = analytics_data["detail_views"].get(vehicle_id, 0)
    
    return {
        "vehicle_id": vehicle_id,
        "views": views,
        "favorites": favorites,
        "details": details
    }

@app.get("/analytics/dashboard")
async def get_analytics_dashboard():
    """Analytics dashboard verilerini getir"""
    total_views = sum(analytics_data["vehicle_views"].values())
    total_favorites = sum(analytics_data["favorite_clicks"].values())
    total_details = sum(analytics_data["detail_views"].values())
    
    # En popüler araçlar
    top_vehicles = sorted(
        analytics_data["vehicle_views"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    # Günlük istatistikler
    today = datetime.now().strftime("%Y-%m-%d")
    today_stats = analytics_data["daily_stats"].get(today, {"views": 0, "favorites": 0, "details": 0})
    
    return {
        "total_views": total_views,
        "total_favorites": total_favorites,
        "total_details": total_details,
        "today_views": today_stats["views"],
        "today_favorites": today_stats["favorites"],
        "today_details": today_stats["details"],
        "top_vehicles": top_vehicles,
        "admin_actions": analytics_data["admin_actions"]
    }

@app.get("/analytics/trends")
async def get_analytics_trends(days: int = 7):
    """Son X günün trend verilerini getir"""
    trends = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        stats = analytics_data["daily_stats"].get(date, {"views": 0, "favorites": 0, "details": 0})
        trends.append({
            "date": date,
            "views": stats["views"],
            "favorites": stats["favorites"],
            "details": stats["details"]
        })
    
    return {"trends": trends[::-1]}  # En eski tarihten en yeniye

# Araç endpoints
@app.get("/araclar", response_model=List[AracResponse])
async def araclari_listele(favori: Optional[bool] = None, db: Session = Depends(get_db)):
    """Tüm araçları listele"""
    query = db.query(Arac)
    if favori is not None:
        query = query.filter(Arac.favori == favori)
    araclar = query.all()
    
    # Analytics tracking
    for arac in araclar:
        await track_vehicle_view(arac.id)
    
    return araclar

@app.get("/araclar/{arac_id}", response_model=AracResponse)
async def arac_detay(arac_id: int, db: Session = Depends(get_db)):
    """Belirli bir aracın detaylarını getir"""
    arac = db.query(Arac).filter(Arac.id == arac_id).first()
    if not arac:
        raise HTTPException(status_code=404, detail="Araç bulunamadı")
    
    # Analytics tracking
    await track_detail_view(arac_id)
    
    return arac

@app.post("/araclar", response_model=AracResponse)
async def arac_ekle(arac: AracCreate, db: Session = Depends(get_db)):
    """Yeni araç ekle"""
    # Varsayılan resim URL'si
    default_image = "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=300&fit=crop"
    
    db_arac = Arac(
        isim=arac.isim,
        model=arac.model,
        yil=arac.yil,
        kategori=arac.kategori,
        aciklama=arac.aciklama,
        favori=False,
        resim_url=arac.resim_url or default_image
    )
    db.add(db_arac)
    db.commit()
    db.refresh(db_arac)
    
    # Analytics tracking
    await track_admin_action("add_vehicle", db_arac.id)
    
    return db_arac

@app.delete("/araclar/{arac_id}")
async def arac_sil(arac_id: int, db: Session = Depends(get_db)):
    """Aracı sil"""
    arac = db.query(Arac).filter(Arac.id == arac_id).first()
    if not arac:
        raise HTTPException(status_code=404, detail="Araç bulunamadı")
    
    db.delete(arac)
    db.commit()
    
    # Analytics tracking
    await track_admin_action("delete_vehicle", arac_id)
    
    return {"success": True, "message": "Araç başarıyla silindi"}

@app.patch("/araclar/{arac_id}/favori", response_model=AracResponse)
async def favori_degistir(arac_id: int, db: Session = Depends(get_db)):
    """Aracın favori durumunu değiştir"""
    arac = db.query(Arac).filter(Arac.id == arac_id).first()
    if not arac:
        raise HTTPException(status_code=404, detail="Araç bulunamadı")
    
    arac.favori = not arac.favori
    db.commit()
    db.refresh(arac)
    
    # Analytics tracking
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
    
    # Analytics tracking
    await track_admin_action("update_vehicle", arac_id)
    
    return arac

# Kullanıcı endpoints
@app.post("/login", response_model=LoginResponse)
async def login(kullanici: KullaniciLogin, db: Session = Depends(get_db)):
    """Kullanıcı girişi"""
    db_kullanici = db.query(Kullanici).filter(
        Kullanici.kullanici_adi == kullanici.kullanici_adi,
        Kullanici.parola == kullanici.parola
    ).first()
    
    if not db_kullanici:
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre")
    
    return {
        "success": True,
        "message": "Giriş başarılı",
        "kullanici": {
            "id": db_kullanici.id,
            "kullanici_adi": db_kullanici.kullanici_adi,
            "admin": db_kullanici.admin
        }
    }

@app.post("/register", response_model=LoginResponse)
async def register(kullanici: KullaniciCreate, db: Session = Depends(get_db)):
    """Yeni kullanıcı kaydı"""
    # Kullanıcı adı kontrolü
    existing_user = db.query(Kullanici).filter(
        Kullanici.kullanici_adi == kullanici.kullanici_adi
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten kullanılıyor")
    
    # Yeni kullanıcı oluştur (varsayılan olarak admin değil)
    new_user = Kullanici(
        kullanici_adi=kullanici.kullanici_adi,
        parola=kullanici.parola,
        admin=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "Kayıt başarılı",
        "kullanici": {
            "id": new_user.id,
            "kullanici_adi": new_user.kullanici_adi,
            "admin": new_user.admin
        }
    }

@app.post("/logout")
async def logout():
    """Kullanıcı çıkışı"""
    return {"success": True, "message": "Çıkış başarılı"}
