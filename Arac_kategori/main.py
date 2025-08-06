from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from .models import seed_data
from typing import List, Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Araç Yönetim API",
    description="Yol bakım araçları için profesyonel yönetim sistemi",
    version="1.0.0"
)

# Session management will be handled via cookies or local storage

# CORS ayarları (gerekirse frontend için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static dosyaları serve et
app.mount("/static", StaticFiles(directory="Fakeapi/Arac_kategori"), 
          name="static")


@app.get("/")
async def root():
    """Ana sayfa - HTML arayüzü"""
    return FileResponse("Fakeapi/Arac_kategori/index.html")


@app.get("/araclar-ui")
async def arac_ui():
    """Araç yönetim arayüzü"""
    return FileResponse("Fakeapi/Arac_kategori/index.html")


@app.get("/login")
async def login_page():
    """Login sayfası"""
    return FileResponse("Fakeapi/Arac_kategori/login.html")


@app.on_event("startup")
def startup_event():
    from .database import SessionLocal
    db = SessionLocal()
    seed_data(db)
    db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Mevcut kullanıcıyı al"""
    # For now, we'll use a simple approach without session middleware
    # The frontend will handle user state via localStorage
    return None


def require_admin(user: models.Kullanici = Depends(get_current_user)):
    """Admin yetkisi gerektiren işlemler için"""
    if not user or not user.admin:
        raise HTTPException(status_code=403, 
                          detail="Bu işlem için admin yetkisi gereklidir")
    return user


@app.post("/login", response_model=schemas.LoginResponse)
def login(login_data: schemas.KullaniciLogin, db: Session = Depends(get_db)):
    """Kullanıcı girişi"""
    kullanici = db.query(models.Kullanici).filter(
        models.Kullanici.kullanici_adi == login_data.kullanici_adi,
        models.Kullanici.parola == login_data.parola
    ).first()
    
    if kullanici:
        return schemas.LoginResponse(
            success=True,
            message="Giriş başarılı",
            kullanici=schemas.KullaniciResponse(
                id=kullanici.id,
                kullanici_adi=kullanici.kullanici_adi,
                admin=kullanici.admin
            )
        )
    else:
        raise HTTPException(status_code=401, 
                          detail="Geçersiz kullanıcı adı veya parola")


@app.post("/logout")
def logout():
    """Kullanıcı çıkışı"""
    return {"message": "Çıkış başarılı"}


@app.get("/me", response_model=schemas.KullaniciResponse)
def get_current_user_info():
    """Mevcut kullanıcı bilgilerini al"""
    # For now, return a default response since we're not using session middleware
    raise HTTPException(status_code=401, detail="Giriş yapılmamış")


@app.get("/araclar", response_model=List[schemas.AracResponse])
def araclari_listele(
    db: Session = Depends(get_db),
    favori: Optional[bool] = Query(None, 
                                   description="Sadece favorileri göster")
):
    """Tüm araçları listele veya sadece favorileri göster"""
    query = db.query(models.Arac)
    if favori is not None:
        query = query.filter(models.Arac.favori == favori)
    return query.all()


@app.post("/araclar", response_model=schemas.AracResponse)
def arac_ekle(arac: schemas.AracCreate, db: Session = Depends(get_db)):
    """Yeni araç ekle"""
    try:
        yeni_arac = models.Arac(**arac.dict())
        db.add(yeni_arac)
        db.commit()
        db.refresh(yeni_arac)
        return yeni_arac
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, 
                          detail=f"Araç eklenirken hata: {str(e)}")


@app.delete("/araclar/{id}", response_model=schemas.MessageResponse)
def arac_sil(id: int, db: Session = Depends(get_db)):
    """Araç sil"""
    arac = db.query(models.Arac).get(id)
    if not arac:
        raise HTTPException(status_code=404, detail="Araç bulunamadı")
    
    try:
        db.delete(arac)
        db.commit()
        return schemas.MessageResponse(
            message="Araç başarıyla silindi",
            success=True,
            data={"id": id}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, 
                          detail=f"Silme hatası: {str(e)}")


@app.patch("/araclar/{id}/favori", response_model=schemas.AracResponse)
def favori_degistir(id: int, db: Session = Depends(get_db)):
    """Aracın favori durumunu değiştir"""
    arac = db.query(models.Arac).get(id)
    if not arac:
        raise HTTPException(status_code=404, detail="Araç bulunamadı")
    
    try:
        arac.favori = not arac.favori
        db.commit()
        db.refresh(arac)
        return arac
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, 
                          detail=f"Favori değiştirme hatası: {str(e)}")


@app.put("/araclar/{id}", response_model=schemas.AracResponse)
def arac_guncelle(
    id: int, 
    guncel_arac: schemas.AracUpdate, 
    db: Session = Depends(get_db)
):
    """Araç bilgilerini güncelle"""
    arac = db.query(models.Arac).get(id)
    if not arac:
        raise HTTPException(status_code=404, detail="Araç bulunamadı")
    
    try:
        update_data = guncel_arac.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(arac, key, value)
        db.commit()
        db.refresh(arac)
        return arac
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, 
                          detail=f"Güncelleme hatası: {str(e)}")


@app.get("/araclar/search", response_model=List[schemas.AracResponse])
def arac_ara(
    q: str = Query(..., description="Arama terimi"),
    db: Session = Depends(get_db)
):
    """Araç ara"""
    query = db.query(models.Arac).filter(
        models.Arac.isim.ilike(f"%{q}%") |
        models.Arac.kategori.ilike(f"%{q}%") |
        models.Arac.model.ilike(f"%{q}%")
    )
    return query.all()
